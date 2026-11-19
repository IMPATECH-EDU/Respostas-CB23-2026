"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

import numpy as np

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook

VAZOES = np.linspace(0.0, 100.0, 11)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")


def _adutora() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton deve recalcular a derivada a cada iteração (convergência quadrática)."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Colebrook com Re = 1e4 converge em no máximo 6 iterações (o relato fala em 10)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_2_com_derivada_exata(self):
        """x² - 2 a partir de x0 = 2, com f' exata, converge em no máximo 6 iterações."""
        newton = Newton(tol=1e-12, df=lambda x: 2 * x)
        resultado = newton.encontrar(lambda x: x * x - 2, 0.0, 4.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_erro_cai_quadraticamente(self):
        """Perto da raiz, o novo erro é no máximo da ordem do quadrado do erro anterior."""
        newton = Newton(tol=1e-15, df=lambda x: 2 * x)
        historico = newton.encontrar(lambda x: x * x - 2, 0.0, 4.0).historico
        erros = [abs(x - math.sqrt(2)) for x in historico]
        # e_{k+1} ≈ e_k² / (2·sqrt(2)) para Newton; com a derivada fixa, e_{k+1} ≈ 0,29·e_k.
        e1, e2 = erros[2], erros[3]
        self.assertGreater(e1, 1e-8)
        self.assertLess(e2, e1 ** 2)


class TestContratoPontoOperacao(unittest.TestCase):
    """Issue #8: regras de ponto_operacao que os testes de aceitação não verificam."""

    def test_intervalo_invertido(self):
        """a >= b levanta ValueError antes de chamar o resolvedor."""
        for a, b in [(80.0, 20.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _adutora(), Bisseccao(), a=a, b=b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Um intervalo que sai do domínio do ensaio (0 a 100 L/s) levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(BOMBA, _adutora(), Bisseccao(), a=10.0, b=120.0)

    def test_resolvedor_que_nao_converge(self):
        """Se o resolvedor para em max_iter sem convergir, ponto_operacao levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _adutora(), Bisseccao(tol=1e-10, max_iter=3))


class TestContratoOrdemConvergencia(unittest.TestCase):
    """Issue #8: regras de ordem_convergencia que os testes de aceitação não verificam."""

    def test_erros_abaixo_do_piso_sao_ignorados(self):
        """Erros no nível do arredondamento ficam de fora; valem os 3 últimos acima do piso."""
        historico = [2.0 + 1e-1, 2.0 + 1e-3, 2.0 + 1e-9, 2.0 + 1e-15, 2.0 + 4e-16, 2.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 2.0), 3.0, delta=1e-3)

    def test_piso_relativo_ao_tamanho_da_raiz(self):
        """Para raízes grandes, o piso escala com |raiz|: 1e-14 · 1e6 = 1e-8."""
        raiz = 1e6
        historico = [raiz + 1.0, raiz + 1e-1, raiz + 5e-9, raiz + 1e-9]   # só 2 acima de 1e-8
        with self.assertRaises(ValueError):
            ordem_convergencia(historico, raiz)

    def test_ordem_cubica(self):
        """Erros 1e-1, 1e-3, 1e-9 indicam convergência de ordem 3."""
        historico = [1.0 + 1e-1, 1.0 + 1e-3, 1.0 + 1e-9]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 3.0, delta=1e-4)


if __name__ == "__main__":
    unittest.main()

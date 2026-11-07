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


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: o Newton precisa reavaliar a derivada e convergir quadraticamente."""

    def test_raiz_de_dois_em_poucas_iteracoes(self):
        """x² − 2 a partir de x0 = 1: Newton de verdade chega a 1e-12 em no máximo 6 passos."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_colebrook_re_1e4(self):
        """Fator de atrito em Re = 10⁴ com no máximo 6 iterações (o relato fala em ~5)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_avaliada_a_cada_iteracao(self):
        """Com df fornecida, df é chamada uma vez por iteração, e não uma vez só."""
        chamadas = []

        def derivada(x: float) -> float:
            chamadas.append(x)
            return 3.0 * x * x

        resultado = Newton(tol=1e-12, df=derivada).encontrar(lambda x: x ** 3 - 8.0, 1.0, 4.0)
        self.assertAlmostEqual(resultado.raiz, 2.0, places=12)
        self.assertEqual(len(chamadas), resultado.iteracoes)

    def test_erros_caem_quadraticamente(self):
        """Perto da raiz, e_{k+1} / e_k² fica limitado (≈ f''/2f' = 1/(2√2) para x² − 2)."""
        raiz = math.sqrt(2.0)
        historico = Newton(tol=1e-14).encontrar(lambda x: x * x - 2.0, 0.0, 2.0).historico
        erros = [abs(x - raiz) for x in historico if abs(x - raiz) > 1e-13]
        for anterior, seguinte in zip(erros[1:], erros[2:]):
            self.assertLess(seguinte / anterior ** 2, 1.0)


_Q = np.arange(0.0, 101.0, 10.0)
_BOMBA = CurvaCalibracao(_Q, 50.0 - 0.004 * _Q ** 2, "spline")


def _adutora() -> Tubulacao:
    """A adutora da estação, com Newton resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Newton(tol=1e-12))


class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: regras de ponto_operacao que os testes de aceitação não verificam."""

    def test_intervalo_invertido(self):
        """a >= b é recusado antes de chamar o resolvedor."""
        for a, b in [(60.0, 30.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(_BOMBA, _adutora(), Bisseccao(), a=a, b=b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Um b além do último ponto do ensaio (100 L/s) é recusado: a curva não extrapola."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(_BOMBA, _adutora(), Bisseccao(), a=10.0, b=120.0)

    def test_resolvedor_que_nao_converge(self):
        """Se o resolvedor esgota max_iter sem convergir, ponto_operacao levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "convergiu"):
            ponto_operacao(_BOMBA, _adutora(), Bisseccao(tol=1e-12, max_iter=3))

    def test_resultado_e_o_do_resolvedor(self):
        """A vazão é a raiz do ResultadoRaiz e a altura é bomba(vazão)."""
        ponto = ponto_operacao(_BOMBA, _adutora(), Newton(tol=1e-10))
        self.assertTrue(ponto.resultado.convergiu)
        self.assertEqual(ponto.vazao, ponto.resultado.raiz)
        self.assertAlmostEqual(ponto.altura, _BOMBA(ponto.vazao))


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: regras de ordem_convergencia que os testes de aceitação não verificam."""

    def test_ordem_cubica(self):
        """Erros 1e-1, 1e-3, 1e-9 dão p = 3."""
        self.assertAlmostEqual(ordem_convergencia([2.1, 2.001, 2 + 1e-9], 2.0), 3.0, places=4)

    def test_piso_relativo_a_raiz(self):
        """Com raiz 1e6, o piso vira 1e-8: o erro 1e-9 sai, e a ordem é 2 (e não 2,5)."""
        raiz = 1e6
        historico = [raiz + 1e-1, raiz + 1e-2, raiz + 1e-4, raiz + 1e-9]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 2.0, delta=0.01)

    def test_erros_abaixo_do_piso_nao_contam(self):
        """Só dois erros acima do piso: ValueError, mesmo com um histórico longo."""
        historico = [1.5, 1.25] + [1.0 + 1e-16] * 5 + [1.0]
        with self.assertRaises(ValueError):
            ordem_convergencia(historico, 1.0)


if __name__ == "__main__":
    unittest.main()

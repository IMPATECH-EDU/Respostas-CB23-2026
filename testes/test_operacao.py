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
from elevatoria.raizes import Bisseccao, MetodoRaiz, Newton, ResultadoRaiz
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook

VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")


def _tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: o Newton deve convergir quadraticamente."""

    def test_colebrook_em_poucas_iteracoes(self) -> None:
        """Colebrook com Re = 1e4 converge em até 6 iterações, e não em 10, como no relato."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_dois_em_poucas_iteracoes(self) -> None:
        """x² − 2 a partir de x0 = 1 converge em até 6 iterações com a derivada exata."""
        resultado = Newton(tol=1e-12, df=lambda x: 2 * x).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_digitos_dobram(self) -> None:
        """Perto da raiz, cada erro é da ordem do quadrado do anterior: e_{k+1} ≤ e_k²."""
        resultado = Newton(tol=1e-15, df=lambda x: 2 * x).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        erros = [abs(x - math.sqrt(2)) for x in resultado.historico]
        self.assertLessEqual(erros[3], erros[2] ** 2)
        self.assertLessEqual(erros[4], erros[3] ** 2)


class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: regras do contrato de ponto_operacao que os testes de aceitação não verificam."""

    def test_intervalo_invertido(self) -> None:
        """a >= b levanta ValueError antes de chamar o resolvedor."""
        for a, b in [(60.0, 40.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=a, b=b)

    def test_fora_do_dominio_da_bomba(self) -> None:
        """Um intervalo que sai do domínio da bomba levanta ValueError, sem extrapolar."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=10.0, b=120.0)

    def test_resolvedor_que_nao_converge(self) -> None:
        """Se o resolvedor esgota max_iter, ponto_operacao levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(tol=1e-10, max_iter=3))


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: o piso de ordem_convergencia, que os testes de aceitação não verificam."""

    def test_erros_abaixo_do_piso_sao_ignorados(self) -> None:
        """Erros no nível do arredondamento não entram: os 3 últimos acima do piso valem."""
        historico = [1 + 1e-2, 1 + 1e-4, 1 + 1e-8, 1 + 1e-15, 1 + 2e-16, 1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, delta=0.01)

    def test_piso_relativo_a_raiz(self) -> None:
        """Com |raiz| grande, o piso escala com ela: 1e-14 · 1e6 = 1e-8 descarta o erro 1e-9."""
        raiz = 1e6
        historico = [raiz + 1e-1, raiz + 1e-5, raiz + 1e-9]
        with self.assertRaises(ValueError):
            ordem_convergencia(historico, raiz)


if __name__ == "__main__":
    unittest.main()

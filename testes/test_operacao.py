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

VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²


def _tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: testes de regressão do Newton (escritos antes da correção)."""

    def test_newton_raiz_de_2_em_poucas_iteracoes(self):
        """Newton para x² - 2 em [0, 2], com tol 1e-12, converge em no máximo 7 iterações."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=12)
        self.assertLessEqual(resultado.iteracoes, 7)

    def test_newton_converge_quadraticamente(self):
        """A ordem de convergência estimada do Newton para x² - 2 é cerca de 2."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertGreater(ordem_convergencia(resultado.historico, math.sqrt(2)), 1.8)

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Colebrook com Re = 1e4 pelo Newton leva no máximo 6 iterações (o relato fala em 10)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)


class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: regras do contrato de ponto_operacao que os testes de aceitação não verificam."""

    def test_intervalo_invertido(self):
        """a >= b levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=90.0, b=40.0)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Um intervalo que sai do domínio da bomba ([0, 100] L/s) levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=10.0, b=120.0)

    def test_resolvedor_que_nao_converge(self):
        """Se o resolvedor não converge (bissecção com só 3 iterações), levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(tol=1e-10, max_iter=3))


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: regras do contrato de ordem_convergencia que os testes de aceitação não verificam."""

    def test_ignora_erros_abaixo_do_piso(self):
        """Erros abaixo de piso · max(1, |raiz|) são ignorados: só os 3 últimos acima dele contam."""
        historico = [1 + 1e-1, 1 + 1e-2, 1 + 1e-4, 1 + 1e-8, 1 + 1e-16]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, delta=0.01)

    def test_piso_relativo_ao_tamanho_da_raiz(self):
        """Com raiz 1e6 o piso vira 1e-8: um erro de 1e-9 não conta e sobram só 2 erros."""
        historico = [1e6 + 1e-2, 1e6 + 1e-4, 1e6 + 1e-9]
        with self.assertRaises(ValueError):
            ordem_convergencia(historico, 1e6)


if __name__ == "__main__":
    unittest.main()
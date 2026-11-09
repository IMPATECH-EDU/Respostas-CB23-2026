"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook

VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²


def tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))

class TestNewtonRegressao(unittest.TestCase):
    """Regressão da issue #9: o Newton precisa convergir quadraticamente."""

    def test_raiz_de2_poucas_iteracoes(self):
        """O Newton acha a raiz de x² - 2 em no máximo 7 iterações."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertLessEqual(resultado.iteracoes, 7)

    def test_colebrook_re(self):
        """Com Re = 1e4, o Newton resolve Colebrook em no máximo 6 iterações."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

class TestPontoOperacaoContrato(unittest.TestCase):
    """Regras do contrato de `ponto_operacao` que os testes de aceitação não cobrem."""

    def test_intervalo_fora_do_dominio(self):
        """Um intervalo que sai do domínio da bomba levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Newton(), a=-50.0, b=150.0)

    def test_resolvedor_nao_converge(self):
        """Um resolvedor que não converge levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(max_iter=1))

if __name__ == "__main__":
    unittest.main()

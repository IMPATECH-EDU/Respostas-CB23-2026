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
from fornecido.hidraulica import Tubulacao

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestNewton(unittest.TestCase):
    """Testes contra o método de Newton"""
    def test_iteracoes(self) -> None:
        """Verifica se o número de iterações bate com o esperado do método de Newton"""
        resultado = Newton().encontrar(lambda x: x**2 - 2, 1, 2)
        self.assertLessEqual(resultado.iteracoes, 5)

    def test_erro(self) -> None:
        """Garante que o erro desaparece na taxa esperada para o método de Newton"""
        resultado = Newton().encontrar(lambda x: x**2 - 2, 1, 2)
        self.assertAlmostEqual(resultado.historico[3], math.sqrt(2), 9)

class TestOperacao(unittest.TestCase):
    """Testes do contrato de ponto_operacao e ordem_convergencia"""
    def test_ponto_operacao(self) -> None:
        """Verifica se convergiu=False causa erro ao forçar só 1 iteração"""
        VAZOES = np.arange(0.0, 101.0, 10.0)
        BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")
        tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))
        self.assertRaises(ValueError, lambda: ponto_operacao(BOMBA, tubulacao, Newton(max_iter=1), 0, 10))

    def test_ordem_convergencia(self) -> None:
        """Erros abaixo do piso são ignorados: a ordem continua sendo 2."""
        historico = [1e-1, 1e-2, 1e-4, 1e-8, 1e-15, 1e-16]
        self.assertAlmostEqual(ordem_convergencia(historico, 0.0), 2.0)
        

if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão para o defeito da issue #9 em `Newton`."""

    def test_newton_colebrook_poucas_iteracoes(self):
        """Resolve Colebrook para Re = 1e4 em no máximo 6 iterações com Newton."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_newton_convergencia_quadratica_raiz_de_2(self):
        """Encontra sqrt(2) em [0, 2] com convergência quadrática (no máximo 6 iterações)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)


if __name__ == "__main__":
    unittest.main()
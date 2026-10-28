"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))



import math
from elevatoria.raizes import Newton


class TestNewtonRegressao(unittest.TestCase):
    """Regressões da atualização da derivada da issue #9."""

    def test_derivada_analitica_atualizada(self) -> None:
        """Newton analítico alcança sqrt(2) dentro de seis iterações."""
        resultado = Newton(tol=1e-12, max_iter=6, df=lambda x: 2*x).encontrar(
            lambda x: x*x - 2, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=12)

    def test_derivada_numerica_atualizada(self) -> None:
        """Newton numérico converge para a raiz cúbica dentro de seis iterações."""
        resultado = Newton(tol=1e-10, max_iter=6).encontrar(
            lambda x: x**3 - 7, 1.0, 4.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, 7 ** (1/3), places=9)


if __name__ == "__main__":
    unittest.main()

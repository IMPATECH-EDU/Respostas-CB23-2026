"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# ---------------------------------------------------------------------------------------
# Issue #9: testes de regressão do Newton (escritos antes da correção)
# ---------------------------------------------------------------------------------------
class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: o Newton tem que convergir quadraticamente."""

    def test_colebrook_em_re_1e4(self):
        """O caso do relato: em Re = 1e4 o fator de atrito sai em no máximo 6 iterações."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_dois(self):
        """x² - 2 a partir de x0 = 1 converge em no máximo 6 iterações (não em ~30)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_calculada_em_cada_ponto(self):
        """A derivada df é chamada uma vez por iteração, sempre no ponto atual."""
        pontos = []

        def df(x):
            pontos.append(x)
            return 2 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertEqual(pontos, list(resultado.historico[:-1]))


if __name__ == "__main__":
    unittest.main()

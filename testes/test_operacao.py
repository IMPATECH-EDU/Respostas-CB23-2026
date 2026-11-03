"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao, Newton, ResultadoRaiz


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9."""

    def test_newton_recalcula_derivada(self):
        """Newton converge para raiz de x² - 2 em até cinco iterações."""
        f = lambda x: x**2 - 2
        df = lambda x: 2*x
        resultado = Newton(tol=1e-10, max_iter=5, df=df).encontrar(f, 1.0, 2.0)

        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, 2**0.5, places=10)

    def test_newton_sem_derivada(self):
        """Newton converge para raiz de x² - 2 em até cinco iterações, mesmo sem derivada."""
        f = lambda x: x**2 - 2
        resultado = Newton(tol=1e-10, max_iter=5).encontrar(f, 1.0, 2.0)

        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, 2**0.5, places=10)

if __name__ == "__main__":
    unittest.main()

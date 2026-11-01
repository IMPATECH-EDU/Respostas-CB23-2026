"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.raizes import Bisseccao, Newton

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestRegressaoIssue9(unittest.TestCase):

    def test_newton_com_derivada_exata(self):
        """Verifica se o Newton atualiza a derivada exata a cada iteração."""
        f = lambda x: x**2 - 2
        df = lambda x: 2 * x

        resultado = Newton(
            tol=1e-12, max_iter=100, df=df
        ).encontrar(f, 1.0, 2.0)

        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=11)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_newton_com_derivada_numerica(self):
        """Verifica se o Newton atualiza a derivada numérica a cada iteração."""
        f = lambda x: x**2 - 2

        resultado = Newton(
            tol=1e-12, max_iter=100
        ).encontrar(f, 1.0, 2.0)

        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=11)
        self.assertLessEqual(resultado.iteracoes, 6)


if __name__ == "__main__":
    unittest.main()

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


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton calculava a derivada uma vez só e convergia linearmente."""

    @staticmethod
    def f(x: float) -> float:
        """x² - 2, cuja raiz positiva é √2."""
        return x * x - 2.0

    def test_raiz_de_dois_em_no_maximo_seis_iteracoes(self):
        """Partindo de 1,5, o Newton chega a √2 com tol 1e-12 em no máximo 6 iterações."""
        resultado = Newton(tol=1e-12).encontrar(self.f, 0.0, 3.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_digitos_corretos_dobram_a_cada_iteracao(self):
        """Com 2 iterações a partir de 1,5, o erro já é menor que 1e-5 (convergência quadrática)."""
        historico = Newton(tol=1e-12).encontrar(self.f, 0.0, 3.0).historico
        self.assertLess(abs(historico[2] - math.sqrt(2.0)), 1e-5)


if __name__ == "__main__":
    unittest.main()

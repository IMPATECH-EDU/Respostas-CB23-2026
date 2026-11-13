"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import math

from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestNewton(unittest.TestCase):
    """Testes de regressão da velocidade de convergência do Newton (issue #9)."""

    def test_raiz_quadrada_com_derivada_exata(self) -> None:
        """Newton encontra a raiz de x² - 2 em até seis iterações com derivada exata."""
        metodo = Newton(tol=1e-12, max_iter=6, df=lambda x: 2 * x)
        resultado = metodo.encontrar(lambda x: x * x - 2, 0.0, 2.0)

        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=10)

    def test_colebrook_com_derivada_numerica(self) -> None:
        """Colebrook para Re = 10000 converge em até seis iterações de Newton."""
        metodo = Newton(tol=1e-12, max_iter=6)
        fator, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, metodo)

        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(fator, 0.03202, delta=5e-5)


if __name__ == "__main__":
    unittest.main()

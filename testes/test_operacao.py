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


class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: o Newton precisa reavaliar a derivada e convergir quadraticamente."""

    def test_raiz_de_dois_em_poucas_iteracoes(self):
        """x² − 2 a partir de x0 = 1: Newton de verdade chega a 1e-12 em no máximo 6 passos."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_colebrook_re_1e4(self):
        """Fator de atrito em Re = 10⁴ com no máximo 6 iterações (o relato fala em ~5)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_avaliada_a_cada_iteracao(self):
        """Com df fornecida, df é chamada uma vez por iteração, e não uma vez só."""
        chamadas = []

        def derivada(x: float) -> float:
            chamadas.append(x)
            return 3.0 * x * x

        resultado = Newton(tol=1e-12, df=derivada).encontrar(lambda x: x ** 3 - 8.0, 1.0, 4.0)
        self.assertAlmostEqual(resultado.raiz, 2.0, places=12)
        self.assertEqual(len(chamadas), resultado.iteracoes)

    def test_erros_caem_quadraticamente(self):
        """Perto da raiz, e_{k+1} / e_k² fica limitado (≈ f''/2f' = 1/(2√2) para x² − 2)."""
        raiz = math.sqrt(2.0)
        historico = Newton(tol=1e-14).encontrar(lambda x: x * x - 2.0, 0.0, 2.0).historico
        erros = [abs(x - raiz) for x in historico if abs(x - raiz) > 1e-13]
        for anterior, seguinte in zip(erros[1:], erros[2:]):
            self.assertLess(seguinte / anterior ** 2, 1.0)


if __name__ == "__main__":
    unittest.main()

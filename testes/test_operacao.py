"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook

RUGOSIDADE_RELATIVA = 0.15e-3 / 0.20


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton calculava a derivada uma vez só e convergia linearmente."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Colebrook com Re = 1e4 e tol = 1e-12 converge em no máximo 6 iterações (eram 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_2_converge_rapido(self):
        """x² − 2 a partir de x0 = 1 converge em no máximo 6 iterações (eram mais de 30)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_avaliada_a_cada_iteracao(self):
        """Com df fornecida, df é chamada uma vez por iteração, sempre no ponto atual."""
        pontos = []

        def df(x: float) -> float:
            pontos.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertEqual(len(pontos), resultado.iteracoes)
        self.assertEqual(pontos, list(resultado.historico[:-1]))


if __name__ == "__main__":
    unittest.main()

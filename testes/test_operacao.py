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


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton deve recalcular a derivada a cada iteração (convergência quadrática)."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Colebrook com Re = 1e4 converge em no máximo 6 iterações (o relato fala em 10)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_2_com_derivada_exata(self):
        """x² - 2 a partir de x0 = 2, com f' exata, converge em no máximo 6 iterações."""
        newton = Newton(tol=1e-12, df=lambda x: 2 * x)
        resultado = newton.encontrar(lambda x: x * x - 2, 0.0, 4.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_erro_cai_quadraticamente(self):
        """Perto da raiz, o novo erro é no máximo da ordem do quadrado do erro anterior."""
        newton = Newton(tol=1e-15, df=lambda x: 2 * x)
        historico = newton.encontrar(lambda x: x * x - 2, 0.0, 4.0).historico
        erros = [abs(x - math.sqrt(2)) for x in historico]
        # e_{k+1} ≈ e_k² / (2·sqrt(2)) para Newton; com a derivada fixa, e_{k+1} ≈ 0,29·e_k.
        e1, e2 = erros[2], erros[3]
        self.assertGreater(e1, 1e-8)
        self.assertLess(e2, e1 ** 2)


if __name__ == "__main__":
    unittest.main()

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


# Issue #9: regressão do Newton

RUGOSIDADE_RELATIVA = 0.15e-3 / 0.20


class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9 (escritos antes da correção)."""

    def test_poucas_iteracoes_para_a_raiz_de_dois(self):
        """Newton em x² - 2 a partir de 1 converge em poucas iterações (o defeito levava dezenas)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=10)
        self.assertLessEqual(resultado.iteracoes, 8)

    def test_derivada_recalculada_a_cada_iteracao(self):
        """Com df fornecida, ela é chamada uma vez por iteração e não só no ponto inicial."""
        chamadas = []

        def df(x: float) -> float:
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertEqual(len(chamadas), resultado.iteracoes)
        self.assertGreater(len(set(chamadas)), 1)

    def test_erro_cai_com_o_quadrado_a_cada_passo(self):
        """Em x² - 2, cada erro é no máximo o quadrado do anterior (convergência quadrática)."""
        resultado = Newton(tol=1e-13).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        erros = [abs(x - math.sqrt(2)) for x in resultado.historico]
        for anterior, seguinte in zip(erros, erros[1:]):
            if anterior > 1e-7:
                self.assertLessEqual(seguinte, anterior ** 2)

    def test_colebrook_re_1e4_com_cinco_ou_seis_iteracoes(self):
        """No Colebrook com Re = 1e4 o Newton gasta no máximo 6 iterações (eram 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)


if __name__ == "__main__":
    unittest.main()

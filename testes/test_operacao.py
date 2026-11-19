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
    """Issue #9: o Newton convergia devagar. Escritos antes da correção."""

    def test_colebrook_com_re_1e4(self):
        """Colebrook em Re = 1e4 converge em até 6 iterações (o relato via 10)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_erro_cai_ao_quadrado(self):
        """Em x² - 2 com a derivada exata, cada erro fica abaixo do quadrado do anterior."""
        r = Newton(tol=1e-12, df=lambda x: 2 * x).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        erros = [abs(x - math.sqrt(2)) for x in r.historico]
        for k in (1, 2, 3):
            with self.subTest(k=k):
                self.assertLess(erros[k + 1], erros[k] ** 2)


if __name__ == "__main__":
    unittest.main()

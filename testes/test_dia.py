"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioMalhaIrregular(unittest.TestCase):
    """Testes de regressão da issue #11: o trapézio de tabela precisa usar a largura de cada passo."""

    def test_reta_em_malha_irregular(self):
        """Issue #11: ∫ x dx em x = [0, 1, 3] vale 4,5 (passos de 1 e de 2)."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x), 4.5)

    def test_constante_com_leitura_perdida(self):
        """Issue #11: ∫ 2 dx em [0, 1], com a leitura de 0,5 perdida, vale 2."""
        x = np.array([0.0, 0.25, 0.75, 1.0])
        y = np.full(4, 2.0)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 2.0)

    def test_parabola_em_malha_irregular(self):
        """Issue #11: trapézios de x² em x = [0, 0,25, 0,75, 1] somam 0,359375."""
        x = np.array([0.0, 0.25, 0.75, 1.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x ** 2), 0.359375)


if __name__ == "__main__":
    unittest.main()

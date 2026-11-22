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


# ---------------------------------------------------------------------------------------
# Issue #11: regressão do trapézio em tabela (escritos antes da correção; falham no original)
# ---------------------------------------------------------------------------------------
class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: integrar_tabela deve usar a largura de cada intervalo, não só a primeira."""

    def test_reta_em_malha_irregular(self):
        """O trapézio é exato para uma reta, mesmo com intervalos de larguras diferentes."""
        x = np.array([0.0, 1.0, 3.0, 3.5, 6.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2.0 * x + 1.0), 42.0)

    def test_leitura_perdida_no_registro(self):
        """Vazão de 1 L/s com uma leitura perdida (passos de 15 e 30 min) integra 1 L/s·h."""
        t = np.array([0.0, 0.25, 0.75, 1.0])     # falta a leitura de 0,5 h
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.ones(t.size)), 1.0)

    def test_igual_ao_trapezoid_do_numpy(self):
        """Numa malha irregular aleatória, o resultado coincide com np.trapezoid."""
        rng = np.random.default_rng(11)
        x = np.cumsum(rng.uniform(0.1, 1.0, 40))
        y = np.sin(x) + 0.1 * x
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), float(np.trapezoid(y, x)))


if __name__ == "__main__":
    unittest.main()
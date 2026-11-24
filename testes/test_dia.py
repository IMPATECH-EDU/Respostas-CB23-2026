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


class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: o trapézio usava o primeiro passo em toda a malha."""

    def test_malha_irregular_com_reta(self):
        """x = 0, 1, 3 com y = x dá área 4,5 (antes dava 2,5)."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [0.0, 1.0, 3.0]), 4.5)

    def test_lacuna_no_registro(self):
        """Vazão 10 em x = 0, 1, 2, 4 integra 40, apesar da lacuna de 2 a 4."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 2.0, 4.0], [10.0] * 4), 40.0)

    def test_reta_em_malha_aleatoria(self):
        """Em pontos sorteados, a integral de 2x + 1 em [0, 4] é 20."""
        rng = np.random.default_rng(7)
        x = np.sort(np.concatenate(([0.0, 4.0], rng.uniform(0.0, 4.0, 20))))
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2.0 * x + 1.0), 20.0)

    def test_volume_do_dia_com_falhas(self):
        """Vazão constante com 8 leituras perdidas ainda dá 3,6 · 50 · 24 m³."""
        t = np.arange(0.0, 24.0 + 1e-9, 0.25)
        manter = np.setdiff1d(np.arange(t.size), [3, 10, 11, 25, 40, 41, 60, 90])
        volume = 3.6 * Trapezio().integrar_tabela(t[manter], np.full(manter.size, 50.0))
        self.assertAlmostEqual(volume, 3.6 * 50.0 * 24.0)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada
from fornecido.simulador import verdade_dia


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioRegressao(unittest.TestCase):
    """Issue #11: integrar_tabela supunha passo constante. Escritos antes da correção."""

    def test_reta_em_malha_irregular(self):
        """Com passos 1 e 2, o trapézio ainda é exato para a reta 2x + 1: dá 12 em [0, 3]."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [1.0, 3.0, 7.0]), 12.0)

    def test_leitura_perdida_no_meio(self):
        """50 L/s constantes por 1 h, sem a leitura de 0,5 h, integram 50 e não 37,5."""
        t = np.array([0.0, 0.25, 0.75, 1.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.full(4, 50.0)), 50.0)

    def test_volume_do_registro_3487(self):
        """Com as 8 leituras perdidas do registro 3487, o volume fica a menos de 1% da conferência."""
        t, q = vazao_registrada(3487)
        volume = 3.6 * Trapezio().integrar_tabela(t, q)
        self.assertLess(abs(volume / verdade_dia()["volume_m3"] - 1), 0.01)


if __name__ == "__main__":
    unittest.main()

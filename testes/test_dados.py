"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: media_movel deve devolver n - janela + 1 valores, a começar pela 1ª janela."""

    def setUp(self):
        self.rampa = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0, 10.0, 12.0])

    def test_quantidade_de_valores(self):
        """Seis pontos com janela 3 dão 6 - 3 + 1 = 4 médias."""
        self.assertEqual(len(self.rampa.media_movel(3)), 4)

    def test_primeira_janela_presente(self):
        """O primeiro valor é a média de self[0:janela] (2, 4, 6 -> 4)."""
        self.assertTrue(np.allclose(self.rampa.media_movel(3), [4.0, 6.0, 8.0, 10.0]))

    def test_janela_do_tamanho_da_serie(self):
        """Janela igual ao tamanho da série dá um único valor: a média de tudo."""
        resultado = self.rampa.media_movel(len(self.rampa))
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 7.0)

    def test_janela_unitaria_reproduz_a_serie(self):
        """Com janela 1, cada média é o próprio ponto."""
        self.assertTrue(np.allclose(self.rampa.media_movel(1), self.rampa))


if __name__ == "__main__":
    unittest.main()

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


class TestRegressaoMediaMovel(unittest.TestCase):
    """Issue #4: media_movel deve devolver n - janela + 1 valores."""

    def test_tamanho_serie_de_600_janela_30(self):
        """Série de 600 pontos com janela 30 gera 571 médias, como no relato da issue."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_media_usa_os_primeiros_pontos(self):
        """O primeiro valor é a média de self[0:janela], e todos os valores estão presentes."""
        mm = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0]).media_movel(2)
        self.assertTrue(np.allclose(mm, [3.0, 5.0, 7.0]))

    def test_janela_igual_ao_tamanho(self):
        """Com janela igual ao tamanho da série, sai um único valor: a média da série."""
        s = SerieTemporal.de_lista([1.0, 2.0, 6.0])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 3.0)

    def test_janela_1_devolve_a_propria_serie(self):
        """Janela 1 devolve uma cópia com os mesmos valores da série."""
        s = SerieTemporal.de_lista([5.0, -1.0, 2.5])
        self.assertTrue(np.allclose(s.media_movel(1), s))


if __name__ == "__main__":
    unittest.main()

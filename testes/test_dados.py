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
    """Issue #4: media_movel devolvia n - janela valores em vez de n - janela + 1."""

    def test_tamanho_n_menos_janela_mais_um(self):
        """Com 600 pontos e janela 30, a média móvel tem 571 valores."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_janela_incluida(self):
        """O primeiro valor é a média de s[0:janela], e não a de s[1:janela + 1]."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 1.5)

    def test_janela_do_tamanho_da_serie(self):
        """Com janela = len(s), sai um único valor: a média da série inteira."""
        s = SerieTemporal.de_lista([2.0, 4.0, 9.0])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 5.0)


if __name__ == "__main__":
    unittest.main()

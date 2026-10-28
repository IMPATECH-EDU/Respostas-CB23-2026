"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])



import numpy as np
from elevatoria.serie import SerieTemporal


class TestMediaMovelRegressao(unittest.TestCase):
    """Regressões da issue #4, inclusive janelas nas extremidades."""

    def test_primeira_janela_preservada(self) -> None:
        """A primeira média aparece e o resultado tem n - janela + 1 pontos."""
        s = SerieTemporal.de_lista([2, 8, 5, 17])
        resultado = s.media_movel(2)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(np.allclose(resultado, [5, 6.5, 11]))
        self.assertTrue(np.allclose(s, [2, 8, 5, 17]))

    def test_janela_igual_serie(self) -> None:
        """Uma janela que ocupa toda a série produz sua média em um único ponto."""
        resultado = SerieTemporal.de_lista([3, 8, 13]).media_movel(3)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 8.0)

    def test_janela_unitaria(self) -> None:
        """Janela unitária conserva todos os valores, inclusive o primeiro."""
        s = SerieTemporal.de_lista([9, -2, 4])
        resultado = s.media_movel(1)
        self.assertEqual(len(resultado), len(s))
        self.assertTrue(np.allclose(resultado, s))


if __name__ == "__main__":
    unittest.main()

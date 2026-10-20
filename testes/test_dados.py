"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import ler_log, por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: media_movel deve devolver n - janela + 1 valores."""

    def test_quantidade_de_valores(self):
        """600 pontos com janela 30 dão 571 médias (o caso do relato)."""
        s = SerieTemporal.de_lista(np.arange(600))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_media_inclui_o_primeiro_ponto(self):
        """O valor 0 é a média de self[0:janela], incluindo o primeiro ponto."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        self.assertTrue(np.allclose(s.media_movel(2), [1.5, 2.5, 3.5]))

    def test_janela_igual_ao_tamanho(self):
        """Janela igual a len(self) devolve um único valor: a média da série."""
        s = SerieTemporal.de_lista([1.0, 2.0, 6.0])
        r = s.media_movel(3)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(float(r[0]), 3.0)


if __name__ == "__main__":
    unittest.main()

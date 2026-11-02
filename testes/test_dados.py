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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

from elevatoria.serie import SerieTemporal
import numpy as np

class TestSerieTemporalCustom(unittest.TestCase):
    def setUp(self):
        self.s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])

    def test_media_movel_tamanho_e_valores(self):
        mm_2 = self.s.media_movel(2)
        self.assertEqual(len(mm_2), 4)
        self.assertTrue(np.allclose(mm_2, [2.5, 6.5, 12.5, 20.5]))

        mm_3 = self.s.media_movel(3)
        self.assertEqual(len(mm_3), 3)
        self.assertTrue(np.allclose(mm_3, [14/3, 29/3, 50/3]))

    

if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag
from elevatoria.serie import SerieTemporal
import numpy as np


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestIssue4(unittest.TestCase):
    def test_media_movel_funciona(self):
        lista_teste=[1,5,9,7,3] #resultado esperado = [3 7 8 5] com janela = 2
        media = SerieTemporal.de_lista(lista_teste).media_movel(2)
        self.assertEqual(len(media), 4)
        self.assertIsInstance(media, SerieTemporal)
        self.assertTrue(np.allclose(media, [3, 7, 8, 5]))


if __name__ == "__main__":
    unittest.main()

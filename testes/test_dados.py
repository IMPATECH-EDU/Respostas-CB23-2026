"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag
import numpy as np
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])

    def test_tamanho_correto_media_movel(self):
        """Garante que a média móvel de tamanho k retorna exatamente n - k + 1 valores."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        mm = s.media_movel(3)
        # Uma série de 5 elementos com janela 3 deve devolver 3 valores (5 - 3 + 1)
        self.assertEqual(len(mm), 3)

    def test_valores_corretos_media_movel(self):
        """Verifica se os valores da média móvel estão corretos, não omitindo a primeira janela."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        mm = s.media_movel(2)
        esperado = [15.0, 25.0, 35.0]
        # O código atual com defeito devolve apenas [25.0, 35.0] e falhará aqui
        self.assertTrue(np.allclose(mm, esperado))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

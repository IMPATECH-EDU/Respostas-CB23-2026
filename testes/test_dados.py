"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestMediaMovelRegrassao(unittest.TestCase):
    def test_tamanho(self):
        # Estamos fazendo o numero de pontos menos o numero da janela mais um para criar a media movel
        s = SerieTemporal.de_lista(range(10))
        self.assertEqual(len(s.media_movel(3)),8)

    def test_primeiro_valor(self):
        # Pegamos o primeiro valor para ser a media de s ate o tamanho da janela [0:janela]
        s = SerieTemporal.de_lista([1,2,3,4,5])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 1.5)

    def test_janela_max(self):
        # Fazemos a janela = len(s)
        s = SerieTemporal.de_lista([2,4,6])
        mm = s.media_movel(3)
        self.assertEqual(len(mm),1)
        self.assertAlmostEqual(float(mm[0]), 4.0)

if __name__ == "__main__":
    unittest.main()

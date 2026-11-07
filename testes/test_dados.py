"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import numpy as np
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
class TestRegressaoMediaMovel(unittest.TestCase):
    """Testes de regressão da issue #4 (média móvel)."""

    def test_media_movel_janela_2(self):
        """Verifica se a média móvel de 30 pontos retorna 30 - janela + 1 valores"""
        dados = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0, 50.0])
        janela = 2
        resultado = dados.media_movel(janela)
        self.assertEqual(len(resultado), len(dados) - janela + 1)
    def test_media_movel_janela_1(self):
        """Verifica se a média móvel de janela 1 retorna a própria série"""
        dados = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0, 50.0])
        janela = 1
        resultado = dados.media_movel(janela)

        # Verifica se os vetores são do mesmo tamanho
        self.assertEqual(len(resultado), len(dados))
        
        # Verifica se o resultado é igual à série original
        self.assertTrue(np.allclose(resultado, dados))
if __name__ == "__main__":
    unittest.main()

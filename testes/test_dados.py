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

class TestRegressaoIssue4(unittest.TestCase):
    """Testes de regresssão para a Issue #4 (media_movel)"""

    def test_media_movel_tamanho_retornado(self):
        """Para N=5 e janela w=3, media_movel deve retornar 3 elementos (5 - 3 + 1)."""
        serie = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        resultado = serie.media_movel(3)
        self.assertEqual(len(resultado), 3)

    def test_media_movel_valores_janela_2(self):
        """Média móvel de janela 2 em [10, 20, 30] deve retornar [15, 25] com tamanho 2."""
        serie = SerieTemporal.de_lista([10.0, 20.0, 30.0])
        resultado = serie.media_movel(2)
        esperado = np.array([15.0, 25.0])
        self.assertTrue(np.allclose(resultado, esperado))

class TestReamostrar(unittest.TestCase):
    def test_medias_dos_blocos(self):
        """Calcula a media correta de cada bloco"""
        serie = SerieTemporal.de_lista([1,2,3,4,5,6])

        resultado = serie.reamostrar(2)

        esperado = [1.5,3.5,5.5]
        self.assertTrue(np.allclose(resultado, esperado))

    def test_descartar_sobra_final(self):
        """Descarta a parte que sobrou na divisão inteira"""
        serie = SerieTemporal.de_lista([1,2,3,4,5,6,100])

        resultado = serie.reamostrar(3)

        esperado = [2.0,5.0]
        self.assertTrue(np.allclose(resultado,esperado))
        self.assertEqual(len(resultado), 2)

if __name__ == "__main__":
    unittest.main()

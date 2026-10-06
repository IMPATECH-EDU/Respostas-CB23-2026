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

class TestReamostrarSerie(unittest.TestCase):
    """Testes para o método reamostrar e descarte de sobras (Issue #5)."""

    def test_descarte_de_sobra_no_fim(self):
        """Garante que os pontos excedentes no final da série que não formam um bloco são descartados."""
        s = SerieTemporal.de_lista([1.0, 3.0, 5.0, 7.0, 9.0])
        r = s.reamostrar(2)
        # Com k=2, forma os blocos [1, 3] -> 2.0 e [5, 7] -> 6.0. O valor 9.0 é descartado.
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 6.0]))

    def test_retorno_exato_sem_sobras_e_tipo(self):
        """Verifica o cálculo exato sem sobras e atesta que o retorno é do tipo SerieTemporal."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        r = s.reamostrar(2)
        
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(r, [15.0, 35.0]))


if __name__ == "__main__":
    unittest.main()

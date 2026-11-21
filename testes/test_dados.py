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

# Testes - Média móvel (Issue #4)

class TestMediaMovel(unittest.TestCase):
    def test_media_movel_simples(self):
        """Regressão #4: verifica tamanho (n - janela + 1), valores, tipo e imutabilidade."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        copia = s.copy()
        resultado = s.media_movel(3)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(len(resultado), 3)
        np.testing.assert_allclose(resultado, [2.0, 3.0, 4.0])
        np.testing.assert_allclose(s, copia)

    def test_media_movel_janela_unitaria(self):
        """Janela igual a 1 devolve cópia com os mesmos valores da série."""
        x = SerieTemporal.de_lista([3.0, 5.0, 7.0])
        resultado = x.media_movel(1)
        self.assertIsInstance(resultado, SerieTemporal)
        np.testing.assert_allclose(resultado, [3.0, 5.0, 7.0])

    def test_media_movel_janela_total(self):
        """Janela igual ao tamanho da série devolve um único elemento com a média geral."""
        x = SerieTemporal.de_lista([2.0, 4.0, 6.0])
        resultado = x.media_movel(3)
        self.assertEqual(len(resultado), 1)
        np.testing.assert_allclose(resultado, [4.0])

    def test_media_movel_janela_invalida(self):
        """Janela menor que 1 ou maior que o tamanho da série levanta ValueError."""
        x = SerieTemporal.de_lista([3.0, 5.0])
        with self.assertRaises(ValueError):
            x.media_movel(0)
        with self.assertRaises(ValueError):
            x.media_movel(3)


# Testes - Reamostragem por bloco (Issue #5)

class TestReamostrar(unittest.TestCase):
    def test_reamostrar_blocos_exatos(self):
        """Série divisível por k devolve médias exatas de cada bloco sem alterar self."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0, 50.0, 60.0])
        copia = s.copy()
        resultado = s.reamostrar(2)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(len(resultado), 3)
        np.testing.assert_allclose(resultado, [15.0, 35.0, 55.0])
        np.testing.assert_allclose(s, copia)

    def test_reamostrar_com_sobra_no_fim(self):
        """Pontos excedentes ao final que não formam um bloco completo de tamanho k são descartados."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 100.0, 200.0])
        resultado = s.reamostrar(3)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(len(resultado), 2)
        np.testing.assert_allclose(resultado, [2.0, 5.0])

    def test_reamostrar_bloco_unitario(self):
        """Bloco k=1 preserva todos os elementos da série como SerieTemporal."""
        s = SerieTemporal.de_lista([4.0, 8.0, 12.0])
        resultado = s.reamostrar(1)
        self.assertIsInstance(resultado, SerieTemporal)
        np.testing.assert_allclose(resultado, [4.0, 8.0, 12.0])

    def test_reamostrar_k_invalido(self):
        """Tamanho de bloco k < 1 ou k > len(self) levanta ValueError."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            s.reamostrar(0)
        with self.assertRaises(ValueError):
            s.reamostrar(4)


if __name__ == "__main__":
    unittest.main()

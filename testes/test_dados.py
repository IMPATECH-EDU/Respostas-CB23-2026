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


class TestRegressaoMediaMovel(unittest.TestCase):
    """Issue #4: media_movel deve devolver n - janela + 1 valores."""

    def test_tamanho_serie_de_600_janela_30(self):
        """Série de 600 pontos com janela 30 gera 571 médias, como no relato da issue."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_media_usa_os_primeiros_pontos(self):
        """O primeiro valor é a média de self[0:janela], e todos os valores estão presentes."""
        mm = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0]).media_movel(2)
        self.assertTrue(np.allclose(mm, [3.0, 5.0, 7.0]))

    def test_janela_igual_ao_tamanho(self):
        """Com janela igual ao tamanho da série, sai um único valor: a média da série."""
        s = SerieTemporal.de_lista([1.0, 2.0, 6.0])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 3.0)

    def test_janela_1_devolve_a_propria_serie(self):
        """Janela 1 devolve uma cópia com os mesmos valores da série."""
        s = SerieTemporal.de_lista([5.0, -1.0, 2.5])
        self.assertTrue(np.allclose(s.media_movel(1), s))


class TestReamostrarBlocos(unittest.TestCase):
    """Issue #5: SerieTemporal.reamostrar."""

    def test_sobra_no_fim_e_descartada(self):
        """Os len % k pontos finais que não fecham um bloco são descartados."""
        r = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7, 100]).reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_igual_ao_tamanho(self):
        """Com k igual ao tamanho, sai um único bloco com a média da série."""
        r = SerieTemporal.de_lista([1.0, 2.0, 3.0, 10.0]).reamostrar(4)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(r, [4.0]))

    def test_nao_modifica_a_serie(self):
        """reamostrar não altera os valores nem o tamanho da série original."""
        s = SerieTemporal.de_lista([3.0, 1.0, 4.0, 1.0, 5.0])
        copia = np.array(s)
        s.reamostrar(2)
        self.assertTrue(np.array_equal(s, copia))


class TestContratoLerLog(unittest.TestCase):
    """Issue #1: regras de ler_log que os testes de aceitação não verificam."""

    def test_linhas_em_branco_nao_contam_como_invalidas(self):
        """Linhas vazias ou só com espaços são ignoradas, sem ir para as inválidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=10\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_impossivel_e_invalida(self):
        """Uma linha com mês 13 casa com o padrão, mas é descartada como inválida."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=10"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_hora_impossivel_e_invalida(self):
        """Uma linha com hora 25 é descartada como inválida."""
        linha = "2026-10-05 25:00:00 INFO PT101 contagens=10"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_resto_sem_pares_e_invalido(self):
        """Uma linha cujo resto não tem nenhum par chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 WARN B1 sem pares aqui"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_varios_espacos_entre_as_partes(self):
        """As partes podem ser separadas por mais de um espaço."""
        registros, invalidas = ler_log("2026-10-05  08:00:00   INFO  FT201  pulsos=3873")
        self.assertEqual(invalidas, [])
        self.assertEqual(registros[0].tag, "FT201")
        self.assertAlmostEqual(registros[0].valores["pulsos"], 3873.0)


if __name__ == "__main__":
    unittest.main()

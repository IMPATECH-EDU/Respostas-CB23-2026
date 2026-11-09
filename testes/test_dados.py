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


class TestRegressaoIssue4(unittest.TestCase):
    """Testes de regressão para a issue #4 (defeito em media_movel)."""

    def test_media_movel_tamanho(self):
        """Média móvel de N pontos com janela J deve conter exatamente N - J + 1 elementos."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0, 50.0])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 3)

    def test_media_movel_primeiro_ponto_e_valores(self):
        """Primeiro ponto da média móvel deve ser a média exata dos primeiros pontos da janela."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        mm = s.media_movel(2)
        esperado = np.array([1.5, 2.5, 3.5, 4.5])
        self.assertTrue(np.allclose(mm, esperado))

    def test_media_movel_janela_igual_tamanho(self):
        """Média móvel com janela igual ao tamanho da série deve devolver exatamente um elemento."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 4.0)


class TestReamostrar(unittest.TestCase):
    """Testes para o método reamostrar da issue #5."""

    def test_reamostrar_com_sobra_descartada(self):
        """Reamostragem descarta os pontos finais excedentes que não formam um bloco completo."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
        res = s.reamostrar(3)
        self.assertEqual(len(res), 2)

    def test_reamostrar_valores_medias_blocos(self):
        """Reamostragem calcula corretamente a média de cada bloco consecutivo de tamanho k."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        res = s.reamostrar(2)
        self.assertTrue(np.allclose(res, [15.0, 35.0]))

    def test_reamostrar_k_igual_tamanho(self):
        """Reamostragem com k igual ao tamanho da série devolve apenas um valor com a média total."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0])
        res = s.reamostrar(3)
        self.assertEqual(len(res), 1)
        self.assertAlmostEqual(float(res[0]), 20.0)


class TestLerLogContrato(unittest.TestCase):
    """Testes para regras do contrato de ler_log."""

    def test_ler_log_ignora_linhas_em_branco_e_espacos(self):
        """Linhas vazias ou apenas com espaços não contam como linhas inválidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=100\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(len(invalidas), 0)

    def test_ler_log_data_invalida_vai_para_invalidas(self):
        """Linhas com data impossível são descartadas e adicionadas à lista de inválidas."""
        texto = "2026-13-45 08:00:00 INFO PT101 contagens=100\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

    def test_ler_log_resto_sem_chave_valor_vai_para_invalidas(self):
        """Linha sem nenhum par chave=valor no resto é descartada como inválida."""
        texto = "2026-10-05 08:00:00 INFO PT101 texto_sem_igual\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)


if __name__ == "__main__":
    unittest.main()

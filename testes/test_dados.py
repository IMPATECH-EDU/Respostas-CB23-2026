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

from elevatoria import dados
from elevatoria.serie import SerieTemporal
import numpy as np


class TestSerieTemporalCustom(unittest.TestCase):
    """Casos adicionais para a série temporal."""

    def setUp(self):
        self.s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])

    def test_media_movel_tamanho_e_valores(self):
        """Cobre tamanhos e valores da média móvel para duas janelas."""
        mm_2 = self.s.media_movel(2)
        self.assertEqual(len(mm_2), 4)
        self.assertTrue(np.allclose(mm_2, [2.5, 6.5, 12.5, 20.5]))

        mm_3 = self.s.media_movel(3)
        self.assertEqual(len(mm_3), 3)
        self.assertTrue(np.allclose(mm_3, [14/3, 29/3, 50/3]))

    def test_media_movel_regressao_tamanho_esperado(self):
        """Cobre o número correto de janelas de uma série longa."""
        serie = SerieTemporal.de_lista(np.arange(600, dtype=float))
        resultado = serie.media_movel(30)
        self.assertEqual(len(resultado), 571)
        self.assertIsInstance(resultado, SerieTemporal)

    def test_media_movel_regressao_janela_um(self):
        """Cobre a média móvel com janela unitária sem perda de pontos."""
        resultado = self.s.media_movel(1)
        self.assertEqual(len(resultado), len(self.s))
        self.assertTrue(np.allclose(resultado, self.s))

    def test_reamostrar_descarta_sobra_no_fim(self):
        """Cobre a sobra final que não forma um bloco completo."""
        serie = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        resultado = serie.reamostrar(2)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertTrue(np.allclose(resultado, [1.5, 3.5]))
        self.assertTrue(np.array_equal(serie, [1, 2, 3, 4, 5]))

    def test_reamostrar_serie_inteira_em_um_bloco(self):
        """Cobre uma reamostragem cujo bloco ocupa toda a série."""
        resultado = SerieTemporal.de_lista([2, 4, 6, 8]).reamostrar(4)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 5.0)


class TestLerLogContratosNaoCobertos(unittest.TestCase):
    """Casos do leitor de log não cobertos pelos testes de aceitação."""

    def test_ler_log_ignora_linhas_em_branco(self):
        """Cobre linhas vazias e com espaços, que não são registradas como inválidas."""
        texto = "  \n\t\n2026-10-05 08:00:00 INFO B1 evento=partida\n   \n"
        registros, invalidas = dados.ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_ler_log_rejeita_data_impossivel(self):
        """Cobre uma linha estruturada cuja data não existe no calendário."""
        linha = "2026-13-05 08:00:00 INFO PT102 contagens=1789"
        registros, invalidas = dados.ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_ler_log_rejeita_resto_sem_pares_chave_valor(self):
        """Cobre texto no campo resto que não contém nenhum par chave=valor."""
        linha = "2026-10-05 08:00:00 INFO PT102 sem_dados"
        registros, invalidas = dados.ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

if __name__ == "__main__":
    unittest.main()

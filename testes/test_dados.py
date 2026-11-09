"""Testes do Marco 1"""

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
    """Issue #4: media_movel deve devolver `n - janela + 1` valores, começando na janela 0."""

    def test_quantidade_de_valores(self):
        """Série de 600 pontos com janela 30 devolve 571 valores (o defeito dava 570)."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeiro_valor_e_media_da_primeira_janela(self):
        """O primeiro valor é a média de self[0:janela], que o defeito omitia."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0, 10.0])
        mm = s.media_movel(2)
        self.assertEqual(len(mm), 4)
        self.assertAlmostEqual(float(mm[0]), 3.0)

    def test_valores_conferem_com_media_direta(self):
        """Todos os valores coincidem com a média calculada janela a janela."""
        s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0, 36.0])
        esperado = [s[i:i + 3].mean() for i in range(len(s) - 3 + 1)]
        self.assertTrue(np.allclose(s.media_movel(3), esperado))

    def test_janela_igual_ao_tamanho(self):
        """Janela do tamanho da série devolve um único valor: a média de tudo."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        mm = s.media_movel(4)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 2.5)

    def test_janela_um_devolve_a_propria_serie(self):
        """Janela 1 devolve n valores iguais aos da série original."""
        s = SerieTemporal.de_lista([5.0, 7.0, 9.0])
        self.assertTrue(np.allclose(s.media_movel(1), [5.0, 7.0, 9.0]))


class TestReamostrar(unittest.TestCase):
    """Issue #5: médias por bloco com SerieTemporal.reamostrar."""

    def test_sobra_no_fim_e_descartada(self):
        """Com 7 pontos e k=3 há 2 blocos; o ponto que sobra no fim não entra."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 100.0])
        r = s.reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_igual_ao_tamanho(self):
        """Com k igual a len(self) há um só bloco: a média de toda a série."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        r = s.reamostrar(4)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(float(r[0]), 2.5)

    def test_k_um_devolve_a_propria_serie(self):
        """Com k=1 cada ponto é um bloco, e o resultado tem os mesmos valores."""
        s = SerieTemporal.de_lista([3.0, 1.0, 2.0])
        self.assertTrue(np.allclose(s.reamostrar(1), [3.0, 1.0, 2.0]))

    def test_nao_modifica_self_e_mantem_tipo(self):
        """reamostrar não altera a série original e devolve uma SerieTemporal 1D."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        copia = np.array(s)
        r = s.reamostrar(2)
        self.assertTrue(np.array_equal(s, copia))
        self.assertIsInstance(r, SerieTemporal)
        self.assertEqual(r.ndim, 1)

class TestContratoLerLog(unittest.TestCase):
    """Regras do contrato de ler_log que os testes de aceitação não verificam."""

    def test_linhas_vazias_sao_ignoradas_e_nao_contam_como_invalidas(self):
        """Linhas vazias ou só com espaços não viram registro nem entram em `invalidas`."""
        texto = ("\n"
                 "2026-10-05 08:00:00 INFO PT101 contagens=131\n"
                 "   \n"
                 "2026-10-05 08:00:06 INFO PT101 contagens=140\n")
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 2)
        self.assertEqual(invalidas, [])

    def test_data_impossivel_e_resto_sem_par_sao_invalidos(self):
        """Mês 13 e `resto` sem nenhum chave=valor são devolvidos como inválidos, intactos."""
        mes_13 = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        sem_par = "2026-10-05 08:00:00 INFO PT101 semdados"
        valida = "2026-10-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log("\n".join([mes_13, valida, sem_par]))
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [mes_13, sem_par])

    def test_varios_pares_na_mesma_linha(self):
        """Uma linha com vários pares guarda todos, números como float e o resto como str."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5")
        self.assertEqual(registros[0].valores, {"evento": "partida", "corrente": 47.5})


if __name__ == "__main__":
    unittest.main()
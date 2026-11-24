"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import (converter_vetorizado, ler_log, medir_memoria, medir_tempos,
                              por_tag, serie, valida_tag)
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestRegressaoMediaMovel(unittest.TestCase):
    """Issue #4: a média móvel perdia a primeira janela."""

    def test_tamanho_da_serie_do_relato(self):
        """600 pontos e janela 30 dão 571 valores (antes dava 570)."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_janela_esta_presente(self):
        """O primeiro valor é a média dos primeiros pontos da janela."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0])
        resultado = s.media_movel(2)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(np.allclose(resultado, [3.0, 5.0, 7.0]))

    def test_janela_igual_ao_tamanho(self):
        """Janela igual ao tamanho da série dá um valor só, a média de tudo."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 6.0])
        resultado = s.media_movel(4)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 3.0)

    def test_janela_um_devolve_a_propria_serie(self):
        """Janela 1 devolve a própria série."""
        s = SerieTemporal.de_lista([5.0, -1.0, 3.5])
        resultado = s.media_movel(1)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(np.allclose(resultado, [5.0, -1.0, 3.5]))


class TestContratoLerLog(unittest.TestCase):
    """Regras de ler_log que a aceitação não cobre."""

    VALIDA = "2026-10-05 08:00:00 INFO PT101 contagens=131"

    def test_linhas_vazias_nao_sao_invalidas(self):
        """Linhas vazias ou só com espaços são ignoradas, não contam como inválidas."""
        registros, invalidas = ler_log(f"\n   \n{self.VALIDA}\n\t\n")
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_impossivel_e_invalida(self):
        """Mês 13 deixa a linha inválida, e ela volta sem alteração."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(f"{linha}\n{self.VALIDA}")
        self.assertEqual(invalidas, [linha])
        self.assertEqual(len(registros), 1)

    def test_hora_impossivel_e_invalida(self):
        """Hora 25 também é descartada."""
        linha = "2026-10-05 25:00:00 INFO PT101 contagens=131"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Sem nenhum par chave=valor, a linha é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT101 sem pares aqui"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_final_de_linha_do_windows(self):
        """Final de linha \\r\\n não deixa o \\r no valor."""
        registros, invalidas = ler_log(f"{self.VALIDA}\r\n{self.VALIDA}\r\n")
        self.assertEqual((len(registros), invalidas), (2, []))
        self.assertEqual(registros[0].valores, {"contagens": 131.0})

    def test_valor_com_ponto_decimal_vira_float(self):
        """Número vira float e 'partida' continua str."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5")
        self.assertAlmostEqual(registros[0].valores["corrente"], 47.5)
        self.assertEqual(registros[0].valores["evento"], "partida")

    def test_tag_valida_so_com_a_string_inteira(self):
        """valida_tag rejeita tag seguida de quebra de linha."""
        self.assertTrue(valida_tag("B1"))
        self.assertFalse(valida_tag("B1\n"))


class TestSerieDoLog(unittest.TestCase):
    """Função `serie`."""

    TEXTO = ("2026-10-05 08:00:00 INFO PT102 contagens=10\n"
             "2026-10-05 08:00:06 ALARME PT102 evento=pressao_alta limite=2000\n"
             "2026-10-05 08:00:12 INFO PT102 contagens=12\n")

    def test_chave_de_texto_levanta_erro(self):
        """Chave de texto (evento) levanta ValueError."""
        registros, _ = ler_log(self.TEXTO)
        with self.assertRaises(ValueError):
            serie(registros, "PT102", "evento")

    def test_tag_sem_registros_da_serie_vazia(self):
        """Tag ausente do log dá série vazia."""
        registros, _ = ler_log(self.TEXTO)
        self.assertEqual(len(serie(registros, "PT101", "contagens")), 0)


class TestMemoriaETempos(unittest.TestCase):
    """Issue #3: casos extras de memória e conversão."""

    def test_tipo_nao_inteiro_levanta_erro(self):
        """medir_memoria rejeita array de float."""
        with self.assertRaises(ValueError):
            medir_memoria(np.array([1.0, 2.0]))

    def test_valor_fora_de_16_bits_levanta_erro(self):
        """Contagem acima de 65535 não cabe em uint16."""
        with self.assertRaises(ValueError):
            medir_memoria(np.array([70000]))

    def test_lista_cresce_com_o_tamanho(self):
        """A lista ocupa mais memória que qualquer ndarray."""
        m = medir_memoria(np.arange(1000) % 4096)
        self.assertGreater(m["list"], m["float64"])

    def test_vetorizado_nao_estoura_em_uint16(self):
        """Com uint16, 4095 contagens ainda dão 600 kPa (sem overflow)."""
        resultado = converter_vetorizado(np.array([4095], dtype=np.uint16))
        self.assertAlmostEqual(float(resultado[0]), 600.0)

    def test_k_invalido_em_medir_tempos(self):
        """medir_tempos repassa o ValueError de k inválido."""
        with self.assertRaises(ValueError):
            medir_tempos(np.arange(10), k=0)


if __name__ == "__main__":
    unittest.main()

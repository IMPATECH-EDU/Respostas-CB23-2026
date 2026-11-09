"""Testes de aceitação do Marco 1 (código fornecido; NÃO ALTERE).

Estes testes conferem o contrato público de `elevatoria/dados.py` e `elevatoria/serie.py`.
Passar em todos eles é necessário, mas não basta: eles não cobrem todos os casos (veja a
issue #4). Os seus próprios testes ficam em `testes/`.
"""
import dataclasses
import re
import unittest

import numpy as np

from elevatoria import dados
from elevatoria.serie import SerieTemporal

TEXTO_PEQUENO = (
    "2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5\n"
    "2026-10-05 08:00:00 INFO PT102 contagens=1623\n"
    "### falha de comunicacao com a RTU ###\n"
    "2026-10-05 08:00:06 ALARME PT102 evento=pressao_alta limite=2000\n"
)


class TestPadraoLinha(unittest.TestCase):
    """Issue #1: o padrão LINHA."""

    def test_e_padrao_compilado_verbose(self):
        self.assertIsInstance(dados.LINHA, re.Pattern, "LINHA deve ser um padrão compilado")
        self.assertTrue(dados.LINHA.flags & re.VERBOSE, "LINHA deve usar re.VERBOSE")

    def test_grupos_nomeados(self):
        self.assertEqual(set(dados.LINHA.groupindex), {"data", "hora", "nivel", "tag", "resto"})

    def test_casa_linha_valida(self):
        m = dados.LINHA.fullmatch("2026-10-05 08:00:00 INFO PT102 contagens=1789")
        self.assertIsNotNone(m)
        self.assertEqual((m["data"], m["hora"], m["nivel"], m["tag"], m["resto"]),
                         ("2026-10-05", "08:00:00", "INFO", "PT102", "contagens=1789"))

    def test_rejeita_linhas_corrompidas(self):
        for linha in ["### falha de comunicacao com a RTU ###", "2026-10-05 08:20:4",
                      "2026-10-05 08:00:00 DEBUG PT102 contagens=1789"]:
            with self.subTest(linha=linha):
                self.assertIsNone(dados.LINHA.fullmatch(linha))


class TestValidaTag(unittest.TestCase):
    """Issue #1: valida_tag."""

    def test_validas(self):
        for tag in ["PT101", "FT201", "B1"]:
            with self.subTest(tag=tag):
                self.assertTrue(dados.valida_tag(tag))

    def test_invalidas(self):
        for tag in ["pt101", "PT", "PT1010", "101PT", "PT101 "]:
            with self.subTest(tag=tag):
                self.assertFalse(dados.valida_tag(tag))


class TestLerLog(unittest.TestCase):
    """Issue #1: ler_log."""

    def test_texto_pequeno(self):
        registros, invalidas = dados.ler_log(TEXTO_PEQUENO)
        self.assertEqual(len(registros), 3)
        self.assertEqual(invalidas, ["### falha de comunicacao com a RTU ###"])
        self.assertEqual([r.tag for r in registros], ["B1", "PT102", "PT102"])

    def test_tipos_dos_valores(self):
        registros, _ = dados.ler_log(TEXTO_PEQUENO)
        self.assertEqual(registros[1].valores, {"contagens": 1623.0})
        self.assertIsInstance(registros[1].valores["contagens"], float)
        self.assertEqual(registros[0].valores["evento"], "partida")
        self.assertEqual(registros[2].nivel, "ALARME")

    def test_instante(self):
        registros, _ = dados.ler_log(TEXTO_PEQUENO)
        self.assertEqual(registros[2].instante.strftime("%Y-%m-%d %H:%M:%S"),
                         "2026-10-05 08:00:06")

    def test_texto_vazio(self):
        self.assertEqual(dados.ler_log(""), ([], []))

    def test_registro_imutavel(self):
        registros, _ = dados.ler_log(TEXTO_PEQUENO)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            registros[0].tag = "PT101"


class TestContagemESerie(unittest.TestCase):
    """Issue #1: contagem_por_tag e serie."""

    def test_contagem_por_tag(self):
        registros, _ = dados.ler_log(TEXTO_PEQUENO)
        self.assertEqual(dados.contagem_por_tag(registros), {"B1": 1, "PT102": 2})
        self.assertEqual(dados.contagem_por_tag([]), {})

    def test_serie_ignora_registros_sem_a_chave(self):
        registros, _ = dados.ler_log(TEXTO_PEQUENO)
        s = dados.serie(registros, "PT102", "contagens")
        self.assertIsInstance(s, SerieTemporal)
        self.assertTrue(np.array_equal(s, [1623.0]))


class TestConversores(unittest.TestCase):
    """Issue #2: criar_conversores."""

    def test_cada_tag_usa_o_seu_fator(self):
        conv = dados.criar_conversores({"A1": 1.0, "B2": 2.0, "C3": 3.0})
        self.assertEqual(set(conv), {"A1", "B2", "C3"})
        for tag, esperado in [("A1", 10.0), ("B2", 20.0), ("C3", 30.0)]:
            with self.subTest(tag=tag):
                self.assertAlmostEqual(conv[tag](10.0), esperado)


class TestMemoriaETempo(unittest.TestCase):
    """Issue #3: medir_memoria, converter_* e medir_tempos."""

    def setUp(self):
        self.contagens = np.arange(1000) % 4096

    def test_chaves_e_tamanhos(self):
        m = dados.medir_memoria(self.contagens)
        self.assertEqual(set(m), {"list", "array('H')", "uint16", "int32", "int64",
                                  "float32", "float64"})
        self.assertEqual(m["uint16"], 2 * 1000)
        self.assertEqual(m["float64"], 8 * 1000)
        self.assertEqual(m["array('H')"], 2 * 1000)
        self.assertGreater(m["list"], m["int64"])

    def test_memoria_rejeita_2d(self):
        with self.assertRaises(ValueError):
            dados.medir_memoria(np.zeros((2, 2), dtype=int))

    def test_conversoes_equivalentes(self):
        lista = [0, 2048, 4095]
        esperado = [c * 600 / 4095 for c in lista]
        for f in [dados.converter_laco, dados.converter_compreensao, dados.converter_map]:
            with self.subTest(funcao=f.__name__):
                self.assertTrue(np.allclose(f(lista), esperado))
        self.assertTrue(np.allclose(dados.converter_vetorizado(np.array(lista)), esperado))

    def test_medir_tempos(self):
        tempos = dados.medir_tempos(self.contagens, k=2)
        self.assertEqual(set(tempos), {"laço", "compreensão", "map+lambda", "vetorizado"})
        for metodo, t in tempos.items():
            with self.subTest(metodo=metodo):
                self.assertGreater(t, 0.0)


class TestSerieTemporal(unittest.TestCase):
    """Código existente de elevatoria/serie.py (contrato da classe)."""

    def setUp(self):
        self.s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])

    def test_de_lista(self):
        self.assertIsInstance(self.s, SerieTemporal)
        self.assertEqual(self.s.dtype, np.float64)
        with self.assertRaises(ValueError):
            SerieTemporal.de_lista([[1, 2], [3, 4]])

    def test_media_movel_tipo_e_erros(self):
        self.assertIsInstance(self.s.media_movel(2), SerieTemporal)
        for janela in [0, 6]:
            with self.subTest(janela=janela), self.assertRaises(ValueError):
                self.s.media_movel(janela)

    def test_variacao_e_amplitude(self):
        self.assertTrue(np.allclose(self.s.variacao(), [3, 5, 7, 9]))
        self.assertIsInstance(self.s.amplitude(), float)
        self.assertAlmostEqual(self.s.amplitude(), 24.0)

    def test_normalizar(self):
        z = self.s.normalizar()
        self.assertAlmostEqual(float(z.mean()), 0.0)
        self.assertAlmostEqual(float(z.std(ddof=1)), 1.0)
        with self.assertRaises(ValueError):
            SerieTemporal.de_lista([2.0, 2.0, 2.0]).normalizar()

    def test_fatia_e_imutabilidade(self):
        self.assertIsInstance(self.s[1:], SerieTemporal)
        copia = np.array(self.s)
        self.s.media_movel(2)
        self.s.normalizar()
        self.assertTrue(np.array_equal(self.s, copia))


class TestReamostrar(unittest.TestCase):
    """Issue #5: SerieTemporal.reamostrar."""

    def test_blocos(self):
        r = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6]).reamostrar(2)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(r, [1.5, 3.5, 5.5]))

    def test_k_invalido(self):
        s = SerieTemporal.de_lista([1, 2, 3])
        for k in [0, 4]:
            with self.subTest(k=k), self.assertRaises(ValueError):
                s.reamostrar(k)


if __name__ == "__main__":
    unittest.main()

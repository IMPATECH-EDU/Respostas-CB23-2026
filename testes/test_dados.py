"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import sys
import unittest

import numpy as np

from elevatoria.dados import (converter_compreensao, converter_laco, converter_map,
                              converter_vetorizado, criar_conversores, ler_log,
                              medir_memoria, medir_tempos, por_tag, serie)
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestMediaMovelRegressao(unittest.TestCase):
    """Regressões da Issue #4, escritas antes da correção de media_movel."""

    def test_media_movel_inclui_primeira_janela(self) -> None:
        """Janela de dois pontos inclui a primeira janela e todas as médias esperadas."""
        s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])
        resultado = s.media_movel(2)
        esperado = [2.5, 6.5, 12.5, 20.5]
        self.assertEqual(resultado.shape, (4,),
                         f"Esperado {esperado}; recebido {resultado.tolist()}")
        self.assertTrue(np.allclose(resultado, esperado))

    def test_media_movel_janela_igual_ao_tamanho(self) -> None:
        """Janela igual ao tamanho da série produz um único valor com a média total."""
        s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])
        resultado = s.media_movel(5)
        self.assertEqual(resultado.shape, (1,),
                         f"Esperado [11.0]; recebido {resultado.tolist()}")
        self.assertAlmostEqual(float(resultado[0]), 11.0)


class TestLerLogContrato(unittest.TestCase):
    """Regras de leitura não verificadas pelos testes de aceitação."""

    def test_ignora_linhas_em_branco(self) -> None:
        """Linhas vazias ou só com espaços não entram nos registros nem nas inválidas."""
        registros, invalidas = ler_log("\n   \n\t\n")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [])

    def test_descarta_datas_e_horas_impossiveis(self) -> None:
        """Datas e horas impossíveis são descartadas mesmo com formato correto."""
        for instante in ["2026-13-05 08:00:00", "2026-02-30 08:00:00",
                         "2026-10-05 24:00:00", "2026-10-05 08:60:00"]:
            with self.subTest(instante=instante):
                linha = f"{instante} INFO PT102 contagens=10"
                registros, invalidas = ler_log(linha)
                self.assertEqual(registros, [])
                self.assertEqual(invalidas, [linha])

    def test_descarta_linhas_sem_pares(self) -> None:
        """Uma linha sem nenhum par chave=valor é inválida."""
        for resto in ["sem pares", "contagens=", "   "]:
            with self.subTest(resto=resto):
                linha = f"2026-10-05 08:00:00 INFO PT102 {resto}"
                registros, invalidas = ler_log(linha)
                self.assertEqual(registros, [])
                self.assertEqual(invalidas, [linha])

    def test_preserva_linhas_invalidas_sem_strip(self) -> None:
        """Linhas inválidas mantêm seus espaços e a ordem original."""
        linhas = ["  falha de comunicacao  ",
                  "2026-10-05 08:00:00 DEBUG PT102 contagens=10  "]
        registros, invalidas = ler_log("\n".join(linhas))
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, linhas)


class TestSerieContrato(unittest.TestCase):
    """Seleção dos valores numéricos para uma série temporal."""

    def test_preserva_ordem_e_filtra_tag_e_chave(self) -> None:
        """A série preserva a ordem de entrada e ignora outras tags e chaves ausentes."""
        registros, _ = ler_log(
            "2026-10-05 08:00:06 INFO PT102 contagens=20\n"
            "2026-10-05 08:00:00 INFO PT101 contagens=999\n"
            "2026-10-05 08:00:00 ALARME PT102 evento=pressao_alta\n"
            "2026-10-05 08:00:00 INFO PT102 contagens=10\n"
        )
        resultado = serie(registros, "PT102", "contagens")
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertTrue(np.allclose(resultado, [20.0, 10.0]))

    def test_sem_valores_produz_serie_vazia(self) -> None:
        """Sem registros correspondentes, o retorno continua sendo uma SerieTemporal vazia."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO PT102 evento=partida")
        for tag, chave in [("PT101", "contagens"), ("PT102", "contagens")]:
            with self.subTest(tag=tag, chave=chave):
                resultado = serie(registros, tag, chave)
                self.assertIsInstance(resultado, SerieTemporal)
                self.assertEqual(resultado.size, 0)


class TestConversoresContrato(unittest.TestCase):
    """Conversores com fatores próprios, incluindo os casos limite do dicionário."""

    def test_fatores_zero_negativo_e_fracionario(self) -> None:
        """Cada lambda preserva seu fator, inclusive zero, negativo e fracionário."""
        conversores = criar_conversores({"A1": 0.0, "B2": -2.0, "C3": 0.5})
        self.assertEqual(set(conversores), {"A1", "B2", "C3"})
        self.assertAlmostEqual(conversores["A1"](4.0), 0.0)
        self.assertAlmostEqual(conversores["B2"](4.0), -8.0)
        self.assertAlmostEqual(conversores["C3"](4.0), 2.0)

    def test_escalas_vazias(self) -> None:
        """Sem escalas, não há conversores a criar."""
        self.assertEqual(criar_conversores({}), {})


class TestMemoriaContrato(unittest.TestCase):
    """Contagem dos bytes e validação das entradas de medir_memoria."""

    def test_lista_conta_objetos_e_arrays_contam_dados(self) -> None:
        """A lista inclui seu objeto e cada elemento; arrays contam apenas seus dados."""
        memoria = medir_memoria(np.array([0, 0, 0, 4095], dtype=np.uint16))
        self.assertEqual(memoria["list"],
                         sys.getsizeof([0, 0, 0, 4095]) + 3 * sys.getsizeof(0) + sys.getsizeof(4095))
        for estrutura, esperado in [("array('H')", 8), ("uint16", 8), ("int32", 16),
                                    ("int64", 32), ("float32", 16), ("float64", 32)]:
            with self.subTest(estrutura=estrutura):
                self.assertEqual(memoria[estrutura], esperado)

    def test_rejeita_entradas_que_nao_sao_vetores_inteiros(self) -> None:
        """Lista Python, array escalar e vetores de tipos não inteiros são rejeitados."""
        for entrada in [[1, 2], np.array(1), np.array([1.5]),
                        np.array([True]), np.array(["1"])]:
            with self.subTest(entrada=entrada):
                with self.assertRaises(ValueError):
                    medir_memoria(entrada)


class TestConversaoContrato(unittest.TestCase):
    """Casos limite dos quatro métodos de conversão para kPa."""

    def test_vetorizado_uint16_sem_estouro_e_sem_mutacao(self) -> None:
        """A conversão de uint16 alcança 600 kPa sem overflow nem alterar a entrada."""
        contagens = np.array([0, 273, 4095], dtype=np.uint16)
        convertido = converter_vetorizado(contagens)
        self.assertIsInstance(convertido, np.ndarray)
        self.assertTrue(np.issubdtype(convertido.dtype, np.floating))
        self.assertTrue(np.allclose(convertido, [0.0, 40.0, 600.0]))
        self.assertTrue(np.array_equal(contagens, [0, 273, 4095]))

    def test_conversoes_vazias_preservam_tipo_de_retorno(self) -> None:
        """Entrada vazia produz lista nas versões Python e ndarray na vetorizada."""
        for converter in [converter_laco, converter_compreensao, converter_map]:
            with self.subTest(funcao=converter.__name__):
                convertido = converter([])
                self.assertIsInstance(convertido, list)
                self.assertEqual(convertido, [])
        convertido = converter_vetorizado(np.array([], dtype=np.uint16))
        self.assertIsInstance(convertido, np.ndarray)
        self.assertEqual(convertido.shape, (0,))


class TestTemposContrato(unittest.TestCase):
    """Validação das repetições pelo cronômetro fornecido."""

    def test_repeticoes_invalidas(self) -> None:
        """Repetições não inteiras ou não positivas levantam ValueError."""
        for k in [0, -1, 1.5, "2"]:
            with self.subTest(k=k):
                with self.assertRaises(ValueError):
                    medir_tempos(np.array([0, 4095]), k=k)


class TestReamostrarContrato(unittest.TestCase):
    """Médias por bloco, sobra final e limites válidos de reamostrar."""

    def test_descarta_sobra_sem_modificar_serie(self) -> None:
        """O ponto final sem bloco completo é descartado e a série original é preservada."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0, 1000.0])
        resultado = s.reamostrar(2)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(resultado.shape, (2,))
        self.assertTrue(np.allclose(resultado, [3.0, 7.0]))
        self.assertTrue(np.allclose(s, [2.0, 4.0, 6.0, 8.0, 1000.0]))

    def test_limites_validos_k_um_e_tamanho_total(self) -> None:
        """k igual a um preserva os valores e k igual ao tamanho produz a média total."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0])
        for k, esperado in [(1, [2.0, 4.0, 6.0, 8.0]), (4, [5.0])]:
            with self.subTest(k=k):
                resultado = s.reamostrar(k)
                self.assertIsInstance(resultado, SerieTemporal)
                self.assertEqual(resultado.shape, (len(esperado),))
                self.assertTrue(np.allclose(resultado, esperado))


if __name__ == "__main__":
    unittest.main()

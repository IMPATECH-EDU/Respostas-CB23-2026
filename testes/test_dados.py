"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import (converter_map, converter_vetorizado, ler_log,
                              medir_memoria, por_tag, serie)
from elevatoria.serie import SerieTemporal
import numpy as np

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self) -> None:
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])
# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoMediaMovel(unittest.TestCase):
    """Confere valores e limites omitidos pela aceitação da média móvel."""

    def test_media_movel_600_leituras_janela_30(self) -> None:
        """Verifica que 600 leituras com janela 30 produzem 571 médias."""
        s = SerieTemporal.de_lista(np.arange(600, dtype=float))

        resultado = s.media_movel(30)

        self.assertEqual(len(resultado), 571)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertTrue(
            np.allclose(resultado, np.arange(571) + 14.5)
        )

    def test_janela_tamanho_da_serie(self) -> None:
        """Uma janela do tamanho da série produz uma única média."""
        s = SerieTemporal.de_lista([2, 4, 9])
        resultado = s.media_movel(3)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 5.0)
        self.assertIsInstance(resultado, SerieTemporal)

    def test_janela_unitaria_preserva_pontos(self) -> None:
        """Janela unitária inclui o primeiro ponto e não modifica a entrada."""
        s = SerieTemporal.de_lista([2, 4, 9])
        copia = s.copy()
        resultado = s.media_movel(1)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(np.allclose(resultado, copia))
        self.assertTrue(np.allclose(s, copia))


class TestReamostrar(unittest.TestCase):
    """Confere blocos completos, sobras e limites da reamostragem."""

    def test_blocos_completos(self) -> None:
        """Calcula corretamente médias de blocos completos."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])

        resultado = s.reamostrar(3)

        self.assertTrue(np.allclose(resultado, [2, 5]))
        self.assertIsInstance(resultado, SerieTemporal)

    def test_descarta_sobra(self) -> None:
        """Descarta os pontos finais de um bloco incompleto."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7, 8])

        copia = s.copy()
        resultado = s.reamostrar(3)

        self.assertTrue(np.allclose(s, copia))
        self.assertEqual(len(resultado), 2)
        self.assertTrue(np.allclose(resultado, [2, 5]))

    def test_k_invalido(self) -> None:
        """Rejeita tamanhos de bloco fora do intervalo permitido."""
        s = SerieTemporal.de_lista([1, 2, 3])

        with self.assertRaises(ValueError):
            s.reamostrar(0)

        with self.assertRaises(ValueError):
            s.reamostrar(4)

class TestContratoLerLog(unittest.TestCase):
    """Cobre regras de leitura ausentes dos testes de aceitação."""

    def test_linhas_em_branco(self) -> None:
        """Linhas vazias ou só com espaços são ignoradas sem descarte."""
        self.assertEqual(ler_log("\n   \n\t\n"), ([], []))

    def test_data_hora_impossiveis(self) -> None:
        """Datas e horários impossíveis são devolvidos sem alterar o texto."""
        linhas = [
            "2026-02-30 08:00:00 INFO PT102 contagens=10  ",
            "2026-10-05 24:00:00 INFO PT102 contagens=10",
        ]
        registros, invalidas = ler_log("\n".join(linhas))
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, linhas)

    def test_resto_sem_pares(self) -> None:
        """Uma linha bem formada sem chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT102 contagens=  "
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_ordem_e_conversao_numerica(self) -> None:
        """Preserva a ordem de entrada e converte negativos e notação científica."""
        registros, invalidas = ler_log(
            "2026-10-05 08:00:06 INFO PT102 contagens=-1.5 evento=partida\n"
            "2026-10-05 08:00:00 INFO PT102 contagens=2e3"
        )
        self.assertEqual(invalidas, [])
        self.assertGreater(registros[0].instante, registros[1].instante)
        self.assertAlmostEqual(registros[0].valores["contagens"], -1.5)
        self.assertAlmostEqual(registros[1].valores["contagens"], 2000.0)
        self.assertEqual(registros[0].valores["evento"], "partida")

    def test_serie_nao_descarta_valor_convertivel(self) -> None:
        """Uma chave presente é convertida pela SerieTemporal, sem filtro de tipo."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO PT102 contagens=12")
        for valor in (12, "12"):
            with self.subTest(valor=valor):
                registros[0].valores["contagens"] = valor
                resultado = serie(registros, "PT102", "contagens")
                self.assertEqual(len(resultado), 1)
                self.assertTrue(np.allclose(resultado, [12.0]))


class TestRegressaoConversaoEMemoria(unittest.TestCase):
    """Evita medições incompletas, overflow e entradas de tipo incorreto."""

    def test_map_materializa_lista(self) -> None:
        """Map devolve uma lista calculada, permitindo medir a conversão inteira."""
        resultado = converter_map([0, 2048, 4095])
        self.assertIsInstance(resultado, list)
        self.assertTrue(np.allclose(resultado, [0.0, 2048 * 600 / 4095, 600.0]))

    def test_vetorizado_uint16_sem_overflow(self) -> None:
        """A multiplicação não estoura em uint16 nem modifica as contagens."""
        contagens = np.array([0, 2048, 4095], dtype=np.uint16)
        copia = contagens.copy()
        resultado = converter_vetorizado(contagens)
        self.assertTrue(np.allclose(resultado, [0.0, 2048 * 600 / 4095, 600.0]))
        self.assertTrue(np.array_equal(contagens, copia))

    def test_memoria_rejeita_tipo_nao_inteiro(self) -> None:
        """Arrays de float, bool, texto e objeto levantam ValueError explicativo."""
        for valores in ([1.5], [True], ["1"], [None]):
            with self.subTest(valores=valores):
                with self.assertRaisesRegex(ValueError, "inteiros"):
                    medir_memoria(np.array(valores))

    def test_memoria_rejeita_lista_e_matriz(self) -> None:
        """Lista Python e matriz são rejeitadas com mensagem explicativa."""
        for valores in ([1, 2], np.ones((2, 2), dtype=int)):
            with self.subTest(valores=valores):
                with self.assertRaisesRegex(ValueError, "ndarray 1D"):
                    medir_memoria(valores)


if __name__ == "__main__":
    unittest.main()

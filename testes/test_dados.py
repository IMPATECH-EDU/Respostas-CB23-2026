"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import converter_vetorizado, ler_log, medir_memoria, por_tag, valida_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestMediaMovel(unittest.TestCase):
    """Testes de regressão da média móvel (issue #4)."""

    def test_primeira_janela(self) -> None:
        """A média móvel inclui a primeira janela e tem n - janela + 1 valores."""
        serie = SerieTemporal.de_lista([2, 4, 6, 8])
        resultado = serie.media_movel(2)

        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(len(resultado), 3)
        for valor, esperado in zip(resultado, [3.0, 5.0, 7.0]):
            self.assertAlmostEqual(float(valor), esperado)

    def test_janela_do_tamanho_da_serie(self) -> None:
        """Uma janela do tamanho da série devolve uma única média."""
        serie = SerieTemporal.de_lista([2, 4, 6, 8])
        resultado = serie.media_movel(4)

        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 5.0)


class TestValidaTag(unittest.TestCase):
    """Verifica os limites do formato das tags."""

    def test_limites_validos(self) -> None:
        """Aceita uma ou duas letras e de um a três dígitos."""
        for tag in ["A1", "A12", "A123", "AB1", "AB12", "AB123"]:
            with self.subTest(tag=tag):
                self.assertTrue(valida_tag(tag))

    def test_caracteres_extras(self) -> None:
        """Rejeita letras em excesso, espaços e texto depois da tag."""
        for tag in ["ABC1", "AB1234", " A1", "A1\n", "A1texto", ""]:
            with self.subTest(tag=tag):
                self.assertFalse(valida_tag(tag))


class TestLerLog(unittest.TestCase):
    """Verifica regras do leitor que os testes de aceitação não cobrem."""

    def test_ignora_linhas_em_branco(self) -> None:
        """Linhas vazias ou só com espaços não entram nas linhas inválidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=100\n\n"
        registros, invalidas = ler_log(texto)

        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])
        self.assertAlmostEqual(registros[0].valores["contagens"], 100.0)

    def test_rejeita_data_e_hora_impossiveis(self) -> None:
        """Datas e horários impossíveis são devolvidos como linhas inválidas."""
        linhas = [
            "2026-02-30 08:00:00 INFO PT101 contagens=100",
            "2026-10-05 25:00:00 INFO PT101 contagens=100",
        ]
        registros, invalidas = ler_log("\n".join(linhas))

        self.assertEqual(registros, [])
        self.assertEqual(invalidas, linhas)

    def test_rejeita_linha_sem_pares(self) -> None:
        """Uma linha sem chave=valor é descartada preservando seus espaços."""
        linha = "2026-10-05 08:00:00 INFO B1 evento de partida   "
        registros, invalidas = ler_log(linha)

        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])


class TestMemoriaEConversao(unittest.TestCase):
    """Verifica os tipos de entrada e a conversão de contagens uint16."""

    def test_memoria_rejeita_lista_e_floats(self) -> None:
        """A medição de memória rejeita listas e arrays de ponto flutuante."""
        for entrada in [[0, 100, 4095], np.array([0.0, 100.0, 4095.0])]:
            with self.subTest(entrada=entrada), self.assertRaises(ValueError):
                medir_memoria(entrada)

    def test_conversao_uint16_sem_estouro(self) -> None:
        """A conversão vetorizada evita overflow e preserva as contagens originais."""
        contagens = np.array([0, 2048, 4095], dtype=np.uint16)
        copia = contagens.copy()
        pressoes = converter_vetorizado(contagens)

        self.assertTrue(np.allclose(pressoes, [0.0, 2048 * 600 / 4095, 600.0]))
        self.assertEqual(pressoes.dtype, np.dtype(float))
        self.assertTrue(np.array_equal(contagens, copia))


class TestReamostrar(unittest.TestCase):
    """Verifica as médias por bloco e o descarte dos pontos restantes."""

    def test_blocos_completos(self) -> None:
        """Calcula a média de cada bloco sem modificar a série original."""
        serie = SerieTemporal.de_lista([2, 4, 6, 8, 10, 12])
        copia = serie.copy()
        resultado = serie.reamostrar(2)

        self.assertIsInstance(resultado, SerieTemporal)
        self.assertTrue(np.allclose(resultado, [3.0, 7.0, 11.0]))
        self.assertTrue(np.array_equal(serie, copia))

    def test_descarta_sobra(self) -> None:
        """Os pontos que não completam o último bloco são descartados."""
        serie = SerieTemporal.de_lista([2, 4, 6, 8, 100])
        resultado = serie.reamostrar(2)

        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(np.allclose(resultado, [3.0, 7.0]))


if __name__ == "__main__":
    unittest.main()

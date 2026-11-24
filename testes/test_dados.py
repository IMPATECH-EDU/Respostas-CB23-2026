"""Testes do Marco 1 da estação elevatória."""

import unittest

import numpy as np

from elevatoria.dados import ler_log, por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo de teste fornecido pela disciplina."""

    def test_lista_vazia(self) -> None:
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestMediaMovel(unittest.TestCase):
    """Testes de regressão da média móvel da issue #4."""

    def test_quantidade_de_janelas(self) -> None:
        """Uma série de 1000 pontos com janela de 40 produz 961 médias."""
        serie = SerieTemporal.de_lista(list(range(1000)))

        resultado = serie.media_movel(40)

        self.assertEqual(len(resultado), 961)

    def test_media_movel_inclui_primeira_janela(self) -> None:
        """As médias incluem a primeira e a última janela, na ordem original."""
        serie = SerieTemporal.de_lista([1, 2, 3, 4])

        resultado = serie.media_movel(2)

        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(np.allclose(resultado, [1.5, 2.5, 3.5]))

    def test_media_movel_janela_igual_ao_tamanho(self) -> None:
        """Uma janela do tamanho da série produz uma única média."""
        serie = SerieTemporal.de_lista([2, 4, 6])

        resultado = serie.media_movel(3)

        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(resultado[0], 4.0)


class TestReamostrar(unittest.TestCase):
    """Testes das médias por bloco da issue #5."""

    def test_descarta_sobra(self) -> None:
        """Com 11 pontos e blocos de 2, o último ponto é descartado."""
        serie = SerieTemporal.de_lista(list(range(11)))

        resultado = serie.reamostrar(2)

        self.assertEqual(len(resultado), 5)
        self.assertTrue(np.allclose(resultado, [0.5, 2.5, 4.5, 6.5, 8.5]))

    def test_blocos_exatos(self) -> None:
        """Quando a divisão é exata, o último bloco também entra no resultado."""
        serie = SerieTemporal.de_lista([1, 2, 3, 10, 20, 30])

        resultado = serie.reamostrar(3)

        self.assertEqual(len(resultado), 2)
        self.assertTrue(np.allclose(resultado, [2.0, 20.0]))


class TestLerLog(unittest.TestCase):
    """Testes das regras de leitura do log SCADA."""

    def test_preserva_texto_e_ordem_das_invalidas(self) -> None:
        """Linhas inválidas mantêm seus espaços e sua ordem, e linhas vazias são ignoradas."""
        primeira = "  linha corrompida  "
        segunda = "2026-10-05 08:00:00 INFO PT101 sem_pares  "
        valida = "2026-10-05 08:00:00 INFO PT101 contagens=131"
        texto = "\n".join([primeira, "   ", valida, segunda])

        registros, invalidas = ler_log(texto)

        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [primeira, segunda])

    def test_ano_bissexto(self) -> None:
        """O dia 29 de fevereiro é aceito em 2024 e descartado em 2025."""
        valida = "2024-02-29 08:00:00 INFO PT101 contagens=131"
        invalida = "2025-02-29 08:00:00 INFO PT101 contagens=132"

        registros, invalidas = ler_log(invalida + "\n" + valida)

        self.assertEqual(invalidas, [invalida])
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0].instante.year, 2024)
        self.assertEqual(registros[0].instante.day, 29)

    def test_notacao_cientifica_e_texto_no_mesmo_registro(self) -> None:
        """Um número em notação científica vira float e o evento continua como texto."""
        linha = "2026-10-05 08:00:00 INFO B1 evento=partida corrente=4.75e1"

        registros, invalidas = ler_log(linha)

        self.assertEqual(invalidas, [])
        self.assertEqual(len(registros), 1)
        valores = registros[0].valores
        self.assertEqual(valores["evento"], "partida")
        self.assertIsInstance(valores["corrente"], float)
        self.assertAlmostEqual(valores["corrente"], 47.5)


if __name__ == "__main__":
    unittest.main()
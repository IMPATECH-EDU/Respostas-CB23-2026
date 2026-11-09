"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import ler_log, por_tag, valida_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestMediaMovelRegressaoIssue4(unittest.TestCase):
    """Issue 4: a média móvel devolvia um valor a menos (a última janela era perdida)."""

    def test_600_pontos_janela_30_devolve_571(self):
        """Série de 600 pontos com janela de 30 devolve 600 - 30 + 1 = 571 valores."""
        s = SerieTemporal(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_ultima_janela_e_incluida(self):
        """A última janela (os 3 últimos pontos) entra no resultado, com os valores corretos."""
        mm = SerieTemporal([1.0, 2.0, 3.0, 4.0, 5.0]).media_movel(3)
        self.assertTrue(np.allclose(mm, [2.0, 3.0, 4.0]))

    def test_janela_do_tamanho_da_serie(self):
        """Com janela igual ao tamanho da série há exatamente uma janela: a média de tudo."""
        mm = SerieTemporal([1.0, 2.0, 3.0]).media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(mm[0], 2.0)


class TestReamostrar(unittest.TestCase):
    """Issue 5: médias de blocos consecutivos de k pontos."""

    def test_blocos_exatos_de_uma_hora(self):
        """600 leituras de 6 s em blocos de 10 dão 60 médias por minuto."""
        s = SerieTemporal(np.arange(600.0))
        r = s.reamostrar(10)
        self.assertEqual(len(r), 60)
        self.assertAlmostEqual(r[0], 4.5)
        self.assertAlmostEqual(r[59], 594.5)

    def test_sobra_no_fim_e_descartada(self):
        """Com 7 pontos e k = 3, os blocos são [1,2,3] e [4,5,6]; o ponto 7 sobra e é descartado."""
        r = SerieTemporal([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]).reamostrar(3)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_invalido_e_serie_intacta(self):
        """k = 0, negativo, não inteiro ou maior que a série levanta ValueError; a série não muda."""
        s = SerieTemporal([1.0, 2.0, 3.0])
        for k in (0, -1, 2.5, 4):
            with self.subTest(k=k), self.assertRaises(ValueError):
                s.reamostrar(k)
        self.assertTrue(np.allclose([s[0], s[1], s[2]], [1.0, 2.0, 3.0]))


class TestLerLogContrato(unittest.TestCase):
    """Issue 1: regras do contrato de `ler_log` que a aceitação não verifica."""

    def test_data_impossivel_e_invalida(self):
        """Uma linha com o formato certo, mas data e hora que não existem, vai para as inválidas."""
        linha = "2026-13-45 25:61:00 INFO PT101 contagens=1800"
        registros, invalidas = ler_log(linha)
        self.assertEqual((registros, invalidas), ([], [linha]))

    def test_nivel_desconhecido_e_invalido(self):
        """Só INFO, WARN e ALARME são níveis válidos; DEBUG torna a linha inválida."""
        linha = "2026-10-05 08:00:00 DEBUG PT101 contagens=1800"
        registros, invalidas = ler_log(linha)
        self.assertEqual((registros, invalidas), ([], [linha]))


class TestElevatoriaOitoExtras(unittest.TestCase):
    """Testes de `valida_tag`, `ler_log` e `SerieTemporal`."""

    # --- Testes para dados.py ---

    def test_01_valida_tag_correta(self):
        """1. Garante que o regex aceita tags perfeitamente formatadas."""
        self.assertTrue(valida_tag("PT101"))
        self.assertTrue(valida_tag("B1"))
        self.assertTrue(valida_tag("FT201"))

    def test_02_valida_tag_incorreta(self):
        """2. Garante que o regex rejeita espaços, minúsculas e formatos errados."""
        self.assertFalse(valida_tag("pt101"))
        self.assertFalse(valida_tag("101PT"))
        self.assertFalse(valida_tag("PT101 "))

    def test_03_ler_log_linhas_validas(self):
        """3. Verifica se as linhas bem formatadas geram objetos Registro corretamente."""
        texto_log = "2026-10-19 12:00:00 INFO PT101 valor=10.5 estado=ativo"
        registros, invalidas = ler_log(texto_log)

        self.assertEqual(len(invalidas), 0)
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0].tag, "PT101")
        self.assertAlmostEqual(registros[0].valores["valor"], 10.5)
        self.assertEqual(registros[0].valores["estado"], "ativo")

    def test_04_ler_log_linhas_invalidas(self):
        """4. Garante que linhas sem o formato exato são separadas para a lista de inválidas."""
        texto_log = (
            "2026-10-19 12:00:00 INFO PT101\n"  # Faltam os pares chave=valor
            "Data errada INFO PT101 valor=10\n"  # Formato de data incorreto
        )
        registros, invalidas = ler_log(texto_log)

        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 2)

    # --- Testes para serie.py ---

    def test_05_serie_temporal_dimensoes(self):
        """5. Verifica se a série rejeita matrizes que não sejam unidimensionais."""
        serie = SerieTemporal([1.0, 2.0, 3.0])
        self.assertEqual(len(serie), 3)

        with self.assertRaises(ValueError):
            SerieTemporal(np.array([[1, 2], [3, 4]]))

    def test_06_serie_temporal_estatisticas(self):
        """6. Confirma o cálculo correto de média, mínimo, máximo, soma e amplitude."""
        serie = SerieTemporal([10.0, 20.0, 30.0])
        self.assertAlmostEqual(serie.media(), 20.0)
        self.assertAlmostEqual(serie.min(), 10.0)
        self.assertAlmostEqual(serie.max(), 30.0)
        self.assertAlmostEqual(serie.sum(), 60.0)
        self.assertAlmostEqual(serie.amplitude(), 20.0)

    def test_07_serie_temporal_aritmetica(self):
        """7. Verifica se as operações aritméticas (+, -, *, /) afetam todos os elementos."""
        serie = SerieTemporal([2.0, 4.0, 6.0])

        self.assertAlmostEqual((serie + 2.0)[0], 4.0)
        self.assertAlmostEqual((serie / 2.0)[2], 3.0)

    def test_08_serie_temporal_janela_invalida(self):
        """8. Verifica se o método media_movel bloqueia janelas de tamanho incorreto."""
        serie = SerieTemporal([1.0, 2.0, 3.0])

        with self.assertRaises(ValueError):
            serie.media_movel(5)

        with self.assertRaises(ValueError):
            serie.media_movel(0)


if __name__ == "__main__":
    unittest.main()
"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import contagem_por_tag, criar_conversores, ler_log, por_tag, serie
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestRegressaoMediaMovel(unittest.TestCase):
    """Issue #4: media_movel devolvia n - janela valores em vez de n - janela + 1."""

    def test_tamanho_n_menos_janela_mais_um(self):
        """Com 600 pontos e janela 30, a média móvel tem 571 valores."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_janela_incluida(self):
        """O primeiro valor é a média de s[0:janela], e não a de s[1:janela + 1]."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 1.5)

    def test_janela_do_tamanho_da_serie(self):
        """Com janela = len(s), sai um único valor: a média da série inteira."""
        s = SerieTemporal.de_lista([2.0, 4.0, 9.0])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 5.0)


class TestReamostrarSobra(unittest.TestCase):
    """Issue #5: reamostrar, com atenção aos pontos que sobram no fim."""

    def test_sobra_no_fim_descartada(self):
        """Com 7 pontos e k = 3, saem 2 médias e o sétimo ponto é descartado."""
        r = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 100]).reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_igual_ao_tamanho(self):
        """Com k = len(s), sai um único bloco: a média da série inteira."""
        r = SerieTemporal.de_lista([1.0, 2.0, 6.0]).reamostrar(3)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(r, [3.0]))

    def test_nao_modifica_a_serie(self):
        """reamostrar devolve uma série nova e deixa a original intacta."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        copia = np.array(s)
        s.reamostrar(2)
        self.assertTrue(np.array_equal(s, copia))


class TestContratoLerLog(unittest.TestCase):
    """Issue #1: regras do contrato de ler_log que os testes de aceitação não verificam."""

    def test_linhas_vazias_nao_contam(self):
        """Linhas vazias ou só com espaços são ignoradas e não entram em `invalidas`."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=131\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual((len(registros), invalidas), (1, []))

    def test_data_impossivel_e_invalida(self):
        """Uma linha que casa com LINHA, mas tem mês 13 ou hora 25, é inválida."""
        linhas = ["2026-13-05 08:00:00 INFO PT101 contagens=131",
                  "2026-10-05 25:00:00 INFO PT101 contagens=131"]
        registros, invalidas = ler_log("\n".join(linhas))
        self.assertEqual((registros, invalidas), ([], linhas))

    def test_sem_par_chave_valor_e_invalida(self):
        """Uma linha cujo resto não tem nenhum par chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 WARN B1 sem pares aqui"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_varios_espacos_e_valor_texto(self):
        """Partes separadas por vários espaços; número vira float e texto continua str."""
        registros, _ = ler_log("2026-10-05  08:00:06   WARN B1  evento=vibracao corrente=49.8")
        self.assertEqual(registros[0].valores, {"evento": "vibracao", "corrente": 49.8})
        self.assertEqual(registros[0].instante.second, 6)


class TestContagemSerieConversores(unittest.TestCase):
    """Issues #1 e #2: contagem_por_tag, serie e criar_conversores."""

    def test_serie_de_tag_ausente_e_vazia(self):
        """serie de uma tag que não está no log devolve uma SerieTemporal vazia."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO PT101 contagens=131")
        s = serie(registros, "PT102", "contagens")
        self.assertIsInstance(s, SerieTemporal)
        self.assertEqual(len(s), 0)

    def test_contagem_soma_o_total(self):
        """A soma das contagens por tag é o número de registros."""
        texto = ("2026-10-05 08:00:00 INFO PT101 contagens=1\n"
                 "2026-10-05 08:00:06 INFO PT101 contagens=2\n"
                 "2026-10-05 08:00:06 INFO FT201 pulsos=3\n")
        registros, _ = ler_log(texto)
        self.assertEqual(contagem_por_tag(registros), {"PT101": 2, "FT201": 1})

    def test_conversor_nao_usa_o_ultimo_fator(self):
        """Cada conversor usa o fator da própria tag, mesmo sendo o primeiro do dicionário."""
        conv = criar_conversores({"PT102": 600 / 4095, "FT201": 0.1})
        self.assertAlmostEqual(conv["PT102"](4095), 600.0)
        self.assertAlmostEqual(conv["FT201"](10), 1.0)


if __name__ == "__main__":
    unittest.main()

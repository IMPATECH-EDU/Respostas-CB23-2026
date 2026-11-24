"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import (converter_vetorizado, criar_conversores, ler_log, medir_memoria,
                              por_tag, serie, valida_tag)
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoMediaMovel(unittest.TestCase):
    """Issue #4: media_movel deve devolver n - janela + 1 médias, começando na primeira janela."""

    def setUp(self):
        self.quadrados = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])

    def test_tamanho_do_caso_relatado(self):
        """600 leituras com janela 30 dão 571 médias, como no relato da issue."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_media_e_a_da_primeira_janela(self):
        """Os valores começam em mean(s[0:2]); nenhuma janela é pulada."""
        mm = self.quadrados.media_movel(2)
        self.assertEqual(len(mm), 4)
        self.assertAlmostEqual(float(mm[0]), 2.5)
        self.assertTrue(np.allclose(mm, [2.5, 6.5, 12.5, 20.5]))

    def test_janela_do_tamanho_da_serie(self):
        """Com janela = len(s), sai um único valor: a média da série inteira."""
        mm = self.quadrados.media_movel(5)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 11.0)

    def test_janela_um_devolve_a_propria_serie(self):
        """Com janela 1, cada média é o próprio ponto: a série volta inteira."""
        mm = self.quadrados.media_movel(1)
        self.assertEqual(len(mm), len(self.quadrados))
        self.assertTrue(np.allclose(mm, self.quadrados))


LEITURA_OK = "2026-10-05 08:00:00 INFO PT101 contagens=131"


class TestReamostrar(unittest.TestCase):
    """Issue #5: médias por bloco, com a sobra do fim descartada."""

    def test_sobra_no_fim_e_descartada(self):
        """Com 7 pontos e k = 3, saem 2 médias, e o 7º ponto não entra em nenhuma."""
        r = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 1000]).reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_igual_ao_tamanho_e_k_um(self):
        """k = len(s) dá a média da série inteira; k = 1 devolve a própria série."""
        s = SerieTemporal.de_lista([2.0, 4.0, 9.0])
        self.assertTrue(np.allclose(s.reamostrar(3), [5.0]))
        self.assertTrue(np.allclose(s.reamostrar(1), s))

    def test_tipo_e_imutabilidade(self):
        """O resultado é SerieTemporal 1D, e a série original não muda."""
        s = SerieTemporal.de_lista(np.arange(10.0))
        original = np.array(s)
        r = s.reamostrar(4)
        self.assertIsInstance(r, SerieTemporal)
        self.assertEqual(r.ndim, 1)
        self.assertTrue(np.array_equal(s, original))

    def test_k_nao_inteiro(self):
        """k = 2.0 (float) ou True não são aceitos: ValueError."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        for k in [2.0, True]:
            with self.subTest(k=k), self.assertRaises(ValueError):
                s.reamostrar(k)


class TestContratoLerLog(unittest.TestCase):
    """Issue #1: regras da docstring de ler_log que os testes de aceitação não verificam."""

    def test_linhas_em_branco_nao_contam_como_invalidas(self):
        """Linhas vazias ou só com espaços e tabs são puladas sem ir para `invalidas`."""
        texto = f"\n   \n{LEITURA_OK}\n\t \n\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_ou_hora_impossivel_e_invalida(self):
        """Linha no formato certo, mas com mês 13, 30 de fevereiro ou 25 h, é descartada."""
        impossiveis = ["2026-13-05 08:00:00 INFO PT101 contagens=131",
                       "2026-02-30 08:00:00 INFO PT101 contagens=131",
                       "2026-10-05 25:00:00 INFO PT101 contagens=131"]
        registros, invalidas = ler_log("\n".join(impossiveis))
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, impossiveis)

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Linha cujo resto não tem nenhum chave=valor vai para `invalidas`."""
        linha = "2026-10-05 08:00:00 WARN B1 bomba sem resposta"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_invalida_devolvida_exatamente_como_no_texto(self):
        """A linha descartada volta sem strip: espaços no início e no fim são preservados."""
        linha = "  2026-10-05 08:00:00 INFO PT101 contagens=131  "
        _, invalidas = ler_log(f"{LEITURA_OK}\n{linha}\n")
        self.assertEqual(invalidas, [linha])

    def test_conversao_de_valores_mistos(self):
        """Números negativos e decimais viram float; textos continuam str, na mesma linha."""
        registros, _ = ler_log("2026-10-05 08:00:00 WARN B1 evento=vibracao corrente=-49.8 fase=A1")
        valores = registros[0].valores
        self.assertAlmostEqual(valores["corrente"], -49.8)
        self.assertIsInstance(valores["corrente"], float)
        self.assertEqual((valores["evento"], valores["fase"]), ("vibracao", "A1"))

    def test_ordem_original_e_separadores_multiplos(self):
        """Vários espaços entre as partes são aceitos, e a ordem do texto é mantida."""
        texto = ("2026-10-05 08:00:06   INFO  FT201   pulsos=3873\n"
                 "2026-10-05 08:00:00 INFO LT301 nivel=46.99\n")
        registros, invalidas = ler_log(texto)
        self.assertEqual(invalidas, [])
        self.assertEqual([r.tag for r in registros], ["FT201", "LT301"])


class TestValidaTagESerie(unittest.TestCase):
    """Issue #1: valida_tag nos limites e serie com valores não numéricos."""

    def test_limites_de_letras_e_digitos(self):
        """Duas letras e três dígitos é o máximo; três letras ou nenhum dígito, não."""
        self.assertTrue(valida_tag("AB123"))
        self.assertTrue(valida_tag("Z9"))
        for invalida in ["ABC1", "A", "", "P T101", "PT10a"]:
            with self.subTest(tag=invalida):
                self.assertFalse(valida_tag(invalida))

    def test_serie_de_chave_textual_levanta_value_error(self):
        """Chave com texto (evento) levanta ValueError; chave que nenhum registro tem dá série vazia."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5")
        with self.assertRaises(ValueError):
            serie(registros, "B1", "evento")
        self.assertEqual(len(serie(registros, "B1", "inexistente")), 0)



class TestCriarConversores(unittest.TestCase):
    """Issue #2: cada conversor fica preso ao fator da sua própria tag."""

    def test_primeira_tag_nao_usa_o_ultimo_fator(self):
        """O conversor da primeira tag usa o seu fator, e não o da última (late binding)."""
        conv = criar_conversores({"PT101": 600 / 4095, "FT201": 0.1})
        self.assertAlmostEqual(conv["PT101"](4095), 600.0)
        self.assertAlmostEqual(conv["FT201"](4095), 409.5)

    def test_mudar_o_dicionario_depois_nao_afeta(self):
        """Alterar o dicionário de escalas depois de criar os conversores não muda nada."""
        escalas = {"A1": 2.0}
        conv = criar_conversores(escalas)
        escalas["A1"] = 100.0
        self.assertAlmostEqual(conv["A1"](3.0), 6.0)
        self.assertEqual(criar_conversores({}), {})



class TestMemoriaEConversao(unittest.TestCase):
    """Issue #3: entradas inválidas de medir_memoria e estouro na versão vetorizada."""

    def test_memoria_rejeita_float_e_lista(self):
        """medir_memoria recusa contagens em float e uma lista Python, com ValueError."""
        for invalida in [np.array([1.0, 2.0]), [1, 2, 3]]:
            with self.subTest(entrada=type(invalida).__name__), self.assertRaises(ValueError):
                medir_memoria(invalida)

    def test_memoria_rejeita_fora_da_faixa_do_ad(self):
        """Contagem negativa ou acima de 4095 não é de um A/D de 12 bits: ValueError."""
        for invalida in [np.array([-1, 10]), np.array([0, 4096])]:
            with self.subTest(entrada=invalida.tolist()), self.assertRaises(ValueError):
                medir_memoria(invalida)

    def test_vetorizado_nao_estoura_com_uint16(self):
        """Com contagens uint16, a conversão ainda dá 600 kPa em 4095 (sem estouro de 16 bits)."""
        kpa = converter_vetorizado(np.array([0, 4095], dtype=np.uint16))
        self.assertTrue(np.allclose(kpa, [0.0, 600.0]))
        self.assertEqual(kpa.dtype, np.float64)


if __name__ == "__main__":
    unittest.main()

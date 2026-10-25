"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import ler_log, valida_tag
from elevatoria.serie import SerieTemporal

# class TestPorTagExemplo(unittest.TestCase):
#     """Exemplo do formato. `por_tag` é código existente da base."""

#     def test_lista_vazia(self):
#         """Sem registros, por_tag devolve uma lista vazia."""
#         self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestValidaTagExemplo(unittest.TestCase):
    """Testes de valida_tag."""

    def test_tags_validas_da_docstring(self):
        """Aceita as tags válidas listadas na docstring."""
        for tag in ["PT101", "FT201", "B1"]:
            with self.subTest(tag=tag):
                self.assertTrue(valida_tag(tag))

    def test_tags_invalidas_da_docstring(self):
        """Rejeita as tags inválidas listadas na docstring."""
        for tag in ["pt101", "PT", "PT1010", "101PT", "PT101 "]:
            with self.subTest(tag=tag):
                self.assertFalse(valida_tag(tag))

    def test_string_vazia(self):
        """Uma string vazia não é uma tag."""
        self.assertFalse(valida_tag(""))

    def test_quebra_de_linha_no_fim(self):
        """Uma quebra de linha no fim da string a invalida."""
        self.assertFalse(valida_tag("PT101\n"))

class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: media_movel deve devolver n - janela + 1 valores, a partir da 1ª janela."""

    def setUp(self):
        self.s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])

    def test_tamanho_do_resultado(self):
        """Com 5 pontos e janela 2, o resultado tem 4 valores (n - janela + 1)."""
        self.assertEqual(len(self.s.media_movel(2)), 4)

    def test_valores_comecam_na_primeira_janela(self):
        """O primeiro valor é a média dos 2 primeiros pontos, e não dos pontos 1 e 2."""
        np.testing.assert_allclose(self.s.media_movel(2), [1.5, 2.5, 3.5, 4.5])

    def test_janela_igual_ao_tamanho(self):
        """Com janela igual ao tamanho da série, o resultado é a média geral (1 valor)."""
        r = self.s.media_movel(5)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(float(r[0]), 3.0)

    def test_janela_um_devolve_a_propria_serie(self):
        """Com janela 1, a média móvel é a própria série, sem perder o primeiro ponto."""
        np.testing.assert_allclose(self.s.media_movel(1), np.array(self.s))

    def test_serie_de_600_pontos_janela_30(self):
        """O caso do relato: 600 pontos e janela 30 dão 571 valores."""
        grande = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(grande.media_movel(30)), 571)

    def test_mantem_o_tipo_serie_temporal(self):
        """O resultado continua sendo uma SerieTemporal (guarda, passa antes e depois)."""
        self.assertIsInstance(self.s.media_movel(2), SerieTemporal)

class TestReamostrar(unittest.TestCase):
    """Issue #5: SerieTemporal.reamostrar."""

    def test_blocos_exatos(self):
        """Dez pontos com k=5 dão duas médias calculadas à mão."""
        s = SerieTemporal.de_lista(range(1, 11))
        self.assertTrue(np.allclose(s.reamostrar(5), [3.0, 8.0]))

    def test_sobra_no_fim_e_descartada(self):
        """Com 11 pontos e k=5, o último ponto (muito diferente) não entra em nenhuma média."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1000])
        r = s.reamostrar(5)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [3.0, 8.0]))

    def test_k_um_e_k_igual_ao_tamanho(self):
        """Com k=1 devolve a própria série; com k=len devolve um único valor, a média."""
        s = SerieTemporal.de_lista([2.0, 4.0, 9.0])
        self.assertTrue(np.allclose(s.reamostrar(1), s))
        self.assertAlmostEqual(float(s.reamostrar(3)[0]), 5.0)

    def test_k_invalido_levanta_value_error(self):
        """k=0 e k maior que o tamanho da série levantam ValueError."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0])
        for k in (0, 4):
            with self.subTest(k=k), self.assertRaises(ValueError):
                s.reamostrar(k)

    def test_nao_modifica_a_serie_e_mantem_o_tipo(self):
        """O resultado é uma SerieTemporal e a série original não muda."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        copia = np.array(s)
        r = s.reamostrar(2)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.array_equal(s, copia))

class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras do contrato de ler_log que os testes de aceitação não verificam."""

    def test_linhas_so_com_espacos_sao_ignoradas(self):
        """Linhas vazias ou só com espaços não viram registro nem contam como inválidas."""
        texto = "\n".join(["2026-10-05 08:00:00 INFO PT102 contagens=1623", "", "     ", "\t"])
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_mes_impossivel_e_invalido(self):
        """Uma linha com mês 13 casa com o padrão, mas é inválida por data impossível."""
        linha = "2026-13-05 08:00:00 INFO PT102 contagens=1623"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_hora_impossivel_e_invalida(self):
        """Uma linha com hora 25 também é inválida."""
        linha = "2026-10-05 25:00:00 INFO PT102 contagens=1623"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Se o resto não tem nenhum par chave=valor, a linha é inválida e volta intacta."""
        linha = "2026-10-05 08:00:00 INFO PT102 sem pares aqui"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_registros_seguem_a_ordem_do_texto(self):
        """Os registros saem na mesma ordem em que as linhas aparecem no texto."""
        texto = "\n".join(["2026-10-05 08:00:06 INFO PT102 contagens=2",
                           "2026-10-05 08:00:00 INFO PT101 contagens=1"])
        registros, _ = ler_log(texto)
        self.assertEqual([r.tag for r in registros], ["PT102", "PT101"])

if __name__ == "__main__":
    unittest.main()

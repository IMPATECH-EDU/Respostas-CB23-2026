"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import (converter_vetorizado, criar_conversores, ler_log, medir_memoria,
                              por_tag)
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: media_movel devolvia um valor a menos. Escritos antes da correção."""

    def test_tamanho_do_relato(self):
        """600 leituras com janela 30 dão 571 médias (o relato recebia 570)."""
        s = SerieTemporal.de_lista(np.linspace(1700.0, 1800.0, 600))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_janela_aparece(self):
        """O primeiro valor é a média de s[0:janela], que o código antigo pulava."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 3.0)

    def test_janela_do_tamanho_da_serie(self):
        """Com janela = len(s) sai uma média só, a da série inteira (antes saía vazio)."""
        mm = SerieTemporal.de_lista([1.0, 2.0, 6.0]).media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 3.0)


class TestReamostrar(unittest.TestCase):
    """Issue #5: SerieTemporal.reamostrar."""

    def test_sobra_no_fim_e_descartada(self):
        """Com 7 pontos e k = 3 o sétimo fica de fora: duas médias, sem o 100."""
        r = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 100]).reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_igual_ao_tamanho(self):
        """k = len(s) dá um bloco só, com a média da série inteira."""
        r = SerieTemporal.de_lista([1.0, 2.0, 6.0]).reamostrar(3)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(float(r[0]), 3.0)

    def test_nao_altera_a_serie(self):
        """Depois de reamostrar, a série original continua com os mesmos 5 valores."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        s.reamostrar(2)
        self.assertTrue(np.allclose(s, [1.0, 2.0, 3.0, 4.0, 5.0]))


class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras de ler_log que os testes de aceitação não conferem."""

    def test_linhas_em_branco_nao_sao_invalidas(self):
        """Linhas vazias ou só com espaços são puladas e não entram em invalidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=131\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual((len(registros), invalidas), (1, []))

    def test_data_ou_hora_impossivel(self):
        """Mês 13 e hora 25 casam com LINHA, mas a linha vai para invalidas."""
        linhas = ["2026-13-05 08:00:00 INFO PT101 contagens=131",
                  "2026-10-05 25:00:00 INFO PT101 contagens=131"]
        self.assertEqual(ler_log("\n".join(linhas)), ([], linhas))

    def test_resto_sem_par_chave_valor(self):
        """Linha cujo resto não tem nenhum par chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 WARN B1 vibracao alta"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_invalida_volta_como_estava(self):
        """A linha descartada volta sem strip, com os espaços do começo."""
        linha = "  2026-10-05 08:00:00 INFO PT101 contagens=131"
        self.assertEqual(ler_log(linha)[1], [linha])

    def test_digitos_de_largura_total(self):
        """Data com dígitos de largura total (２０２６) é inválida, apesar do strptime aceitar."""
        linha = "２０２６-10-05 08:00:00 INFO PT101 contagens=131"
        self.assertEqual(ler_log(linha)[1], [linha])


class TestConversores(unittest.TestCase):
    """Issue #2: criar_conversores."""

    def test_fator_fica_fixo_na_criacao(self):
        """Mudar o dicionário de escalas depois não altera os conversores já criados."""
        escalas = {"PT101": 2.0, "FT201": 0.1}
        conversores = criar_conversores(escalas)
        escalas["PT101"] = 1000.0
        self.assertAlmostEqual(conversores["PT101"](3.0), 6.0)


class TestMemoriaEConversao(unittest.TestCase):
    """Issue #3: casos de medir_memoria e da conversão que a aceitação não testa."""

    def test_vetorizado_com_uint16(self):
        """Contagens em uint16 não estouram na conversão: 4095 vira 600 kPa."""
        kpa = converter_vetorizado(np.array([0, 4095], dtype=np.uint16))
        self.assertTrue(np.allclose(kpa, [0.0, 600.0]))

    def test_memoria_recusa_lista_e_float(self):
        """Lista comum e ndarray de float levantam ValueError."""
        for entrada in ([1, 2, 3], np.array([1.0, 2.0, 3.0])):
            with self.subTest(entrada=entrada), self.assertRaises(ValueError):
                medir_memoria(entrada)

    def test_memoria_recusa_fora_da_faixa(self):
        """Contagens negativas ou acima de 4095 levantam ValueError."""
        for ruins in ([0, 4096], [-1, 10]):
            with self.subTest(contagens=ruins), self.assertRaises(ValueError):
                medir_memoria(np.array(ruins))


if __name__ == "__main__":
    unittest.main()

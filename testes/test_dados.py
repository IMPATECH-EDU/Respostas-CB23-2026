"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import ler_log, por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: media_movel deve devolver n - janela + 1 valores."""

    def setUp(self):
        self.s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

    def test_tamanho_do_resultado(self):
        """Série de 6 pontos com janela 3 devolve 4 valores, e não 3."""
        self.assertEqual(len(self.s.media_movel(3)), 4)

    def test_valores_incluem_a_primeira_janela(self):
        """O primeiro valor é a média de s[0:3] (2.0) e os demais vêm em seguida."""
        self.assertTrue(np.allclose(self.s.media_movel(3), [2.0, 3.0, 4.0, 5.0]))

    def test_janela_igual_ao_tamanho(self):
        """Janela do tamanho da série devolve um único valor: a média de tudo."""
        r = self.s.media_movel(6)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(float(r[0]), 3.5)

    def test_janela_um_devolve_a_propria_serie(self):
        """Janela 1 devolve os mesmos 6 valores da série."""
        self.assertTrue(np.allclose(self.s.media_movel(1), self.s))

    def test_tipo_e_imutabilidade(self):
        """O resultado continua SerieTemporal e a série original não muda."""
        copia = np.array(self.s)
        r = self.s.media_movel(2)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.array_equal(self.s, copia))


class TestReamostrar(unittest.TestCase):
    """Issue #5: SerieTemporal.reamostrar."""

    def test_descarta_a_sobra_no_fim(self):
        """Com 7 pontos e k=3, o ponto que sobra é descartado: 2 blocos."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 99])
        r = s.reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_igual_ao_tamanho(self):
        """k igual ao tamanho devolve um único valor: a média da série."""
        r = SerieTemporal.de_lista([2, 4, 6]).reamostrar(3)
        self.assertTrue(np.allclose(r, [4.0]))

    def test_k_um_devolve_a_serie(self):
        """k=1 devolve a própria série, como SerieTemporal."""
        s = SerieTemporal.de_lista([5, 7, 9])
        r = s.reamostrar(1)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(r, s))

    def test_nao_modifica_a_serie(self):
        """reamostrar não altera a série original."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        copia = np.array(s)
        s.reamostrar(2)
        self.assertTrue(np.array_equal(s, copia))


class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras do contrato de ler_log que a aceitação não verifica."""

    def test_data_impossivel_e_invalida(self):
        """Linha com mês 13 casa com o padrão, mas é inválida."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=10"
        registros, invalidas = ler_log(linha + "\n")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Linha cujo resto não tem chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT101 semigual"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_linhas_em_branco_sao_ignoradas(self):
        """Linhas vazias ou só com espaços não viram registro nem inválida."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=10\n\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])


if __name__ == "__main__":
    unittest.main()

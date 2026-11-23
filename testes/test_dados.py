"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import ler_log, por_tag, serie, valida_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: testes de regressão da media_movel (escritos antes da correção)."""

    def test_media_movel_tamanho_n_menos_janela_mais_um(self):
        """Série de 5 pontos com janela 2 devolve 4 médias (n - janela + 1)."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertEqual(len(s.media_movel(2)), 4)

    def test_media_movel_valores_incluem_primeira_janela(self):
        """A primeira média é a de self[0:janela]: [1, 2, 3, 4, 5] com janela 2 dá [1.5, 2.5, 3.5, 4.5]."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertTrue(np.allclose(s.media_movel(2), [1.5, 2.5, 3.5, 4.5]))

    def test_media_movel_janela_igual_ao_tamanho(self):
        """Janela igual ao tamanho da série devolve um único valor: a média de tudo."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 4.0)


class TestValidaTag(unittest.TestCase):
    """Issue #1: casos de valida_tag além dos testes de aceitação."""

    def test_tag_valida_duas_letras(self):
        """Tag com duas letras, valida_tag retorna True"""
        self.assertTrue(valida_tag("PT302"))

    def test_tag_valida_uma_letra(self):
        """Tag com uma letra, valida_tag retorna True"""
        self.assertTrue(valida_tag("Z101"))

    def test_tag_invalida_sem_letras(self):
        """Tag sem letras, valida_tag retorna False"""
        self.assertFalse(valida_tag("103"))

    def test_tag_invalida_tres_letras(self):
        """Tag com três letras, valida_tag retorna False"""
        self.assertFalse(valida_tag("PTE103"))

    def test_tag_valida_um_numero(self):
        """Tag com um número, valida_tag retorna True"""
        self.assertTrue(valida_tag("PT3"))

    def test_tag_valida_dois_numeros(self):
        """Tag com dois números, valida_tag retorna True"""
        self.assertTrue(valida_tag("PT30"))

    def test_tag_valida_tres_numeros(self):
        """Tag com três números, valida_tag retorna True"""
        self.assertTrue(valida_tag("PT301"))

    def test_tag_invalida_sem_numeros(self):
        """Tag sem números, valida_tag retorna False"""
        self.assertFalse(valida_tag("PT"))

    def test_tag_invalida_quatro_numeros(self):
        """Tag com quatro números, valida_tag retorna False"""
        self.assertFalse(valida_tag("PT4141"))


class TestReamostrar(unittest.TestCase):
    """Issue #5: casos de reamostrar além dos testes de aceitação."""

    def test_reamostrar_descarta_sobra_no_fim(self):
        """7 pontos com k=3 dão 2 médias; o 7º ponto (sobra) é descartado."""
        r = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 100]).reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_reamostrar_k_igual_ao_tamanho(self):
        """k igual ao tamanho da série devolve um único valor: a média de tudo."""
        r = SerieTemporal.de_lista([2.0, 4.0, 9.0]).reamostrar(3)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(float(r[0]), 5.0)

    def test_reamostrar_nao_modifica_self(self):
        """reamostrar devolve uma SerieTemporal nova e não altera a série original."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        r = s.reamostrar(2)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(s, [1.0, 2.0, 3.0, 4.0]))


class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras do contrato de ler_log que os testes de aceitação não verificam."""

    def test_linha_so_com_espacos_e_ignorada(self):
        """Linhas vazias ou só com espaços são ignoradas e não contam como inválidas."""
        texto = "2026-10-05 08:00:00 INFO PT101 contagens=131\n   \n\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_impossivel_e_invalida(self):
        """Uma data impossível (mês 13) torna a linha inválida."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(linha + "\n")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Uma linha cujo resto não tem nenhum par chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT101 sem_valor"
        registros, invalidas = ler_log(linha + "\n")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_serie_mantem_valor_zero(self):
        """serie inclui leituras com valor 0 (não confunde 0 com chave ausente)."""
        texto = ("2026-10-05 08:00:00 INFO PT101 contagens=0\n"
                 "2026-10-05 08:00:06 INFO PT101 contagens=5\n")
        registros, _ = ler_log(texto)
        self.assertTrue(np.allclose(serie(registros, "PT101", "contagens"), [0.0, 5.0]))


if __name__ == "__main__":
    unittest.main()
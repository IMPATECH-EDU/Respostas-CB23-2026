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


class TestRegressaoMediaMovel(unittest.TestCase):
    """Issue #4: media_movel devolvia um valor a menos (n - janela em vez de n - janela + 1)."""

    def setUp(self):
        self.s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])

    def test_media_movel_tem_n_menos_janela_mais_um_valores(self):
        """Com 5 pontos e janela 2, a média móvel tem 4 valores, como diz a docstring."""
        self.assertEqual(len(self.s.media_movel(2)), 4)

    def test_media_movel_inclui_a_primeira_janela(self):
        """O primeiro valor é a média de self[0:janela]: (1 + 2) / 2 = 1,5."""
        self.assertTrue(np.allclose(self.s.media_movel(2), [1.5, 2.5, 3.5, 4.5]))

    def test_media_movel_janela_igual_ao_tamanho(self):
        """Com janela igual ao tamanho da série, sobra um único valor: a média de tudo."""
        resultado = self.s.media_movel(5)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 3.0)


class TestContratoLerLog(unittest.TestCase):
    """Regras da docstring de ler_log que os testes de aceitação não verificam."""

    VALIDA = "2026-10-05 08:00:00 INFO PT101 contagens=131"

    def test_linhas_branco_nao_invalidadas(self):
        """Linhas vazias ou só com espaços são ignoradas e não entram em `invalidas`."""
        texto = "\n   \n" + self.VALIDA + "\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_impossivel_invalida(self):
        """Linha que casa com LINHA, mas tem mês 13, vai para `invalidas`."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_hora_impossivel_e_invalida(self):
        """Linha com hora 25:00:00 vai para `invalidas`."""
        linha = "2026-10-05 25:00:00 INFO PT101 contagens=131"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_resto_sem_pares_e_invalido(self):
        """Linha onde `resto` não tem nenhum par chave=valor vai para `invalidas`."""
        linha = "2026-10-05 08:00:00 INFO PT101 sem_igual"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_invalidas_preservam_texto_e_ordem(self):
        """As inválidas voltam exatamente como no texto e na ordem em que aparecem."""
        ruins = ["### falha ###", "2026-10-05 08:20:4"]
        texto = "\n".join([ruins[0], self.VALIDA, ruins[1]])
        _, invalidas = ler_log(texto)
        self.assertEqual(invalidas, ruins)


class TestReamostrar(unittest.TestCase):
    """Issue #5: médias de blocos consecutivos de k pontos."""

    def test_sobra_no_fim_e_descartada(self):
        """Com 7 pontos e k = 3, o ponto que sobra no fim é descartado: 2 blocos."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 100.0])
        self.assertTrue(np.allclose(s.reamostrar(3), [2.0, 5.0]))

    def test_k_igual_a_um_devolve_a_propria_serie(self):
        """Com k = 1, cada bloco tem um ponto e o resultado é igual à série."""
        s = SerieTemporal.de_lista([3.0, 1.0, 4.0])
        self.assertTrue(np.allclose(s.reamostrar(1), s))

    def test_reamostrar_nao_modifica_a_serie(self):
        """reamostrar não altera self e devolve uma SerieTemporal."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        r = s.reamostrar(2)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(s, [1.0, 2.0, 3.0, 4.0]))


if __name__ == "__main__":
    unittest.main()

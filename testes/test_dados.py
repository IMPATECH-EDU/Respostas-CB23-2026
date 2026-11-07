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


class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: media_movel deve devolver n - janela + 1 valores, a começar pela 1ª janela."""

    def setUp(self):
        self.rampa = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0, 10.0, 12.0])

    def test_quantidade_de_valores(self):
        """Seis pontos com janela 3 dão 6 - 3 + 1 = 4 médias."""
        self.assertEqual(len(self.rampa.media_movel(3)), 4)

    def test_primeira_janela_presente(self):
        """O primeiro valor é a média de self[0:janela] (2, 4, 6 -> 4)."""
        self.assertTrue(np.allclose(self.rampa.media_movel(3), [4.0, 6.0, 8.0, 10.0]))

    def test_janela_do_tamanho_da_serie(self):
        """Janela igual ao tamanho da série dá um único valor: a média de tudo."""
        resultado = self.rampa.media_movel(len(self.rampa))
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 7.0)

    def test_janela_unitaria_reproduz_a_serie(self):
        """Com janela 1, cada média é o próprio ponto."""
        self.assertTrue(np.allclose(self.rampa.media_movel(1), self.rampa))


class TestReamostrar(unittest.TestCase):
    """Issue #5: médias de blocos consecutivos de k pontos."""

    def test_sobra_no_fim_e_descartada(self):
        """Sete pontos em blocos de 3: duas médias, e o 7º ponto (100) é ignorado."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 100.0])
        r = s.reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_igual_ao_tamanho(self):
        """Com k = len(s) há um só bloco, cuja média é a média da série."""
        s = SerieTemporal.de_lista([3.0, 5.0, 10.0])
        self.assertTrue(np.allclose(s.reamostrar(3), [6.0]))

    def test_nao_modifica_a_serie(self):
        """reamostrar devolve uma SerieTemporal nova e deixa self intacta."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        copia = np.array(s)
        r = s.reamostrar(2)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.array_equal(s, copia))


class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras do contrato de ler_log que os testes de aceitação não verificam."""

    def test_linhas_so_com_espacos_sao_ignoradas(self):
        """Linhas vazias ou só com espaços não viram registro nem linha inválida."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=10\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual((len(registros), invalidas), (1, []))

    def test_data_impossivel_e_invalida(self):
        """Mês 13 casa com o padrão, mas strptime rejeita: a linha vai para invalidas."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=10"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_hora_impossivel_e_invalida(self):
        """25 h também é impossível e a linha é descartada sem exceção."""
        linha = "2026-10-05 25:00:00 INFO PT101 contagens=10"
        self.assertEqual(ler_log(linha)[1], [linha])

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Um resto sem nenhum chave=valor torna a linha inválida."""
        linha = "2026-10-05 08:00:00 WARN B1 bomba desligada"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_valor_nao_numerico_continua_texto(self):
        """Valores que não viram float (como 12a) continuam str; os outros viram float."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO LT301 nivel=47.5 estado=12a")
        self.assertAlmostEqual(registros[0].valores["nivel"], 47.5)
        self.assertEqual(registros[0].valores["estado"], "12a")

    def test_invalidas_preservam_a_linha_original(self):
        """A linha inválida é devolvida exatamente como estava, inclusive com espaços."""
        linha = "  ### falha ###  "
        self.assertEqual(ler_log(linha + "\n")[1], [linha])


if __name__ == "__main__":
    unittest.main()

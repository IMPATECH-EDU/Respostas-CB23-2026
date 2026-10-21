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
class TestMediaMovelRegressaoIssue4(unittest.TestCase):
    """Regressão da issue #4: media_movel devolvia um valor a menos."""

    def test_tamanho_com_600_leituras_e_janela_30(self):
        """Série de 600 pontos com janela 30 deve ter 571 médias (n - janela + 1)."""
        serie = SerieTemporal.de_lista(np.arange(600, dtype=float))
        self.assertEqual(len(serie.media_movel(30)), 571)

    def test_janela_igual_ao_tamanho_da_serie(self):
        """Com janela igual a len(serie), o resultado tem 1 valor: a média de todos os pontos."""
        serie = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0])
        resultado = serie.media_movel(4)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 5.0)

    def test_primeiro_valor_e_a_media_dos_primeiros_pontos(self):
        """O primeiro valor deve ser a média dos primeiros `janela` pontos, e não ser pulado."""
        serie = SerieTemporal.de_lista([1, 5, 9, 7, 3])
        resultado = serie.media_movel(2)
        self.assertEqual(len(resultado), 4)
        self.assertTrue(np.allclose(resultado, [3, 7, 8, 5]))

    def test_janela_1_devolve_a_propria_serie(self):
        """Com janela 1, a média móvel tem o mesmo tamanho e os mesmos valores da série."""
        serie = SerieTemporal.de_lista([3.0, 1.0, 4.0, 1.0, 5.0])
        resultado = serie.media_movel(1)
        self.assertEqual(len(resultado), 5)
        self.assertTrue(np.allclose(resultado, [3, 1, 4, 1, 5]))


class TestReamostrar(unittest.TestCase):
    """Issue #5: SerieTemporal.reamostrar (médias de blocos de k pontos)."""

    def test_sobra_no_fim_e_descartada(self):
        """Com 7 pontos e k=3, o último ponto não completa um bloco e é descartado."""
        resultado = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7]).reamostrar(3)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(np.allclose(resultado, [2, 5]))

    def test_k_igual_ao_tamanho_da_serie(self):
        """Com k igual a len(serie), sobra um único bloco: a média de todos os pontos."""
        resultado = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0]).reamostrar(4)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 5.0)

    def test_medias_por_minuto_de_600_leituras(self):
        """600 leituras a cada 6 s, com k=10, dão 60 médias por minuto."""
        resultado = SerieTemporal.de_lista(np.arange(600, dtype=float)).reamostrar(10)
        self.assertEqual(len(resultado), 60)
        self.assertAlmostEqual(float(resultado[0]), 4.5)
        self.assertAlmostEqual(float(resultado[-1]), 594.5)

    def test_nao_modifica_a_serie_original(self):
        """reamostrar devolve uma SerieTemporal nova e deixa a série original intacta."""
        serie_original = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        copia = np.array(serie_original)
        resultado = serie_original.reamostrar(2)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertTrue(np.array_equal(serie_original, copia))


class TestLerLogRegrasDoContrato(unittest.TestCase):
    """Issue #1: regras de ler_log que os testes de aceitação não verificam."""

    VALIDA = "2026-10-05 08:00:00 INFO PT101 contagens=131"

    def test_linhas_vazias_ou_so_com_espacos_sao_ignoradas(self):
        """Linhas vazias ou só com espaços não viram registro nem contam como inválidas."""
        texto = f"\n   \n{self.VALIDA}\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_ou_hora_impossivel_e_invalida(self):
        """Linha que casa com o padrão, mas tem mês 13 ou hora 25, vai para as inválidas."""
        for linha in ["2026-13-05 08:00:00 INFO PT101 contagens=131",
                      "2026-10-05 25:00:00 INFO PT101 contagens=131"]:
            with self.subTest(linha=linha):
                registros, invalidas = ler_log(linha)
                self.assertEqual(registros, [])
                self.assertEqual(invalidas, [linha])

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Linha cujo resto não tem nenhum par chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT101 sem_par_aqui"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_ordem_e_texto_original_das_invalidas(self):
        """Registros mantêm a ordem do texto e as inválidas voltam exatamente como estavam."""
        lixo = "   ### lixo com espaços ###  "
        segunda = "2026-10-05 08:00:06 INFO PT101 contagens=140"
        registros, invalidas = ler_log(f"{self.VALIDA}\n{lixo}\n{segunda}")
        self.assertEqual([r.valores["contagens"] for r in registros], [131.0, 140.0])
        self.assertEqual(invalidas, [lixo])


if __name__ == "__main__":
    unittest.main()
"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import converter_vetorizado, ler_log, medir_memoria, por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestDescartesDoLog(unittest.TestCase):
    """Condições em que o formato aparente de uma linha engana."""

    def test_calendario_e_relogio(self) -> None:
        """Preserva duas linhas com campos bem formatados, mas instantes impossíveis."""
        data = "2026-02-29 01:00:00 INFO B1 evento=partida"
        hora = "2026-02-28 24:00:00 INFO B1 evento=partida"
        registros, invalidas = ler_log(data + "\n" + hora)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [data, hora])

    def test_restante_sem_pares(self) -> None:
        """Descarta a linha sem chave=valor, preservando seus espaços finais."""
        linha = "2026-02-28 09:00:00 WARN PT101 leitura perdida   "
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_brancos_entre_leituras(self) -> None:
        """Ignora as linhas em branco e conserva a ordem original de duas tags."""
        a = "2026-10-05 08:00:06 INFO PT102 contagens=1900"
        b = "2026-10-05 08:00:00 INFO B1 evento=partida"
        registros, invalidas = ler_log(a + "\n   \n\n" + b)
        self.assertEqual(invalidas, [])
        self.assertEqual([r.tag for r in registros], ["PT102", "B1"])


class TestContagensCompactas(unittest.TestCase):
    """Conversão e validação das contagens de 12 bits."""

    def test_converte_uint16_no_extremo(self) -> None:
        """A contagem máxima converte para 600 kPa mesmo quando armazenada em uint16."""
        dados = np.array([0, 4095], dtype=np.uint16)
        self.assertTrue(np.allclose(converter_vetorizado(dados), [0.0, 600.0]))

    def test_memoria_exige_inteiros(self) -> None:
        """Um vetor de pressões em ponto flutuante não é um vetor de contagens."""
        with self.assertRaises(ValueError):
            medir_memoria(np.array([3.5]))


class TestMediaMovel(unittest.TestCase):
    """Regressões da média móvel que perdia a janela inicial."""

    def test_primeira_janela(self) -> None:
        """Três pares sobrepostos devem produzir três médias, incluindo a primeira."""
        serie = SerieTemporal.de_lista([2, 8, -4, 0])
        medias = serie.media_movel(2)
        self.assertEqual(len(medias), 3)
        self.assertTrue(np.allclose(medias, [5, 2, -2]))

    def test_janela_do_tamanho_da_serie(self) -> None:
        """Uma janela cobrindo a série inteira produz exatamente uma média."""
        medias = SerieTemporal.de_lista([3, 8, 1]).media_movel(3)
        self.assertEqual(len(medias), 1)
        self.assertAlmostEqual(medias[0], 4.0)


class TestMediasDeBlocos(unittest.TestCase):
    """Blocos completos e conservação dos dados de entrada."""

    def test_sobra_fora_da_media(self) -> None:
        """A sobra final não altera a média de nenhum dos dois blocos completos."""
        serie = SerieTemporal.de_lista([2, 4, 6, 10, 1000])
        self.assertTrue(np.allclose(serie.reamostrar(2), [3, 8]))
        self.assertTrue(np.allclose(serie, [2, 4, 6, 10, 1000]))

    def test_bloco_unitario(self) -> None:
        """Blocos de uma leitura preservam os valores e o tipo SerieTemporal."""
        serie = SerieTemporal.de_lista([3, -2, 8])
        blocos = serie.reamostrar(1)
        self.assertIsInstance(blocos, SerieTemporal)
        self.assertTrue(np.allclose(blocos, serie))


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import criar_conversores, ler_log, converter_vetorizado

from elevatoria.serie import SerieTemporal
import numpy as np

from elevatoria.dados import por_tag


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestMediaMovel(unittest.TestCase):
    """Regressões de alinhamento e tamanho da média móvel."""

    def test_inclui_primeira_janela(self) -> None:
        """A primeira média começa no primeiro ponto da série."""
        s = SerieTemporal.de_lista([2, 4, 8, 16])
        self.assertTrue(np.allclose(s.media_movel(2)[0], 3.0))

    def test_janela_do_tamanho_da_serie(self) -> None:
        """Uma janela do tamanho da série produz exatamente uma média."""
        mm = SerieTemporal.de_lista([2, 4, 9]).media_movel(3)
        self.assertIsInstance(mm, SerieTemporal)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 5.0)



class TestLeituraEConversao(unittest.TestCase):
    """Casos de descarte e conversão de leituras."""

    def test_ignora_linhas_em_branco(self) -> None:
        """Linhas vazias ou só com espaços não entram entre as inválidas."""
        self.assertEqual(ler_log("\n   \n"), ([], []))

    def test_rejeita_data_impossivel_e_preserva_texto(self) -> None:
        """Uma data impossível é descartada com os espaços originais."""
        linha = "2026-02-30 08:00:00 INFO PT102 contagens=42  "
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_conversores_sem_escalas(self) -> None:
        """Sem escalas não há funções de conversão."""
        self.assertEqual(criar_conversores({}), {})

    def test_conversao_de_uint16_sem_estouro(self) -> None:
        """A conversão vetorizada não estoura o uint16 na multiplicação."""
        contagens = np.array([0, 4095], dtype=np.uint16)
        self.assertTrue(np.allclose(converter_vetorizado(contagens), [0.0, 600.0]))


class TestReamostragem(unittest.TestCase):
    """Casos de blocos incompletos e de tamanho unitário."""

    def test_descarta_sobra_do_ultimo_bloco(self) -> None:
        """O ponto final fica fora do cálculo quando não completa um bloco."""
        s = SerieTemporal.de_lista([2, 4, 6, 8, 100])
        medias = s.reamostrar(2)
        self.assertIsInstance(medias, SerieTemporal)
        self.assertTrue(np.allclose(medias, [3, 7]))
        self.assertTrue(np.allclose(s, [2, 4, 6, 8, 100]))

    def test_blocos_unitarios(self) -> None:
        """Um ponto por bloco preserva cada valor."""
        s = SerieTemporal.de_lista([2, 1, 9])
        self.assertTrue(np.allclose(s.reamostrar(1), s))


if __name__ == "__main__":
    unittest.main()

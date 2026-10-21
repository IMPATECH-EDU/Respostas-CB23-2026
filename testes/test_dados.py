"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import por_tag
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


if __name__ == "__main__":
    unittest.main()
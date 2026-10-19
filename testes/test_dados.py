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


# Issue #4: regressão da média móvel

class TestMediaMovelRegressao(unittest.TestCase):
    """Testes de regressão da issue #4 (escritos antes da correção)."""

    def test_tamanho_com_janela_pequena(self):
        """Série de 10 pontos e janela 3 devem render 8 médias (n - janela + 1)."""
        s = SerieTemporal.de_lista(range(10))
        self.assertEqual(len(s.media_movel(3)), 8)

    def test_primeira_media_inclui_o_inicio_da_serie(self):
        """A primeira média é a de self[0:janela]; o código com defeito pulava essa janela."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 1.5)

    def test_valores_completos(self):
        """Todos os valores da média móvel conferem com o cálculo direto por fatias."""
        s = SerieTemporal.de_lista([2.0, 4.0, 9.0, 1.0, 7.0])
        esperado = [np.mean(s[i:i + 3]) for i in range(3)]
        self.assertTrue(np.allclose(s.media_movel(3), esperado))

    def test_janela_igual_ao_tamanho(self):
        """Com janela igual a len(s) existe exatamente uma média: a da série inteira."""
        s = SerieTemporal.de_lista([3.0, 5.0, 10.0, 2.0])
        resultado = s.media_movel(4)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 5.0)

    def test_janela_um_devolve_a_propria_serie(self):
        """Com janela 1 a média móvel é igual à série original."""
        s = SerieTemporal.de_lista([7.0, 1.0, 4.0])
        self.assertTrue(np.allclose(s.media_movel(1), s))

    def test_tamanho_de_600_com_janela_30(self):
        """O caso do relato (600 leituras, janela 30) deve render 571 valores."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestMediaMovel(unittest.TestCase):
    """Testes de regressão da média móvel (issue #4)."""

    def test_primeira_janela(self) -> None:
        """A média móvel inclui a primeira janela e tem n - janela + 1 valores."""
        serie = SerieTemporal.de_lista([2, 4, 6, 8])
        resultado = serie.media_movel(2)

        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(len(resultado), 3)
        for valor, esperado in zip(resultado, [3.0, 5.0, 7.0]):
            self.assertAlmostEqual(float(valor), esperado)

    def test_janela_do_tamanho_da_serie(self) -> None:
        """Uma janela do tamanho da série devolve uma única média."""
        serie = SerieTemporal.de_lista([2, 4, 6, 8])
        resultado = serie.media_movel(4)

        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 5.0)


if __name__ == "__main__":
    unittest.main()

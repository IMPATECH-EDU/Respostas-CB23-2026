"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import valida_tag


# class TestPorTagExemplo(unittest.TestCase):
#     """Exemplo do formato. `por_tag` é código existente da base."""

#     def test_lista_vazia(self):
#         """Sem registros, por_tag devolve uma lista vazia."""
#         self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestValidaTagExemplo(unittest.TestCase):
    """Testes de valida_tag."""

    def test_tags_validas_da_docstring(self):
        """Aceita as tags válidas listadas na docstring."""
        for tag in ["PT101", "FT201", "B1"]:
            with self.subTest(tag=tag):
                self.assertTrue(valida_tag(tag))

    def test_tags_invalidas_da_docstring(self):
        """Rejeita as tags inválidas listadas na docstring."""
        for tag in ["pt101", "PT", "PT1010", "101PT", "PT101 "]:
            with self.subTest(tag=tag):
                self.assertFalse(valida_tag(tag))

    def test_string_vazia(self):
        """Uma string vazia não é uma tag."""
        self.assertFalse(valida_tag(""))

    def test_quebra_de_linha_no_fim(self):
        """Uma quebra de linha no fim da string a invalida."""
        self.assertFalse(valida_tag("PT101\n"))


if __name__ == "__main__":
    unittest.main()

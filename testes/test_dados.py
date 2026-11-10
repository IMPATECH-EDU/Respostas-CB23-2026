"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag, valida_tag


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestValidaTag(unittest.TestCase):
    def test_tag_valida_duas_letras(self):
        """Tag com duas letras, valida_tag retorna True"""
        self.assertTrue(valida_tag("PT302"), [])

    def test_tag_valida_uma_letra(self):
        """Tag com uma letra, valida_tag retorna True"""
        self.assertTrue(valida_tag("Z101"), [])

    def test_tag_invalida_sem_letras(self):
        """Tag sem letras, valida_tag retorna False"""
        self.assertFalse(valida_tag("103"), [])

    def test_tag_invalida_tres_letras(self):
        """Tag com três letras, valida_tag retorna False"""
        self.assertFalse(valida_tag("PTE103"), [])

    def test_tag_valida_um_numero(self):
        """Tag com um número, valida_tag retorna True"""
        self.assertTrue(valida_tag("PT3"), [])

    def test_tag_valida_dois_numeros(self):
        """Tag com dois números, valida_tag retorna True"""
        self.assertTrue(valida_tag("PT30"), [])

    def test_tag_valida_tres_numeros(self):
        """Tag com três números, valida_tag retorna True"""
        self.assertTrue(valida_tag("PT301"), [])

    def test_tag_invalida_sem_numeros(self):
        """Tag sem números, valida_tag retorna False"""
        self.assertFalse(valida_tag("PT"), [])

    def test_tag_invalida_quatro_numeros(self):
        """Tag com quatro números, valida_tag retorna False"""
        self.assertFalse(valida_tag("PT4141"), [])


if __name__ == "__main__":
    unittest.main()

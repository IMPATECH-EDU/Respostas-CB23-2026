"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import ler_log, por_tag

class TestLerLogAdicionais(unittest.TestCase):
    """Regras para o contrato de ler_log que os testes de aceitação não verificam."""

    def test_data_impossivel(self):
        """Uma linha com mês impossível casa com LINHA, mas vai para as inválidas."""
        valida = "2026-10-05 08:00:00 INFO PT101 contagens=131"
        impossivel = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(valida + "\n" + impossivel)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [impossivel])
    def test_ignorar_linha_so_com_espacos(self):
        """Linha só com espaços não vira registro nem entra nas inválidas."""
        valida = "2026-10-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(valida + "\n   \n")
        self.assertEqual(len(registros), 1)
        self.assertEqual(len(invalidas), 0)


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

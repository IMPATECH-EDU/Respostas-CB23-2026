"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import ler_log, por_tag


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestContratoLerLog(unittest.TestCase):
    """Regras da docstring de ler_log que os testes de aceitação não verificam."""

    VALIDA = "2026-10-05 08:00:00 INFO PT101 contagens=131"

    def linhas_branco_nao_invalidadas(self):
        """Linhas vazias ou só com espaços são ignoradas e não entram em `invalidas`."""
        texto = "\n   \n" + self.VALIDA + "\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def data_impossivel_invalida(self):
        """Linha que casa com LINHA, mas tem mês 13, vai para `invalidas`."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def hora_impossivel_e_invalida(self):
        """Linha com hora 25:00:00 vai para `invalidas`."""
        linha = "2026-10-05 25:00:00 INFO PT101 contagens=131"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def resto_sem_pares_e_invalido(self):
        """Linha onde `resto` não tem nenhum par chave=valor vai para `invalidas`."""
        linha = "2026-10-05 08:00:00 INFO PT101 sem_igual"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def invalidas_preservam_texto_e_ordem(self):
        """As inválidas voltam exatamente como no texto e na ordem em que aparecem."""
        ruins = ["### falha ###", "2026-10-05 08:20:4"]
        texto = "\n".join([ruins[0], self.VALIDA, ruins[1]])
        _, invalidas = ler_log(texto)
        self.assertEqual(invalidas, ruins)


if __name__ == "__main__":
    unittest.main()

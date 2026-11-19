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


class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras de ler_log que os testes de aceitação não conferem."""

    def test_linhas_em_branco_nao_sao_invalidas(self):
        """Linhas vazias ou só com espaços são puladas e não entram em invalidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=131\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual((len(registros), invalidas), (1, []))

    def test_data_ou_hora_impossivel(self):
        """Mês 13 e hora 25 casam com LINHA, mas a linha vai para invalidas."""
        linhas = ["2026-13-05 08:00:00 INFO PT101 contagens=131",
                  "2026-10-05 25:00:00 INFO PT101 contagens=131"]
        self.assertEqual(ler_log("\n".join(linhas)), ([], linhas))

    def test_resto_sem_par_chave_valor(self):
        """Linha cujo resto não tem nenhum par chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 WARN B1 vibracao alta"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_invalida_volta_como_estava(self):
        """A linha descartada volta sem strip, com os espaços do começo."""
        linha = "  2026-10-05 08:00:00 INFO PT101 contagens=131"
        self.assertEqual(ler_log(linha)[1], [linha])

    def test_digitos_de_largura_total(self):
        """Data com dígitos de largura total (２０２６) é inválida, apesar do strptime aceitar."""
        linha = "２０２６-10-05 08:00:00 INFO PT101 contagens=131"
        self.assertEqual(ler_log(linha)[1], [linha])


if __name__ == "__main__":
    unittest.main()

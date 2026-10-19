"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import criar_conversores, ler_log, por_tag, serie


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# ---------------------------------------------------------------------------------------
# Issue #1: regras do contrato de ler_log que os testes de aceitação não verificam
# ---------------------------------------------------------------------------------------
class TestLerLogContrato(unittest.TestCase):
    """Issue #1: casos de borda do leitor do log."""

    def test_linhas_em_branco_nao_sao_invalidas(self):
        """Linhas vazias ou só com espaços são puladas e não entram em `invalidas`."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=131\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual((len(registros), invalidas), (1, []))

    def test_data_ou_hora_impossivel(self):
        """Mês 13 e hora 25 casam com o padrão, mas o strptime recusa: a linha é inválida."""
        ruins = ["2026-13-05 08:00:00 INFO PT101 contagens=131",
                 "2026-10-05 25:00:00 INFO PT101 contagens=131"]
        registros, invalidas = ler_log("\n".join(ruins))
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, ruins)

    def test_resto_sem_nenhum_par(self):
        """Uma linha bem formada mas sem nenhum chave=valor no resto é inválida."""
        linha = "2026-10-05 08:00:00 WARN B1 vibracao_alta"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_invalida_guardada_sem_alteracao(self):
        """A linha descartada volta exatamente como estava, com os espaços das pontas."""
        linha = "  ### falha de comunicacao com a RTU ###  "
        self.assertEqual(ler_log(linha + "\n")[1], [linha])

    def test_separadores_com_varios_espacos_e_tab(self):
        """Os campos podem vir separados por vários espaços ou tabs."""
        registros, invalidas = ler_log("2026-10-05  08:00:06\tINFO   LT301 nivel=47.01")
        self.assertEqual(invalidas, [])
        self.assertAlmostEqual(registros[0].valores["nivel"], 47.01)

    def test_serie_de_chave_nao_numerica(self):
        """Pedir a série de uma chave com texto (evento de B1) levanta ValueError."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5")
        with self.assertRaises(ValueError):
            serie(registros, "B1", "evento")


# ---------------------------------------------------------------------------------------
# Issue #2: conversores
# ---------------------------------------------------------------------------------------
class TestConversores(unittest.TestCase):
    """Issue #2: cada conversor com o seu fator."""

    def test_conversores_independentes_da_ordem(self):
        """Cada conversor usa o seu fator mesmo quando o último fator do dicionário é outro."""
        conv = criar_conversores({"PT101": 2.0, "FT201": 0.1})
        self.assertAlmostEqual(conv["PT101"](4095), 8190.0)
        self.assertAlmostEqual(conv["FT201"](4095), 409.5)


if __name__ == "__main__":
    unittest.main()

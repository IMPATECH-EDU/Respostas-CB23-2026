"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import ler_log, por_tag, serie, valida_tag


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestContratoLerLog(unittest.TestCase):
    """Regras de ler_log que a aceitação não cobre."""

    VALIDA = "2026-10-05 08:00:00 INFO PT101 contagens=131"

    def test_linhas_vazias_nao_sao_invalidas(self):
        """Linhas vazias ou só com espaços são ignoradas, não contam como inválidas."""
        registros, invalidas = ler_log(f"\n   \n{self.VALIDA}\n\t\n")
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_impossivel_e_invalida(self):
        """Mês 13 deixa a linha inválida, e ela volta sem alteração."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(f"{linha}\n{self.VALIDA}")
        self.assertEqual(invalidas, [linha])
        self.assertEqual(len(registros), 1)

    def test_hora_impossivel_e_invalida(self):
        """Hora 25 também é descartada."""
        linha = "2026-10-05 25:00:00 INFO PT101 contagens=131"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Sem nenhum par chave=valor, a linha é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT101 sem pares aqui"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_final_de_linha_do_windows(self):
        """Final de linha \\r\\n não deixa o \\r no valor."""
        registros, invalidas = ler_log(f"{self.VALIDA}\r\n{self.VALIDA}\r\n")
        self.assertEqual((len(registros), invalidas), (2, []))
        self.assertEqual(registros[0].valores, {"contagens": 131.0})

    def test_valor_com_ponto_decimal_vira_float(self):
        """Número vira float e 'partida' continua str."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5")
        self.assertAlmostEqual(registros[0].valores["corrente"], 47.5)
        self.assertEqual(registros[0].valores["evento"], "partida")

    def test_tag_valida_so_com_a_string_inteira(self):
        """valida_tag rejeita tag seguida de quebra de linha."""
        self.assertTrue(valida_tag("B1"))
        self.assertFalse(valida_tag("B1\n"))


class TestSerieDoLog(unittest.TestCase):
    """Função `serie`."""

    TEXTO = ("2026-10-05 08:00:00 INFO PT102 contagens=10\n"
             "2026-10-05 08:00:06 ALARME PT102 evento=pressao_alta limite=2000\n"
             "2026-10-05 08:00:12 INFO PT102 contagens=12\n")

    def test_chave_de_texto_levanta_erro(self):
        """Chave de texto (evento) levanta ValueError."""
        registros, _ = ler_log(self.TEXTO)
        with self.assertRaises(ValueError):
            serie(registros, "PT102", "evento")

    def test_tag_sem_registros_da_serie_vazia(self):
        """Tag ausente do log dá série vazia."""
        registros, _ = ler_log(self.TEXTO)
        self.assertEqual(len(serie(registros, "PT101", "contagens")), 0)


if __name__ == "__main__":
    unittest.main()

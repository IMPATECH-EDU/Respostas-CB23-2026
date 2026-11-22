"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import math
import unittest

import numpy as np

from elevatoria.dados import (contagem_por_tag, criar_conversores, ler_log, medir_memoria,
                              por_tag, serie, valida_tag)
from elevatoria.serie import SerieTemporal

#: Início comum das linhas de log montadas nos testes.
_CABECALHO = "2026-10-05 08:00:00 INFO "


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# ---------------------------------------------------------------------------------------
# Issue #1: regras do contrato de ler_log que os testes de aceitação não verificam
# ---------------------------------------------------------------------------------------
class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras de ler_log ausentes dos testes de aceitação."""

    def test_linhas_em_branco_nao_contam_como_invalidas(self):
        """Linhas vazias ou só com espaços/tabulações são ignoradas sem ir para `invalidas`."""
        texto = f"\n   \n{_CABECALHO}PT101 contagens=10\n\t\n\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_ou_hora_impossivel_e_invalida(self):
        """Linhas que casam com LINHA mas têm mês 13, hora 25 ou 30 de fevereiro são descartadas."""
        ruins = ["2026-13-05 08:00:00 INFO PT101 contagens=10",
                 "2026-10-05 25:00:00 INFO PT101 contagens=10",
                 "2026-02-30 08:00:00 INFO PT101 contagens=10"]
        registros, invalidas = ler_log("\n".join(ruins))
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, ruins)

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Uma linha cujo `resto` não tem nenhum `chave=valor` é inválida."""
        linha = f"{_CABECALHO}PT101 leitura sem pares"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_invalida_preservada_exatamente_como_no_texto(self):
        """A linha descartada volta sem strip: espaços nas pontas são mantidos."""
        linha = "   ### falha de comunicacao com a RTU ###  "
        _, invalidas = ler_log(f"{_CABECALHO}PT101 contagens=1\n{linha}\n")
        self.assertEqual(invalidas, [linha])

    def test_varios_pares_e_conversao_parcial(self):
        """Num mesmo registro, valores numéricos viram float e os demais continuam str."""
        registros, _ = ler_log(f"{_CABECALHO}B1 evento=vibracao corrente=49.8 fase=-3")
        valores = registros[0].valores
        self.assertEqual(set(valores), {"evento", "corrente", "fase"})
        self.assertEqual(valores["evento"], "vibracao")
        self.assertAlmostEqual(valores["corrente"], 49.8)
        self.assertAlmostEqual(valores["fase"], -3.0)

    def test_tag_com_digitos_demais_invalida_a_linha(self):
        """Uma tag que valida_tag rejeita (PT1010) também torna a linha inválida."""
        linha = f"{_CABECALHO}PT1010 contagens=1"
        self.assertFalse(valida_tag("PT1010"))
        self.assertEqual(ler_log(linha), ([], [linha]))


class TestContagemESerieExtras(unittest.TestCase):
    """Issue #1: casos de contagem_por_tag e serie fora dos testes de aceitação."""

    def test_contagem_por_tag_soma_o_total(self):
        """A soma das contagens por tag é o número total de registros."""
        texto = "\n".join(f"{_CABECALHO}{tag} x={i}"
                          for i, tag in enumerate(["B1", "PT101", "B1", "LT301", "B1"]))
        registros, _ = ler_log(texto)
        contagem = contagem_por_tag(registros)
        self.assertEqual(contagem, {"B1": 3, "PT101": 1, "LT301": 1})
        self.assertEqual(sum(contagem.values()), len(registros))

    def test_serie_de_tag_inexistente_e_vazia(self):
        """serie de uma tag sem registros devolve uma SerieTemporal vazia."""
        registros, _ = ler_log(f"{_CABECALHO}PT101 contagens=10")
        s = serie(registros, "FT201", "pulsos")
        self.assertIsInstance(s, SerieTemporal)
        self.assertEqual(len(s), 0)

    def test_serie_de_chave_textual_levanta_value_error(self):
        """serie de uma chave com valor textual (evento=partida) levanta ValueError."""
        registros, _ = ler_log(f"{_CABECALHO}B1 evento=partida corrente=47.5")
        with self.assertRaises(ValueError):
            serie(registros, "B1", "evento")
        self.assertTrue(np.allclose(serie(registros, "B1", "corrente"), [47.5]))


if __name__ == "__main__":
    unittest.main()
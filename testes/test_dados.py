"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import ler_log, por_tag, serie
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestLerLogContrato(unittest.TestCase):
    """Regras de leitura não verificadas pelos testes de aceitação."""

    def test_ignora_linhas_em_branco(self) -> None:
        """Linhas vazias ou só com espaços não entram nos registros nem nas inválidas."""
        registros, invalidas = ler_log("\n   \n\t\n")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [])

    def test_descarta_datas_e_horas_impossiveis(self) -> None:
        """Datas e horas impossíveis são descartadas mesmo com formato correto."""
        for instante in ["2026-13-05 08:00:00", "2026-02-30 08:00:00",
                         "2026-10-05 24:00:00", "2026-10-05 08:60:00"]:
            with self.subTest(instante=instante):
                linha = f"{instante} INFO PT102 contagens=10"
                registros, invalidas = ler_log(linha)
                self.assertEqual(registros, [])
                self.assertEqual(invalidas, [linha])

    def test_descarta_linhas_sem_pares(self) -> None:
        """Uma linha sem nenhum par chave=valor é inválida."""
        for resto in ["sem pares", "contagens=", "   "]:
            with self.subTest(resto=resto):
                linha = f"2026-10-05 08:00:00 INFO PT102 {resto}"
                registros, invalidas = ler_log(linha)
                self.assertEqual(registros, [])
                self.assertEqual(invalidas, [linha])

    def test_preserva_linhas_invalidas_sem_strip(self) -> None:
        """Linhas inválidas mantêm seus espaços e a ordem original."""
        linhas = ["  falha de comunicacao  ",
                  "2026-10-05 08:00:00 DEBUG PT102 contagens=10  "]
        registros, invalidas = ler_log("\n".join(linhas))
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, linhas)


class TestSerieContrato(unittest.TestCase):
    """Seleção dos valores numéricos para uma série temporal."""

    def test_preserva_ordem_e_filtra_tag_e_chave(self) -> None:
        """A série preserva a ordem de entrada e ignora outras tags e chaves ausentes."""
        registros, _ = ler_log(
            "2026-10-05 08:00:06 INFO PT102 contagens=20\n"
            "2026-10-05 08:00:00 INFO PT101 contagens=999\n"
            "2026-10-05 08:00:00 ALARME PT102 evento=pressao_alta\n"
            "2026-10-05 08:00:00 INFO PT102 contagens=10\n"
        )
        resultado = serie(registros, "PT102", "contagens")
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertTrue(np.allclose(resultado, [20.0, 10.0]))

    def test_sem_valores_produz_serie_vazia(self) -> None:
        """Sem registros correspondentes, o retorno continua sendo uma SerieTemporal vazia."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO PT102 evento=partida")
        for tag, chave in [("PT101", "contagens"), ("PT102", "contagens")]:
            with self.subTest(tag=tag, chave=chave):
                resultado = serie(registros, tag, chave)
                self.assertIsInstance(resultado, SerieTemporal)
                self.assertEqual(resultado.size, 0)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])



import numpy as np
from elevatoria.serie import SerieTemporal


class TestMediaMovelRegressao(unittest.TestCase):
    """Regressões da issue #4, inclusive janelas nas extremidades."""

    def test_primeira_janela_preservada(self) -> None:
        """A primeira média aparece e o resultado tem n - janela + 1 pontos."""
        s = SerieTemporal.de_lista([2, 8, 5, 17])
        resultado = s.media_movel(2)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(np.allclose(resultado, [5, 6.5, 11]))
        self.assertTrue(np.allclose(s, [2, 8, 5, 17]))

    def test_janela_igual_serie(self) -> None:
        """Uma janela que ocupa toda a série produz sua média em um único ponto."""
        resultado = SerieTemporal.de_lista([3, 8, 13]).media_movel(3)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 8.0)

    def test_janela_unitaria(self) -> None:
        """Janela unitária conserva todos os valores, inclusive o primeiro."""
        s = SerieTemporal.de_lista([9, -2, 4])
        resultado = s.media_movel(1)
        self.assertEqual(len(resultado), len(s))
        self.assertTrue(np.allclose(resultado, s))

from elevatoria.dados import (ler_log, serie, criar_conversores, medir_memoria,
                              converter_vetorizado)


class TestContratosDados(unittest.TestCase):
    """Casos de leitura, conversão e reamostragem além da aceitação."""

    def test_datas_e_horas_impossiveis(self) -> None:
        """Datas e horas impossíveis são devolvidas intactas entre as inválidas."""
        linhas = [f"{data} {hora} INFO B1 evento=partida  " for data, hora in
                  [("2026-02-29", "08:00:00"), ("2026-13-01", "08:00:00"),
                   ("2026-10-05", "24:00:00"), ("2026-10-05", "08:60:00")]]
        registros, invalidas = ler_log("\n".join(linhas))
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, linhas)

    def test_resto_sem_pares(self) -> None:
        """Uma linha com cabeçalho válido mas sem chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 INFO B1 evento= falha"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_espacos_em_branco_ignorados(self) -> None:
        """Linhas vazias ou só com espaços não são contadas como inválidas."""
        self.assertEqual(ler_log("\n  \n\t\n"), ([], []))

    def test_expoente_sinal_e_texto(self) -> None:
        """Valores numéricos com sinal e expoente viram float, preservando os textos."""
        regs, erros = ler_log("2026-10-05 08:00:00 INFO B1 a=-2.5e2 b=+3 evento=partida")
        self.assertEqual(erros, [])
        self.assertAlmostEqual(regs[0].valores["a"], -250.0)
        self.assertAlmostEqual(regs[0].valores["b"], 3.0)
        self.assertEqual(regs[0].valores["evento"], "partida")

    def test_reamostrar_descarta_sobra(self) -> None:
        """A sobra não completa um bloco e não altera as médias nem a série original."""
        s = SerieTemporal.de_lista([3, 9, -1, 7, 1000])
        resultado = s.reamostrar(2)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertTrue(np.allclose(resultado, [6, 3]))
        self.assertTrue(np.allclose(s, [3, 9, -1, 7, 1000]))

    def test_reamostrar_bloco_unico(self) -> None:
        """Um bloco do tamanho da série devolve exatamente uma média."""
        resultado = SerieTemporal.de_lista([-4, 2, 11]).reamostrar(3)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 3.0)

    def test_serie_sem_chave_numerica(self) -> None:
        """Uma tag com apenas eventos gera uma série vazia, com o tipo correto."""
        regs, _ = ler_log("2026-10-05 08:00:00 ALARME PT102 evento=pressao_alta")
        resultado = serie(regs, "PT102", "contagens")
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertEqual(resultado.size, 0)

    def test_conversores_independentes(self) -> None:
        """Fatores zero e negativos são capturados sem depender de alterações posteriores."""
        escalas = {"A1": 0.0, "B2": -3.5, "C3": 0.25}
        conversores = criar_conversores(escalas)
        escalas["B2"] = 8.0
        for tag, esperado in [("A1", 0.0), ("B2", -14.0), ("C3", 1.0)]:
            with self.subTest(tag=tag):
                self.assertAlmostEqual(conversores[tag](4), esperado)

    def test_memoria_rejeita_entradas_invalidas(self) -> None:
        """Lista comum, floats e contagens fora da faixa não são aceitos."""
        for entrada in ([1, 2], np.array([1.5]), np.array([-1]), np.array([4096])):
            with self.subTest(entrada=entrada), self.assertRaises(ValueError):
                medir_memoria(entrada)

    def test_vetorizado_nao_estoura_uint16(self) -> None:
        """A conversão promove uint16 antes da multiplicação e preserva a entrada."""
        entrada = np.array([0, 2048, 4095], dtype=np.uint16)
        resultado = converter_vetorizado(entrada)
        self.assertTrue(np.allclose(resultado, [0, 2048 * 600 / 4095, 600]))
        self.assertTrue(np.allclose(entrada, [0, 2048, 4095]))


if __name__ == "__main__":
    unittest.main()

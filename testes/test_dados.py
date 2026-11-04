"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import (contagem_por_tag, criar_conversores, ler_log, medir_memoria,
                              por_tag, serie, valida_tag)
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Issue #4: regressão da média móvel

class TestMediaMovelRegressao(unittest.TestCase):
    """Testes de regressão da issue #4 (escritos antes da correção)."""

    def test_tamanho_com_janela_pequena(self):
        """Série de 10 pontos e janela 3 devem render 8 médias (n - janela + 1)."""
        s = SerieTemporal.de_lista(range(10))
        self.assertEqual(len(s.media_movel(3)), 8)

    def test_primeira_media_inclui_o_inicio_da_serie(self):
        """A primeira média é a de self[0:janela]; o código com defeito pulava essa janela."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 1.5)

    def test_valores_completos(self):
        """Todos os valores da média móvel conferem com o cálculo direto por fatias."""
        s = SerieTemporal.de_lista([2.0, 4.0, 9.0, 1.0, 7.0])
        esperado = [np.mean(s[i:i + 3]) for i in range(3)]
        self.assertTrue(np.allclose(s.media_movel(3), esperado))

    def test_janela_igual_ao_tamanho(self):
        """Com janela igual a len(s) existe exatamente uma média: a da série inteira."""
        s = SerieTemporal.de_lista([3.0, 5.0, 10.0, 2.0])
        resultado = s.media_movel(4)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 5.0)

    def test_janela_um_devolve_a_propria_serie(self):
        """Com janela 1 a média móvel é igual à série original."""
        s = SerieTemporal.de_lista([7.0, 1.0, 4.0])
        self.assertTrue(np.allclose(s.media_movel(1), s))

    def test_tamanho_de_600_com_janela_30(self):
        """O caso do relato (600 leituras, janela 30) deve render 571 valores."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)


class TestMediaMovelContrato(unittest.TestCase):
    """Contrato de media_movel: tipo, erros e ausência de efeitos colaterais."""

    def test_tipo_de_retorno(self):
        """O resultado continua sendo uma SerieTemporal."""
        s = SerieTemporal.de_lista([1, 2, 3, 4])
        self.assertIsInstance(s.media_movel(2), SerieTemporal)

    def test_janela_invalida_levanta_value_error(self):
        """Janela menor que 1 ou maior que len(s) levanta ValueError."""
        s = SerieTemporal.de_lista([1, 2, 3])
        with self.assertRaises(ValueError):
            s.media_movel(0)
        with self.assertRaises(ValueError):
            s.media_movel(4)

    def test_nao_modifica_self(self):
        """Depois de media_movel a série original permanece igual."""
        s = SerieTemporal.de_lista([5.0, 1.0, 8.0, 2.0])
        copia = np.array(s)
        s.media_movel(2)
        self.assertTrue(np.array_equal(s, copia))


# Issue #5: reamostrar

class TestReamostrar(unittest.TestCase):
    """Médias por bloco de reamostrar."""

    def test_blocos_exatos(self):
        """Seis pontos em blocos de 2 rendem três médias."""
        s = SerieTemporal.de_lista([1, 3, 5, 7, 9, 11])
        self.assertTrue(np.allclose(s.reamostrar(2), [2.0, 6.0, 10.0]))

    def test_sobra_no_fim_e_descartada(self):
        """Sete pontos em blocos de 3 rendem duas médias; o último ponto é descartado."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 100])
        resultado = s.reamostrar(3)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(np.allclose(resultado, [2.0, 5.0]))

    def test_k_igual_ao_tamanho(self):
        """Com k igual a len(s) sai uma única média, a da série toda."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0])
        self.assertTrue(np.allclose(s.reamostrar(3), [4.0]))

    def test_k_invalido_levanta_value_error(self):
        """k menor que 1 ou maior que len(s) levanta ValueError."""
        s = SerieTemporal.de_lista([1, 2, 3])
        with self.assertRaises(ValueError):
            s.reamostrar(0)
        with self.assertRaises(ValueError):
            s.reamostrar(4)

    def test_tipo_e_nao_modifica_self(self):
        """O resultado é SerieTemporal e a série original não muda."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        copia = np.array(s)
        resultado = s.reamostrar(2)
        self.assertIsInstance(resultado, SerieTemporal)
        self.assertTrue(np.array_equal(s, copia))


# Issue #1: regras do contrato de ler_log que os testes de aceitação não cobrem

class TestLerLogContrato(unittest.TestCase):
    """Regras de ler_log (linhas em branco, datas impossíveis, pares, ordem)."""

    def test_texto_vazio(self):
        """Texto vazio devolve duas listas vazias."""
        self.assertEqual(ler_log(""), ([], []))

    def test_linhas_em_branco_nao_sao_invalidas(self):
        """Linhas vazias ou só com espaços são ignoradas e não entram em invalidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=10\n\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_mes_impossivel_e_invalido(self):
        """Uma linha com mês 13 casa com o padrão, mas é descartada como inválida."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=10"
        registros, invalidas = ler_log(linha + "\n")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Se o resto não tem nenhum par chave=valor, a linha é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT101 sem pares aqui"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_conversao_float_e_str(self):
        """Valores numéricos viram float e os demais continuam str."""
        texto = "2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5\n"
        registros, _ = ler_log(texto)
        valores = registros[0].valores
        self.assertEqual(valores["evento"], "partida")
        self.assertIsInstance(valores["corrente"], float)
        self.assertAlmostEqual(valores["corrente"], 47.5)

    def test_ordem_original_e_linhas_invalidas_intactas(self):
        """Registros mantêm a ordem do texto e as inválidas saem exatamente como entraram."""
        texto = ("2026-10-05 08:00:06 INFO PT101 contagens=2\n"
                 "### falha de comunicacao com a RTU ###\n"
                 "2026-10-05 08:00:00 INFO PT101 contagens=1\n")
        registros, invalidas = ler_log(texto)
        self.assertEqual([r.valores["contagens"] for r in registros], [2.0, 1.0])
        self.assertEqual(invalidas, ["### falha de comunicacao com a RTU ###"])

    def test_nivel_desconhecido_e_invalido(self):
        """Um nível fora de INFO, WARN e ALARME torna a linha inválida."""
        linha = "2026-10-05 08:00:00 DEBUG PT101 contagens=10"
        self.assertEqual(ler_log(linha), ([], [linha]))


# Outras funções do módulo dados

class TestValidaTag(unittest.TestCase):
    """valida_tag usa fullmatch: a string inteira precisa ser uma tag."""

    def test_tags_validas(self):
        """Exemplos de tags válidas são aceitos."""
        for tag in ["PT101", "FT201", "B1", "LT301", "AB12"]:
            self.assertTrue(valida_tag(tag), tag)

    def test_tags_invalidas(self):
        """Minúsculas, sem dígitos, dígitos demais, ordem trocada e espaço final são rejeitados."""
        for tag in ["pt101", "PT", "PT1010", "101PT", "PT101 ", "ABC1", "", "P T1"]:
            self.assertFalse(valida_tag(tag), repr(tag))


class TestContagemESerie(unittest.TestCase):
    """contagem_por_tag e serie sobre um log pequeno."""

    TEXTO = ("2026-10-05 08:00:00 INFO PT102 contagens=100\n"
             "2026-10-05 08:00:06 ALARME PT102 evento=pressao_alta limite=2000\n"
             "2026-10-05 08:00:06 INFO PT102 contagens=300\n"
             "2026-10-05 08:00:06 INFO FT201 pulsos=50\n")

    def test_contagem_por_tag(self):
        """Cada tag recebe o número de registros dela, e lista vazia dá dicionário vazio."""
        registros, _ = ler_log(self.TEXTO)
        self.assertEqual(contagem_por_tag(registros), {"PT102": 3, "FT201": 1})
        self.assertEqual(contagem_por_tag([]), {})

    def test_serie_ignora_registros_sem_a_chave(self):
        """O alarme de PT102 não tem 'contagens' e não entra na série."""
        registros, _ = ler_log(self.TEXTO)
        s = serie(registros, "PT102", "contagens")
        self.assertIsInstance(s, SerieTemporal)
        self.assertTrue(np.allclose(s, [100.0, 300.0]))


class TestConversores(unittest.TestCase):
    """criar_conversores: cada função usa o fator da sua própria tag."""

    def test_fator_de_cada_tag(self):
        """Com três fatores diferentes, cada conversor multiplica pelo seu."""
        conv = criar_conversores({"A": 2.0, "B": 10.0, "C": 0.5})
        self.assertAlmostEqual(conv["A"](3), 6.0)
        self.assertAlmostEqual(conv["B"](3), 30.0)
        self.assertAlmostEqual(conv["C"](3), 1.5)


class TestMedirMemoria(unittest.TestCase):
    """medir_memoria: valores esperados e validação da entrada."""

    def test_bytes_dos_ndarrays(self):
        """Para mil elementos, uint16 ocupa 2000 bytes e float64 ocupa 8000."""
        m = medir_memoria(np.arange(1000) % 4096)
        self.assertEqual(m["uint16"], 2000)
        self.assertEqual(m["int32"], 4000)
        self.assertEqual(m["float64"], 8000)
        self.assertEqual(m["array('H')"], 2000)

    def test_entrada_invalida(self):
        """Entrada que não é ndarray 1D de inteiros levanta ValueError."""
        for ruim in [[1, 2, 3], np.zeros((2, 2), dtype=int), np.array([1.5, 2.5])]:
            with self.assertRaises(ValueError):
                medir_memoria(ruim)


if __name__ == "__main__":
    unittest.main()

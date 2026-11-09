"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
from datetime import datetime

import numpy as np

from elevatoria.dados import (converter_vetorizado, criar_conversores, ler_log, medir_memoria,
                              por_tag, serie, valida_tag)
from elevatoria.serie import SerieTemporal

LINHA_VALIDA = "2026-10-05 08:00:00 INFO PT102 contagens=1623"


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: a média móvel deve ter n - janela + 1 valores."""

    def test_tamanho_do_relato(self) -> None:
        """600 leituras com janela de 30 dão 571 médias, como no relato da issue."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_primeira_janela_presente(self) -> None:
        """O primeiro valor é a média de self[0:janela], que o defeito perdia."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        self.assertTrue(np.allclose(s.media_movel(2), [1.5, 2.5, 3.5]))

    def test_janela_do_tamanho_da_serie(self) -> None:
        """Com janela == len(s), o resultado é um único valor: a média da série."""
        medias = SerieTemporal.de_lista([2.0, 4.0, 9.0]).media_movel(3)
        self.assertEqual(len(medias), 1)
        self.assertAlmostEqual(float(medias[0]), 5.0)

    def test_janela_unitaria(self) -> None:
        """Com janela 1, cada média é o próprio ponto."""
        s = SerieTemporal.de_lista([7.0, -1.0, 3.5])
        self.assertTrue(np.allclose(s.media_movel(1), s))

    def test_mantem_o_tipo_e_nao_altera_a_serie(self) -> None:
        """A correção devolve SerieTemporal e deixa a série original intacta."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0])
        medias = s.media_movel(2)
        self.assertIsInstance(medias, SerieTemporal)
        self.assertTrue(np.array_equal(s, [1.0, 2.0, 3.0]))


class TestReamostrar(unittest.TestCase):
    """Issue #5: casos de reamostrar além dos testes de aceitação."""

    def test_sobra_no_fim_descartada(self) -> None:
        """Os pontos que não completam um bloco não entram em nenhuma média."""
        r = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 1000.0]).reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_k_igual_ao_tamanho(self) -> None:
        """Com k == len(s), há um único bloco: a série inteira."""
        r = SerieTemporal.de_lista([2.0, 4.0, 9.0]).reamostrar(3)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(float(r[0]), 5.0)

    def test_k_unitario(self) -> None:
        """Com k == 1, cada bloco é o próprio ponto."""
        s = SerieTemporal.de_lista([7.0, -1.0, 3.5])
        r = s.reamostrar(1)
        self.assertEqual(len(r), 3)
        self.assertTrue(np.allclose(r, s))

    def test_nao_altera_a_serie(self) -> None:
        """reamostrar devolve 1D e preserva o formato e os valores de self."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        r = s.reamostrar(2)
        self.assertEqual(r.ndim, 1)
        self.assertTrue(np.array_equal(s, [1.0, 2.0, 3.0, 4.0, 5.0]))


class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras do contrato de ler_log que os testes de aceitação não verificam."""

    def test_linhas_em_branco_nao_contam(self) -> None:
        """Linhas vazias ou só com espaços não viram registro nem inválida."""
        registros, invalidas = ler_log(f"\n   \n{LINHA_VALIDA}\n\t\n")
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_e_hora_impossiveis(self) -> None:
        """Datas e horas que casam com LINHA, mas não existem, são inválidas."""
        for linha in ["2026-13-05 08:00:00 INFO PT102 contagens=1",
                      "2026-02-30 08:00:00 INFO PT102 contagens=1",
                      "2026-10-05 25:00:00 INFO PT102 contagens=1",
                      "2026-10-05 08:00:60 INFO PT102 contagens=1"]:
            with self.subTest(linha=linha):
                self.assertEqual(ler_log(linha), ([], [linha]))

    def test_resto_sem_pares(self) -> None:
        """Uma linha que casa com LINHA, mas sem par chave=valor, é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT102 sem pares aqui"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_invalida_preservada_como_no_texto(self) -> None:
        """A linha inválida é devolvida sem nenhuma limpeza, com os espaços nas pontas."""
        linha = f"  {LINHA_VALIDA}  "
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_varios_espacos_entre_as_partes(self) -> None:
        """As partes podem ser separadas por mais de um espaço."""
        registros, invalidas = ler_log("2026-10-05   08:00:06  WARN   B1    corrente=49.8")
        self.assertEqual(invalidas, [])
        self.assertEqual(registros[0].instante, datetime(2026, 10, 5, 8, 0, 6))
        self.assertAlmostEqual(registros[0].valores["corrente"], 49.8)

    def test_varios_pares_com_tipos_mistos(self) -> None:
        """Cada valor é convertido à parte: número vira float e texto continua str."""
        registros, _ = ler_log("2026-10-05 08:00:00 ALARME PT102 evento=alta limite=2000")
        self.assertEqual(registros[0].valores["evento"], "alta")
        self.assertAlmostEqual(registros[0].valores["limite"], 2000.0)

    def test_ordem_das_linhas(self) -> None:
        """Os registros seguem a ordem do texto, mesmo fora de ordem cronológica."""
        tarde = "2026-10-05 09:00:00 INFO LT301 nivel=50.0"
        registros, _ = ler_log(f"{tarde}\n{LINHA_VALIDA}\n")
        self.assertEqual([r.tag for r in registros], ["LT301", "PT102"])


class TestLeitorDetalhes(unittest.TestCase):
    """Issue #1: valida_tag e serie em casos de borda."""

    def test_tag_com_quebra_de_linha(self) -> None:
        """Com fullmatch, um fim de linha depois da tag também é sobra de caracteres."""
        self.assertFalse(valida_tag("PT101\n"))

    def test_tag_com_digitos_nao_ascii(self) -> None:
        """Dígitos Unicode, que um \\d sem re.ASCII aceitaria, não formam uma tag."""
        self.assertFalse(valida_tag("PT١٠١"))

    def test_serie_de_outra_tag(self) -> None:
        """serie ignora os registros de outras tags, mesmo que tenham a mesma chave."""
        registros, _ = ler_log(f"{LINHA_VALIDA}\n2026-10-05 08:00:00 INFO PT101 contagens=131\n")
        self.assertTrue(np.allclose(serie(registros, "PT101", "contagens"), [131.0]))


class TestConversores(unittest.TestCase):
    """Issue #2: criar_conversores fora do caso coberto pelos testes de aceitação."""

    def test_nao_depende_do_dicionario_de_origem(self) -> None:
        """Alterar o dicionário depois de criar os conversores não muda os fatores."""
        escalas = {"PT101": 2.0, "FT201": 0.1}
        conversores = criar_conversores(escalas)
        escalas["PT101"] = 100.0
        self.assertAlmostEqual(conversores["PT101"](10.0), 20.0)

    def test_aceita_um_unico_argumento(self) -> None:
        """Cada conversor recebe só a contagem: o fator não vira um parâmetro exposto."""
        conversor = criar_conversores({"PT101": 2.0})["PT101"]
        with self.assertRaises(TypeError):
            conversor(10.0, 5.0)


class TestMemoriaEConversao(unittest.TestCase):
    """Issue #3: casos de entrada que os testes de aceitação não verificam."""

    def test_memoria_rejeita_nao_inteiros(self) -> None:
        """medir_memoria exige dtype inteiro e um ndarray de verdade."""
        for entrada in [np.zeros(3), np.array([True, False]), [1, 2, 3]]:
            with self.subTest(entrada=entrada), self.assertRaises(ValueError):
                medir_memoria(entrada)

    def test_vetorizado_nao_estoura_em_uint16(self) -> None:
        """A conversão vetorizada dá 600 kPa no fundo de escala, mesmo com uint16."""
        kpa = converter_vetorizado(np.array([4095], dtype=np.uint16))
        self.assertTrue(np.allclose(kpa, [600.0]))


if __name__ == "__main__":
    unittest.main()

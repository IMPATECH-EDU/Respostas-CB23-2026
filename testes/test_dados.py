"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np
from elevatoria.dados import por_tag
from elevatoria import dados
import datetime
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestRegressionIssue4(unittest.TestCase):
    """Testes de regressão da issue #4 (média móvel)."""
    def test_media_movel_tamanho_correto(self):
        dados = np.arange(600, dtype=float)
        s = SerieTemporal.de_lista(dados)
        mm = s.media_movel(30)
        self.assertEqual(len(mm), 571)  # 600 - 30 + 1 = 571

    def test_media_movel_janela_um(self):
        """Média móvel com janela 1 deve retornar a própria série com mesmo tamanho."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        mm = s.media_movel(1)
        self.assertEqual(len(mm), 4)


class TestReamostrar(unittest.TestCase):
    """Testes para SerieTemporal.reamostrar (Issue #5)."""

    def test_reamostrar_com_sobra_no_fim(self):
        """Reamostrar série de 7 elementos com k=3 deve descartar a sobra e retornar 2 blocos."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 100.0])
        r = s.reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_reamostrar_k_maior_que_tamanho(self):
        """Reamostrar com k maior que o tamanho da série levanta ValueError."""
        s = SerieTemporal.de_lista([1.0, 2.0])
        with self.assertRaises(ValueError):
            s.reamostrar(5)


class TestLerLogContrato(unittest.TestCase):
    """Testes de regras do contrato de ler_log."""

    def test_ler_log_tipos_dos_valores(self):
        """Valores numéricos deven virar float e textos devem continuar str."""
        texto = "2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5\n"
        registros, invalidas = dados.ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertIsInstance(registros[0].valores["corrente"], float)
        self.assertIsInstance(registros[0].valores["evento"], str)

    def test_ler_log_instante_datetime(self):
        """O atributo instante do Registro deve ser um objeto datetime.datetime."""
        texto = "2026-10-05 08:00:00 INFO PT101 contagens=131\n"
        registros, _ = dados.ler_log(texto)
        self.assertIsInstance(registros[0].instante, datetime.datetime)
        self.assertEqual(registros[0].instante, datetime.datetime(2026, 10, 5, 8, 0, 0))

    def test_ler_log_linha_corrompida_vai_para_invalidas(self):
        """Linha sem tag ou truncada deve ir para a lista de invalidas."""
        texto = "2026-10-05 08:00:00 INFO contagens=131\n"
        registros, invalidas = dados.ler_log(texto)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

    def test_ler_log_valores_nao_numericos_viram_string(self):
        """Chaves de valores não numéricos são convertidas para string e não para float."""
        texto = "2026-10-05 08:00:00 INFO B1 evento=partida\n"
        registros, _ = dados.ler_log(texto)
        self.assertIsInstance(registros[0].valores["evento"], str)
        self.assertEqual(registros[0].valores["evento"], "partida")

    def test_ler_log_rejeita_tag_com_minusculas(self):
        """Linha com tag em minúsculas deve ser classificada como inválida."""
        texto = "2026-10-05 08:00:00 INFO pt101 contagens=131\n"
        registros, invalidas = dados.ler_log(texto)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

if __name__ == "__main__":
    unittest.main()

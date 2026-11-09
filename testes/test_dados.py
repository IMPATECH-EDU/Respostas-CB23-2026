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


class TestRegressaoIssue4MediaMovel(unittest.TestCase):
    """Testes de regressão para a issue #4 da média móvel."""

    def test_media_movel_janela_um_preserva_todos_os_elementos(self):
        """Com janela 1, media_movel devolve todos os elementos originais."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        mm = s.media_movel(1)
        self.assertEqual(len(mm), len(s))
        self.assertTrue(np.allclose(mm, s))

    def test_media_movel_tem_tamanho_n_menos_janela_mais_um(self):
        """Com janela k, o tamanho da média móvel é n - k + 1."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        mm = s.media_movel(30)
        self.assertEqual(len(mm), 571)


class TestReamostrar(unittest.TestCase):
    """Testes de contrato para o método reamostrar."""

    def test_reamostrar_calcula_medias_por_bloco(self):
        """Reamostrar calcula a média correta de cada bloco completo."""
        s = SerieTemporal.de_lista([1.0, 3.0, 5.0, 7.0, 9.0, 11.0])
        r = s.reamostrar(2)
        self.assertTrue(np.allclose(r, [2.0, 6.0, 10.0]))

    def test_reamostrar_descarta_sobra_no_final(self):
        """Reamostrar descarta os pontos finais que não completam bloco."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 100.0])
        r = s.reamostrar(2)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [1.5, 3.5]))

    def test_reamostrar_rejeita_k_invalido(self):
        """Reamostrar levanta ValueError quando k está fora do intervalo válido."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            s.reamostrar(0)
        with self.assertRaises(ValueError):
            s.reamostrar(4)


class TestLerLogContratoExtra(unittest.TestCase):
    """Testes de contrato de ler_log além dos casos de aceitação."""

    def test_ler_log_ignora_linhas_vazias_sem_contar_como_invalidas(self):
        """Linhas vazias e com espaços são ignoradas e não entram em invalidas."""
        texto = (
            "\n"
            "   \n"
            "2026-10-05 08:00:00 INFO PT101 contagens=100\n"
            "\t\n"
            "2026-10-05 08:00:06 INFO PT101 contagens=110\n"
        )
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 2)
        self.assertEqual(invalidas, [])

    def test_ler_log_mantem_linha_corrompida_exatamente_como_veio(self):
        """Linha inválida é devolvida em invalidas sem normalização de texto."""
        invalida = "### falha de comunicacao com a RTU ###"
        texto = (
            "2026-10-05 08:00:00 INFO PT101 contagens=100\n"
            f"{invalida}\n"
            "2026-10-05 08:00:06 INFO PT101 contagens=110\n"
        )
        _, invalidas = ler_log(texto)
        self.assertEqual(invalidas, [invalida])

    def test_ler_log_converte_numeros_para_float_e_preserva_strings(self):
        """Valores numéricos viram float e valores textuais permanecem string."""
        texto = "2026-10-05 08:00:00 INFO B1 corrente=47.5 evento=partida\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(invalidas, [])
        self.assertIsInstance(registros[0].valores["corrente"], float)
        self.assertIsInstance(registros[0].valores["evento"], str)
        self.assertAlmostEqual(registros[0].valores["corrente"], 47.5)


class TestSerieFuncao(unittest.TestCase):
    """Testes de integração da função serie com o parser do log."""

    def test_serie_ignora_registros_sem_chave(self):
        """A série ignora registros da tag sem a chave solicitada."""
        texto = (
            "2026-10-05 08:00:00 INFO PT102 contagens=100\n"
            "2026-10-05 08:00:06 ALARME PT102 evento=pressao_alta limite=2000\n"
            "2026-10-05 08:00:12 INFO PT102 contagens=200\n"
        )
        registros, _ = ler_log(texto)
        s = serie(registros, "PT102", "contagens")
        self.assertTrue(np.allclose(s, [100.0, 200.0]))

    def test_serie_retorna_instancia_de_serie_temporal(self):
        """A função serie retorna explicitamente um objeto SerieTemporal."""
        texto = (
            "2026-10-05 08:00:00 INFO FT201 pulsos=10\n"
            "2026-10-05 08:00:06 INFO FT201 pulsos=12\n"
        )
        registros, _ = ler_log(texto)
        s = serie(registros, "FT201", "pulsos")
        self.assertIsInstance(s, SerieTemporal)
        self.assertTrue(np.allclose(s, [10.0, 12.0]))


if __name__ == "__main__":
    unittest.main()

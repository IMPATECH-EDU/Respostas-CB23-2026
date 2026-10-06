"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag
import numpy as np
from elevatoria.serie import SerieTemporal
from elevatoria.dados import ler_log


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])

    def test_tamanho_correto_media_movel(self):
        """Garante que a média móvel de tamanho k retorna exatamente n - k + 1 valores."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        mm = s.media_movel(3)
        # Uma série de 5 elementos com janela 3 deve devolver 3 valores (5 - 3 + 1)
        self.assertEqual(len(mm), 3)

    def test_valores_corretos_media_movel(self):
        """Verifica se os valores da média móvel estão corretos, não omitindo a primeira janela."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        mm = s.media_movel(2)
        esperado = [15.0, 25.0, 35.0]
        # O código atual com defeito devolve apenas [25.0, 35.0] e falhará aqui
        self.assertTrue(np.allclose(mm, esperado))


class TestReamostrarSerie(unittest.TestCase):
    """Testes para o método reamostrar e descarte de sobras (Issue #5)."""

    def test_descarte_de_sobra_no_fim(self):
        """Garante que os pontos excedentes no final da série que não formam um bloco são descartados."""
        s = SerieTemporal.de_lista([1.0, 3.0, 5.0, 7.0, 9.0])
        r = s.reamostrar(2)
        # Com k=2, forma os blocos [1, 3] -> 2.0 e [5, 7] -> 6.0. O valor 9.0 é descartado.
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 6.0]))

    def test_retorno_exato_sem_sobras_e_tipo(self):
        """Verifica o cálculo exato sem sobras e atesta que o retorno é do tipo SerieTemporal."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        r = s.reamostrar(2)
        
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(r, [15.0, 35.0]))


class TestLerLogRegrasAdicionais(unittest.TestCase):
    """Testes adicionais para as regras de ler_log (Issue #1)."""

    def test_descarta_data_impossivel(self):
        """Verifica se linhas com datas ou horas impossíveis (ex: mês 13) são descartadas."""
        log = "2026-13-05 08:00:00 INFO B1 evento=partida\n"
        registros, invalidas = ler_log(log)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

    def test_descarta_sem_pares_chave_valor(self):
        """Garante que a linha seja inválida se o bloco 'resto' não tiver pares chave=valor."""
        log = "2026-10-05 08:00:00 INFO B1 apenas_texto_solto_sem_igual\n"
        registros, invalidas = ler_log(log)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

    def test_ignora_linhas_vazias_ou_espacos(self):
        """Confirma que linhas vazias ou apenas com espaços não contam como inválidas."""
        log = "   \n\n2026-10-05 08:00:00 INFO B1 evento=partida"
        registros, invalidas = ler_log(log)
        self.assertEqual(len(registros), 1)
        self.assertEqual(len(invalidas), 0)

    def test_conversao_mista_tipos(self):
        """Verifica se a conversão separa corretamente floats e strings no mesmo registro."""
        log = "2026-10-05 08:00:00 INFO PT101 contagens=131 evento=falha"
        registros, _ = ler_log(log)
        valores = registros[0].valores
        self.assertIsInstance(valores["contagens"], float)
        self.assertIsInstance(valores["evento"], str)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np
from datetime import datetime

from elevatoria.dados import valida_tag, ler_log, criar_conversores
from elevatoria.serie import SerieTemporal

class TestDadosESerie(unittest.TestCase):

    # --- Testes da Issue #4 (media_movel)
    
    def test_tamanho_media_movel(self):
        """Verifica se a média móvel retorna o tamanho matemático correto (N - k + 1)."""
        s = np.array([1.0, 2.0, 3.0, 4.0, 5.0]).view(SerieTemporal)
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 3)

    def test_media_movel_janela_invalida(self):
        """Garante que janelas menores que 1 ou maiores que a série levantem ValueError."""
        s = np.array([10.0, 20.0, 30.0]).view(SerieTemporal)
        with self.assertRaises(ValueError):
            s.media_movel(0)
        with self.assertRaises(ValueError):
            s.media_movel(4)

    # --- Testes da Issue #5 (reamostrar) ---

    def test_reamostrar_exato(self):
        """Verifica a reamostragem quando o tamanho da série é múltiplo exato de k."""
        s = np.array([10.0, 20.0, 30.0, 40.0]).view(SerieTemporal)
        reamostrado = s.reamostrar(2)
        np.testing.assert_allclose(reamostrado, [15.0, 35.0])

    def test_reamostrar_com_sobra(self):
        """Garante que a reamostragem descarte corretamente os pontos que sobram no fim."""
        s = np.array([10.0, 20.0, 30.0, 40.0, 50.0]).view(SerieTemporal)
        reamostrado = s.reamostrar(2)
        np.testing.assert_allclose(reamostrado, [15.0, 35.0])

    # --- Testes da Issue #1 (ler_log e valida_tag) ---

    def test_ler_log_linha_corrompida(self):
        """Garante que linhas fora do formato sejam contabilizadas como inválidas."""
        texto = "2026-10-05 08:00:00 INFO PT101 contagens=131\nLINHA CORROMPIDA ALEATORIA\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(len(invalidas), 1)

    def test_ler_log_sem_dados(self):
        """Verifica o comportamento do leitor ao receber uma string vazia."""
        registros, invalidas = ler_log("")
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 0)

    def test_valida_tag_espaco_em_branco(self):
        """Testa se valida_tag barra falsos positivos com espaços no final (re.match vs fullmatch)."""
        self.assertFalse(valida_tag("PT101 "))

    # --- Teste da Issue #2 (criar_conversores) ---

    def test_criar_conversores_late_binding(self):
        """Garante que as lambdas geradas não sofram de late binding e usem fatores isolados."""
        escalas = {"T1": 2.0, "T2": 5.0}
        conversores = criar_conversores(escalas)
        self.assertEqual(conversores["T1"](10), 20.0)
        self.assertEqual(conversores["T2"](10), 50.0)


if __name__ == '__main__':
    unittest.main()
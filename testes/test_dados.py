"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import numpy as np
import unittest

from elevatoria.dados import por_tag
from elevatoria.dados import ler_log
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])



# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestRegressaoMediaMovel(unittest.TestCase):
    """Testes de regressão da issue #4 (média móvel)."""

    def test_media_movel_janela_2(self):
        """Média móvel com janela 2 deve respeitar n - janela + 1."""
        dados = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0, 50.0])
        janela = 2
        resultado = dados.media_movel(janela)
        self.assertEqual(len(resultado), len(dados) - janela + 1)
    def test_media_movel_janela_1(self):
        """Média móvel com janela 1 deve devolver uma cópia dos dados."""
        dados = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0, 50.0])
        janela = 1
        resultado = dados.media_movel(janela)

        # Verifica se os vetores são do mesmo tamanho
        self.assertEqual(len(resultado), len(dados))
        
        # Verifica se o resultado é igual à série original
        self.assertTrue(np.allclose(resultado, dados))

    def test_media_movel_retorna_571_valores(self):
        """Média móvel de 30 pontos deve devolver n - janela + 1 valores."""
        dados = SerieTemporal.de_lista([float(i) for i in range(600)])
        resultado = dados.media_movel(30)
        self.assertEqual(len(resultado), 571)


class TestReamostrar(unittest.TestCase):
    """Testes próprios da reamostragem."""

    def test_bloco_com_sobra(self):
        """Pontos finais que não completam um bloco são descartados."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7])
        resultado = s.reamostrar(3)
        self.assertTrue(np.allclose(resultado, [2.0, 5.0]))

    def test_sobra_um_ponto(self):
        """A sobra no fim não entra na última média."""
        s = SerieTemporal.de_lista([10, 20, 30, 40])
        resultado = s.reamostrar(3)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 20.0)


class TestLerLogRegra(unittest.TestCase):
    """Testes próprios das regras adicionais de ler_log."""

    def test_data_impossivel_e_ignora_linha_vazia(self):
        """Data impossível é inválida e linhas vazias são ignoradas."""
        texto = "\n2026-13-05 08:00:00 INFO PT101 contagens=100\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(registros, [])
        self.assertEqual(len(invalidas), 1)

    def test_resto_sem_par_chave_valor(self):
        """Uma linha válida no formato é inválida sem pares chave=valor."""
        texto = "2026-10-05 08:00:00 INFO PT101 sem_dados"
        registros, invalidas = ler_log(texto)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [texto])

    def test_valor_com_sinal_menos(self):
        """Valores negativos continuam float."""
        texto = "2026-10-05 08:00:00 INFO LT301 nivel=-1.25"
        registros, _ = ler_log(texto)
        self.assertIsInstance(registros[0].valores["nivel"], float)
        self.assertAlmostEqual(registros[0].valores["nivel"], -1.25)
if __name__ == "__main__":
    unittest.main()

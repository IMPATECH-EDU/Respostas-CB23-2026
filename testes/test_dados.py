"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import ler_log, por_tag
from elevatoria.serie import SerieTemporal
import numpy as np

class TestLerLogAdicionais(unittest.TestCase):
    """Regras para o contrato de ler_log que os testes de aceitação não verificam."""

    def test_data_impossivel(self):
        """Uma linha com mês impossível casa com LINHA, mas vai para as inválidas."""
        valida = "2026-10-05 08:00:00 INFO PT101 contagens=131"
        impossivel = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(valida + "\n" + impossivel)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [impossivel])
    def test_ignorar_linha_so_com_espacos(self):
        """Linha só com espaços não vira registro nem entra nas inválidas."""
        valida = "2026-10-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(valida + "\n   \n")
        self.assertEqual(len(registros), 1)
        self.assertEqual(len(invalidas), 0)
    def test_invalidar_linha_sem_par_chave_valor(self):
        """Linha que casa com LINHA vai para as inválidas se não tem chave=valor."""
        sem_par = "2026-10-05 08:00:00 INFO PT101 contag"
        registros, invalidas = ler_log(sem_par)
        self.assertEqual(registros, []) # usando [] em vez de 0 para mostrar o conteúdo se tiver alguma falha.
        self.assertEqual(invalidas, [sem_par])

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])

class TestMedia(unittest.TestCase):
    """Testes de regressão da issue #4 (media_movel)."""

    def test_serie_de_seis(self):
        """Média móvel de [2,4,...,12] com janela 2 deve ter 5 valores: [3,5,7,9,11]."""
        s = SerieTemporal.de_lista([2, 4, 6, 8, 10, 12])
        self.assertTrue(np.allclose(s.media_movel(2), [3, 5, 7, 9, 11])) 

    def test_tamanho_600_janela_30(self):
        """Série de 600 pontos com janela 30 deve render 571 valores."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_reamostrar(self):
        """Blocos de 2 em [1..6] resultam nas médias [1.5, 3.5, 5.5]."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        self.assertTrue(np.allclose(s.reamostrar(2), [1.5, 3.5, 5.5]))

    def test_reamostrar_e_descarta(self):
        """Em [1..7] com k=3 o ponto 7 sobra e é descartado. O resultado é [2, 5]."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7])
        r = s.reamostrar(3)
        self.assertEqual(len(r), 2)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))
    def test_janela_igual_ao_tamanho(self):
        """Com janela igual a len(série) o resultado tem 1 valor, que é a média de tudo."""
        s = SerieTemporal.de_lista([2, 4, 6, 8])
        mm = s.media_movel(4)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 5.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

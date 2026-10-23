"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import ler_log, por_tag
from elevatoria.serie import SerieTemporal

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestMediaMovelRegressao(unittest.TestCase):
    def test_tamanho(self):
        # Estamos fazendo o numero de pontos menos o numero da janela mais um para criar a media movel
        s = SerieTemporal.de_lista(range(10))
        self.assertEqual(len(s.media_movel(3)),8)

    def test_primeiro_valor(self):
        # Pegamos o primeiro valor para ser a media de s ate o tamanho da janela [0:janela]
        s = SerieTemporal.de_lista([1,2,3,4,5])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 1.5)

    def test_janela_max(self):
        # Fazemos a janela = len(s)
        s = SerieTemporal.de_lista([2,4,6])
        mm = s.media_movel(3)
        self.assertEqual(len(mm),1)
        self.assertAlmostEqual(float(mm[0]), 4.0)

class TestReamostrar(unittest.TestCase):
    def test_blocos_exatos(self):
        r = SerieTemporal.de_lista([1,2,3,4,5,6]).reamostrar(3)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_sobra_descartada(self):
        r = SerieTemporal.de_lista([1,2,3,4,5,6,100]).reamostrar(3)
        self.assertTrue(np.allclose(r,[2.0, 5.0]))

    def test_tipo_e_original_intacto(self):
        s = SerieTemporal.de_lista([1,2,3,4])
        r = s.reamostrar(2)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(s, [1,2,3,4]))

class TestLerLogRegras(unittest.TestCase):
    def test_linhas_em_branco(self):
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=131\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_impossivel(self):
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_sem_par_chave_valor(self):
        linha = "2026-10-05 08:00:00 INFO PT101 sem pares aqui"
        registro, invalidas = ler_log(linha)
        self.assertEqual(registro, [])
        self.assertEqual(invalidas, [linha])

if __name__ == "__main__":
    unittest.main()

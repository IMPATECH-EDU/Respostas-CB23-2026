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
    """Testes de regressão da issue #4: a média móvel perdia a primeira janela."""

    def test_tamanho(self):
        """Com 10 pontos e janela 3, a média móvel tem 10 - 3 + 1 = 8 valores."""
        s = SerieTemporal.de_lista(range(10))
        self.assertEqual(len(s.media_movel(3)), 8)

    def test_primeiro_valor(self):
        """O primeiro valor é a média de s[0:janela]: a primeira janela não pode sumir."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 1.5)

    def test_janela_max(self):
        """Com a janela igual ao tamanho da série, sai um único valor: a média da série."""
        s = SerieTemporal.de_lista([2, 4, 6])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 4.0)

class TestReamostrar(unittest.TestCase):
    """Testes de reamostrar (issue #5), incluindo a sobra no fim da série."""

    def test_blocos_exatos(self):
        """Com 6 pontos e k = 3, saem as médias dos 2 blocos."""
        r = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6]).reamostrar(3)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_sobra_descartada(self):
        """Com 7 pontos e k = 3, o ponto que sobra no fim é descartado."""
        r = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 100]).reamostrar(3)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_tipo_e_original_intacto(self):
        """Devolve uma SerieTemporal e não modifica a série original."""
        s = SerieTemporal.de_lista([1, 2, 3, 4])
        r = s.reamostrar(2)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(s, [1, 2, 3, 4]))

class TestLerLogRegras(unittest.TestCase):
    """Regras do contrato de ler_log que os testes de aceitação não verificam."""

    def test_linhas_em_branco(self):
        """Linhas vazias ou só com espaços são ignoradas e não contam como inválidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=131\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_impossivel(self):
        """Uma linha com mês 13 vai para as inválidas, exatamente como estava."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_sem_par_chave_valor(self):
        """Uma linha cujo resto não tem nenhum par chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 INFO PT101 sem pares aqui"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

if __name__ == "__main__":
    unittest.main()
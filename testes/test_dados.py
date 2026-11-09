"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
from datetime import datetime

import numpy as np
from elevatoria.dados import por_tag, ler_log
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoMediaMovel(unittest.TestCase):
    """Testes de regressão da issue #4 ANTES da correção."""

    def test_media_movel_tamanho_correto(self):
        """Verifica se media_movel(30) de 600 pontos devolve exatos 571 valores."""
        s = SerieTemporal.de_lista([1.0] * 600)
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_media_movel_valor_correto(self):
        """Verifica se o valor da média móvel é matematicamente correto no offset da janela."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        mm = s.media_movel(3) # n(5) - janela(3) + 1 = 3 pontos
        np.testing.assert_allclose(mm, [2.0, 3.0, 4.0])


class TestReamostrar(unittest.TestCase):
    """Testes para o cálculo das médias por bloco na issue #5."""
    
    def test_reamostrar_exato(self):
        """Testa se a reamostragem funciona num múltiplo exato do tamanho."""
        s = SerieTemporal.de_lista([2, 4, 10, 20])
        reamostrado = s.reamostrar(2)
        np.testing.assert_allclose(reamostrado, [3.0, 15.0])
        self.assertIsInstance(reamostrado, SerieTemporal)

    def test_reamostrar_com_sobra(self):
        """Verifica se reamostrar descarta corretamente a sobra no fim do array."""
        s = SerieTemporal.de_lista([1, 3, 5, 7, 9])
        reamostrado = s.reamostrar(2)
        np.testing.assert_allclose(reamostrado, [2.0, 6.0]) # o valor '9' é descartado


class TestLerLogAdicionais(unittest.TestCase):
    """Testes de regras do contrato de ler_log que os testes de aceitação não cobrem."""

    def test_ler_log_data_impossivel(self):
        """Verifica se data impossível (mês 13) torna a linha inválida."""
        texto = "2026-13-05 08:00:00 INFO B1 evento=partida\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

    def test_ler_log_sem_pares(self):
        """Verifica se a linha sem chave=valor no resto conta como inválida."""
        texto = "2026-10-05 08:00:00 INFO B1 errodesconhecido\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

    def test_ler_log_vazio(self):
        """Passar um texto vazio deve devolver duas listas vazias e não quebrar o código."""
        registros, invalidas = ler_log("")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [])
        
    def test_ler_log_float_e_str(self):
        """Garante que a conversão para float e fallback para str acontecem adequadamente."""
        texto = "2026-10-05 08:00:00 INFO PT101 a=10.5 b=erro\n"
        registros, _ = ler_log(texto)
        self.assertEqual(registros[0].valores["a"], 10.5)
        self.assertIsInstance(registros[0].valores["a"], float)
        self.assertEqual(registros[0].valores["b"], "erro")


if __name__ == "__main__":
    unittest.main()

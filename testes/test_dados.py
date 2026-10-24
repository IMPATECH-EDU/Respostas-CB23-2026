"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np

from elevatoria.dados import (por_tag, contagem_por_tag, criar_conversores, ler_log, medir_memoria,
                              medir_tempos, serie, valida_tag)
from elevatoria.serie import SerieTemporal

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])

# Abaixo mais um teste de elevatoria.dados
class TestContagemPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `contagem_por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, contagem_por_tag devolve um dicionário vazio."""
        self.assertEqual(contagem_por_tag([]), {})

# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestSerieTemporal(unittest.TestCase):
    """Testes de regressão da issue #4."""

    def test_media_movel(self):
        """Médias móveis de janela 3."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        esperado = SerieTemporal.de_lista([2.0, 3.0, 4.0])
        resultado = s.media_movel(3)
        self.assertTrue(np.allclose(resultado, esperado), f"esperado {esperado}, obtido {resultado}")

    def test_media_movel_falho(self):
        """Médias móveis de janela 0 (deve falhar)."""
        s = SerieTemporal.de_lista([1, 2, 3])
        with self.assertRaises(ValueError):
            s.media_movel(0)

    def test_variacao(self):
        """Diferenças entre pontos consecutivos."""
        s = SerieTemporal.de_lista([1, 3, 2, 5])
        esperado = SerieTemporal.de_lista([2.0, -1.0, 3.0])
        resultado = s.variacao()
        self.assertTrue(np.allclose(resultado, esperado), f"esperado {esperado}, obtido {resultado}")

    def test_reamostrar_1(self):
        """Reamostragem com k=2."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        esperado = SerieTemporal.de_lista([1.5, 3.5, 5.5])
        resultado = s.reamostrar(2)
        self.assertTrue(np.allclose(resultado, esperado), f"esperado {esperado}, obtido {resultado}")

    def test_reamostrar_2(self):
        """Reamostragem com k=3, descartando pontos finais."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7])
        esperado = SerieTemporal.de_lista([2.0, 5.0])
        resultado = s.reamostrar(3)
        self.assertTrue(np.allclose(resultado, esperado), f"esperado {esperado}, obtido {resultado}")

class TestLerLog(unittest.TestCase):
    """Testes de regressão da issue #1."""

    def test_rejeita_data_e_hora_impossiveis(self):
        """Linhas com data ou hora impossíveis são inválidas e preservadas."""
        texto = (
            "2026-13-05 08:00:00 INFO PT101 contagens=12\n"
            "2026-10-05 25:00:00 INFO PT101 contagens=13\n"
            "2026-10-05 08:00:00 INFO PT101 contagens=14\n"
        )

        registros, invalidas = ler_log(texto)

        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0].valores, {"contagens": 14.0})
        self.assertEqual(invalidas, [
            "2026-13-05 08:00:00 INFO PT101 contagens=12",
            "2026-10-05 25:00:00 INFO PT101 contagens=13",
        ])

    def test_rejeita_linhas_sem_pares(self):
        """Linhas sem pares chave=valor são inválidas e preservadas."""
        texto = (
            "2026-10-05 08:00:00 INFO PT101 contagens=12\n"
            "2026-10-05 08:00:01 INFO PT101\n"
            "2026-10-05 08:00:02 INFO PT101 evento=partida\n"
        )

        registros, invalidas = ler_log(texto)

        self.assertEqual(len(registros), 2)
        self.assertEqual(registros[0].valores, {"contagens": 12.0})
        self.assertEqual(registros[1].valores, {"evento": "partida"})
        self.assertEqual(invalidas, ["2026-10-05 08:00:01 INFO PT101"])
    
class TestValidaTag(unittest.TestCase):
    """Testes de regressão da issue #2."""

    def test_valida_tag(self):
        """Valida tags corretas e rejeita incorretas."""
        self.assertTrue(valida_tag("PT101"))
        self.assertTrue(valida_tag("101PT"))
        self.assertFalse(valida_tag("PT1010"))  # mais de 3 dígitos
        self.assertFalse(valida_tag("101PT "))  # sobra de caracteres
    
    def test_valida_tag_vazia(self):
        """Valida tag vazia."""
        self.assertFalse(valida_tag(""))  # tag vazia

if __name__ == "__main__":
    unittest.main()

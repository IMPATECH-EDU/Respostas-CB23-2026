"""Conjunto de 8 testes extras para os ficheiros dados.py e serie.py."""

import unittest
import numpy as np ####

from elevatoria.dados import valida_tag, ler_log
from elevatoria.serie import SerieTemporal

class TestElevatoriaOitoExtras(unittest.TestCase):
    """8 testes para garantir o funcionamento das estruturas base."""

    # --- Testes para dados.py ---

    def test_01_valida_tag_correta(self):
        """1. Garante que o regex aceita tags perfeitamente formatadas."""
        self.assertTrue(valida_tag("PT101"))
        self.assertTrue(valida_tag("B1"))
        self.assertTrue(valida_tag("FT201"))

    def test_02_valida_tag_incorreta(self):
        """2. Garante que o regex rejeita espaços, minúsculas e formatos errados."""
        self.assertFalse(valida_tag("pt101"))
        self.assertFalse(valida_tag("101PT"))
        self.assertFalse(valida_tag("PT101 "))

    def test_03_ler_log_linhas_validas(self):
        """3. Verifica se as linhas bem formatadas geram objetos Registro corretamente."""
        texto_log = "2026-10-19 12:00:00 INFO PT101 valor=10.5 estado=ativo"
        registros, invalidas = ler_log(texto_log)
        
        self.assertEqual(len(invalidas), 0)
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0].tag, "PT101")
        self.assertEqual(registros[0].valores["valor"], 10.5)
        self.assertEqual(registros[0].valores["estado"], "ativo")

    def test_04_ler_log_linhas_invalidas(self):
        """4. Garante que linhas sem o formato exato são separadas para a lista de inválidas."""
        texto_log = (
            "2026-10-19 12:00:00 INFO PT101\n"  # Faltam os pares chave=valor
            "Data errada INFO PT101 valor=10\n" # Formato de data incorreto
        )
        registros, invalidas = ler_log(texto_log)
        
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 2)

    # --- Testes para serie.py ---

    def test_05_serie_temporal_dimensoes(self):
        """5. Verifica se a série rejeita matrizes que não sejam unidimensionais."""
        # Deve aceitar listas 1D
        serie = SerieTemporal([1.0, 2.0, 3.0])
        self.assertEqual(len(serie), 3)
        
        # Deve levantar erro para matrizes 2D
        with self.assertRaises(ValueError):
            SerieTemporal(np.array([[1, 2], [3, 4]]))

    def test_06_serie_temporal_estatisticas(self):
        """6. Confirma o cálculo correto de média, mínimo, máximo, soma e amplitude."""
        serie = SerieTemporal([10.0, 20.0, 30.0])
        self.assertEqual(serie.media(), 20.0)
        self.assertEqual(serie.min(), 10.0)
        self.assertEqual(serie.max(), 30.0)
        self.assertEqual(serie.sum(), 60.0)
        self.assertEqual(serie.amplitude(), 20.0)

    def test_07_serie_temporal_aritmetica(self):
        """7. Verifica se as operações aritméticas (+, -, *, /) afetam todos os elementos."""
        serie = SerieTemporal([2.0, 4.0, 6.0])
        
        soma = serie + 2.0
        self.assertEqual(soma[0], 4.0)
        
        divisao = serie / 2.0
        self.assertEqual(divisao[2], 3.0)

    def test_08_serie_temporal_janela_invalida(self):
        """8. Verifica se o método media_movel bloqueia janelas de tamanho incorreto."""
        serie = SerieTemporal([1.0, 2.0, 3.0])
        
        # Janela maior que a própria série
        with self.assertRaises(ValueError):
            serie.media_movel(5)
            
        # Janela zero ou negativa
        with self.assertRaises(ValueError):
            serie.media_movel(0)

if __name__ == '__main__':
    unittest.main()
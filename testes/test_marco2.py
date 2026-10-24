"""Testes de regressão e validação para o Marco 2."""

import unittest
from datetime import datetime
import numpy as np

from elevatoria.acumuladores import AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

class TestMarco2(unittest.TestCase):
    """Conjunto de 4 testes requeridos no Marco 2 (Issues #6 e #7)."""

    def test_01_kahan_regressao(self):
        """1. Garante que AcumuladorKahan compensa o erro de ponto flutuante (Issue #7)."""
        acumulador = AcumuladorKahan()
        # Somar 0.1 um milhão de vezes
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)
        
        # O acumulador Kahan corrigido não sofre de erro flutuante progressivo
        self.assertEqual(acumulador.total, 100_000.0)

    def test_02_medir_remocao_espurias(self):
        """2. Verifica se a função medir remove corretamente os valores espúrios pelo z-score (Issue #6)."""
        curva = CurvaCalibracao([0, 10, 20], [0, 10, 20], "linear")
        
        # O valor 1000 (índice 3) é um "outlier" (espúrio) isolado
        contagens = [10.0, 10.0, 10.0, 1000.0, 10.0, 10.0]
        registros = [
            Registro(datetime.now(), "INFO", "PT101", {"contagens": c})
            for c in contagens
        ]
        
        resultado = medir(registros, "PT101", curva, u_sistematica=0.0)
        
        self.assertEqual(resultado.espurias, [3])
        self.assertEqual(resultado.n_validas, 5)
        self.assertEqual(resultado.medida.valor, 10.0)

    def test_03_medir_mad_zero(self):
        """3. Verifica o lançamento de ValueError quando a MAD é exatamente zero (Issue #6)."""
        curva = CurvaCalibracao([0, 10, 20], [0, 10, 20], "linear")
        
        # Todos os valores são rigorosamente iguais, logo o desvio e a MAD são zero
        contagens = [15.0, 15.0, 15.0, 15.0]
        registros = [
            Registro(datetime.now(), "INFO", "PT101", {"contagens": c})
            for c in contagens
        ]
        
        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva, u_sistematica=0.0)

    def test_04_medir_calculo_incerteza(self):
        """4. Verifica se a incerteza combinada (u_sistematica + erro padrão) está correta (Issue #6)."""
        curva = CurvaCalibracao([0, 10, 20], [0, 10, 20], "linear")
        
        contagens = [8.0, 10.0, 12.0, 10.0] 
        registros = [
            Registro(datetime.now(), "INFO", "PT101", {"contagens": c})
            for c in contagens
        ]
        
        resultado = medir(registros, "PT101", curva, u_sistematica=3.0)
        
        # A incerteza combinada tem de ser obrigatoriamente superior à incerteza sistemática pura
        self.assertTrue(resultado.medida.incerteza > 3.0)
        self.assertAlmostEqual(resultado.medida.valor, 10.0)
        
if __name__ == '__main__':
    unittest.main()

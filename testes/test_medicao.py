"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo

import unittest
from datetime import datetime
import numpy as np

from elevatoria.acumuladores import AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

    def test_01_kahan_regressao(self):
        """1. Garante que AcumuladorKahan compensa o erro de ponto flutuante (Issue #7)."""
        acumulador = AcumuladorKahan()
        # Somar 0.1 um milhão de vezes
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)
        
        # O acumulador Kahan corrigido não sofre de erro flutuante progressivo
        self.assertAlmostEqual(acumulador.total, 100_000.0, places=9)

    def test_02_medir_remocao_espurias(self):
        """2. Verifica se a função medir remove corretamente os valores espúrios pelo z-score (Issue #6)."""
        # Domínio amplo o bastante para conter a leitura espúria (a curva não extrapola)
        curva = CurvaCalibracao([0, 1000, 2000], [0, 1000, 2000], "linear")

        # O valor 1000 (índice 3) é espúrio; as demais variam um pouco, para a MAD não ser zero
        contagens = [9.0, 11.0, 10.0, 1000.0, 10.0, 9.0, 11.0, 10.0]
        registros = [
            Registro(datetime.now(), "INFO", "PT101", {"contagens": c})
            for c in contagens
        ]

        resultado = medir(registros, "PT101", curva, u_sistematica=0.0)

        self.assertEqual(resultado.espurias, [3])
        self.assertEqual(resultado.n_validas, 7)
        self.assertAlmostEqual(resultado.medida.valor, 10.0)

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
        


if __name__ == "__main__":
    unittest.main()
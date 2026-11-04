"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada
from fornecido.simulador import verdade_dia


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Issue #11: regressão do trapézio em malha irregular

class TestTrapezioMalhaIrregularRegressao(unittest.TestCase):
    """Testes de regressão da issue #11 (escritos antes da correção)."""

    def test_reta_em_tres_pontos_desiguais(self):
        """∫ de y = x em [0, 3] com pontos 0, 1 e 3 vale 4,5 (e não 2,5 com passo único)."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [0.0, 1.0, 3.0]), 4.5)

    def test_funcao_linear_e_exata_em_qualquer_malha(self):
        """O trapézio é exato para 3x + 1 em [0, 2], seja qual for a malha: o resultado é 8."""
        x = np.array([0.0, 0.3, 1.1, 1.2, 2.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 8.0)

    def test_soma_das_areas_de_cada_trapezio(self):
        """Com x = 0, 0,25, 1 e 2 e y = 2, 4, 4 e 8, a área é 0,75 + 3 + 6 = 9,75."""
        resultado = Trapezio().integrar_tabela([0.0, 0.25, 1.0, 2.0], [2.0, 4.0, 4.0, 8.0])
        self.assertAlmostEqual(resultado, 0.25 * 3.0 + 0.75 * 4.0 + 1.0 * 6.0)

    def test_volume_do_dia_com_leituras_perdidas(self):
        """Com as 8 leituras perdidas do registro, o volume do dia fica a menos de 1,5% da conferência."""
        t, q = vazao_registrada(3478)
        volume = 3.6 * Trapezio().integrar_tabela(t, q)
        self.assertLess(abs(volume / verdade_dia()["volume_m3"] - 1), 0.015)


if __name__ == "__main__":
    unittest.main()

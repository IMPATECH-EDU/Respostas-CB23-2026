"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada
from fornecido.simulador import verdade_dia


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioRegressao(unittest.TestCase):
    """Issue #11: integrar_tabela supunha passo constante. Escritos antes da correção."""

    def test_reta_em_malha_irregular(self):
        """Com passos 1 e 2, o trapézio ainda é exato para a reta 2x + 1: dá 12 em [0, 3]."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [1.0, 3.0, 7.0]), 12.0)

    def test_leitura_perdida_no_meio(self):
        """50 L/s constantes por 1 h, sem a leitura de 0,5 h, integram 50 e não 37,5."""
        t = np.array([0.0, 0.25, 0.75, 1.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.full(4, 50.0)), 50.0)

    def test_volume_do_registro_3487(self):
        """Registro 3487, com 8 leituras perdidas: volume a menos de 1% da conferência."""
        t, q = vazao_registrada(3487)
        volume = 3.6 * Trapezio().integrar_tabela(t, q)
        self.assertLess(abs(volume / verdade_dia()["volume_m3"] - 1), 0.01)


class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: entradas que ajustar_polinomio recusa e um caso mal condicionado."""

    def test_grau_negativo(self):
        """grau = -1 levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "negativo"):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_tamanhos_diferentes(self):
        """x com 4 pontos e y com 3 levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "mesmo tamanho"):
            ajustar_polinomio([0.0, 1.0, 2.0, 3.0], [1.0, 2.0, 3.0], 1)

    def test_x_repetido_nao_determina_a_parabola(self):
        """Quatro pontos, mas só dois x distintos: a parábola não é única e sai ValueError."""
        with self.assertRaisesRegex(ValueError, "distintos"):
            ajustar_polinomio([1.0, 1.0, 2.0, 2.0], [0.0, 1.0, 2.0, 3.0], 2)

    def test_x_longe_da_origem(self):
        """Parábola exata com x entre 1000 e 1010 volta com resíduo abaixo de 1e-7."""
        x = np.linspace(1000.0, 1010.0, 11)
        y = 3.0 - 0.5 * (x - 1005.0) ** 2
        ajuste = np.polynomial.polynomial.polyval(x, ajustar_polinomio(x, y, 2))
        self.assertTrue(np.allclose(ajuste, y, rtol=0, atol=1e-7))


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: o registro precisa ter leitura nos limites das faixas."""

    def test_falta_o_limite_das_21h(self):
        """Um registro sem a leitura das 21 h levanta ValueError."""
        t = np.array([0.0, 6.0, 12.0, 18.0, 20.0, 22.0, 24.0])
        with self.assertRaisesRegex(ValueError, "21"):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()

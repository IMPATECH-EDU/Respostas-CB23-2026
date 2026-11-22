"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestTrapezio(unittest.TestCase):
    """Testes de regressão da issue #11."""

    def test_regressao_trapezio(self):
        """A regra composta usa os dois subintervalos iguais para integrar x²."""
        self.assertAlmostEqual(Trapezio().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 10.125)

    def test_regressao_trapezio_tabela(self):
        """A integração tabulada usa a largura própria de cada intervalo não uniforme."""
        x = [0.0, 1.0, 3.0]
        y = [xi ** 2 for xi in x]
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 10.5)


class TestDiaDeOperacao(unittest.TestCase):
    def test_custo_por_faixa_em_malha_irregular(self):
        """Cada custo considera apenas os pontos dentro da respectiva faixa tarifária."""
        t = np.array([0.0, 4.0, 9.0, 15.0, 18.0, 19.5, 21.0, 24.0])
        vazao = np.full(t.size, 50.0)
        potencia = 998.0 * 9.81 * 0.050 * 40.0 / (1000.0 * 0.8)

        resumo = dia_de_operacao(t, vazao, np.array([40.0]), np.array([0.8]), Trapezio())

        np.testing.assert_allclose(
            resumo.custo_por_faixa,
            [potencia * 18.0 * 0.50, potencia * 3.0 * 1.50, potencia * 3.0 * 0.50],
        )

class TestAjustarPolinomio(unittest.TestCase):
    def test_ajustar_polinomio_com_ruido(self):
        """Recupera aproximadamente os coeficientes crescentes do polinômio com dados ruidosos."""
        x = np.arange(5.0)
        ruido = np.array([0.05, -0.05, 0.1, -0.1, 0.0])
        y = 1.0 + 2.0 * x + 0.5 * x**2 + ruido

        coeficientes = ajustar_polinomio(x, y, 2)

        np.testing.assert_allclose(coeficientes, [1.0, 2.0, 0.5], atol=0.1)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import numpy as np

from elevatoria.integracao import Simpson, Trapezio
from elevatoria.dia import ajustar_polinomio, dia_de_operacao


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestIssue11Regressao(unittest.TestCase):
    def test_trapezio_tabela_malha_irregular(self):
        """Verifica se o trapézio calcula a área correta em malhas com espaçamento não uniforme."""
        x = np.array([0.0, 1.0, 3.0])
        y = np.array([0.0, 2.0, 6.0])
        resultado = Trapezio().integrar_tabela(x, y)
        self.assertAlmostEqual(resultado, 9.0)

    def test_trapezio_tabela_intervalos_faltantes(self):
        """Garante a integral correta por trapézio quando há leituras ausentes no meio da série."""
        x = np.array([0.0, 0.25, 0.75, 1.0])
        y = np.array([10.0, 10.0, 10.0, 10.0])
        resultado = Trapezio().integrar_tabela(x, y)
        self.assertAlmostEqual(resultado, 10.0)


class TestDiaContrato(unittest.TestCase):
    def test_ajustar_polinomio_validacao_grau(self):
        """Levanta ValueError se o número de pontos for menor que grau + 1."""
        x = np.array([0.0, 1.0])
        y = np.array([1.0, 2.0])
        with self.assertRaises(ValueError):
            ajustar_polinomio(x, y, grau=2)

    def test_dia_de_operacao_valida_limite_faixas(self):
        """Levanta ValueError se algum limite de faixa tarifária não estiver presente em t."""
        t = np.array([0.0, 12.0, 24.0])
        vazao = np.array([50.0, 50.0, 50.0])
        coef_h = np.array([40.0, -0.001])
        coef_r = np.array([0.8, -0.0001])
        with self.assertRaises(ValueError):
            dia_de_operacao(t, vazao, coef_h, coef_r, Trapezio())


if __name__ == "__main__":
    unittest.main()
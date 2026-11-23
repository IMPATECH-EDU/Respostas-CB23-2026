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


class TestTrapezioRegressao(unittest.TestCase):
    """Testes de regressão para o defeito da issue #11 em `Trapezio.integrar_tabela`."""

    def test_trapezio_constante_malha_nao_uniforme(self):
        """Integra função constante em malha não uniforme com resultado exato."""
        x = np.array([0.0, 0.25, 1.0, 3.0])
        y = np.full(x.size, 2.0)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 6.0)

    def test_trapezio_reta_malha_nao_uniforme(self):
        """Integra função linear f(x) = x em malha não uniforme com resultado exato."""
        x = np.array([0.0, 0.5, 2.0, 4.0])
        y = x.copy()
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 8.0)


class TestDiaContrato(unittest.TestCase):
    """Casos do contrato de `ajustar_polinomio` e `dia_de_operacao` fora da aceitação."""

    def test_ajustar_polinomio_grau_negativo(self):
        """Levanta ValueError quando o grau do polinômio é negativo."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_ajustar_polinomio_tamanhos_diferentes(self):
        """Levanta ValueError quando x e y têm tamanhos diferentes."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_dia_limite_de_faixa_ausente(self):
        """Levanta ValueError quando um limite de faixa tarifária (ex.: 18 h) falta em t."""
        t = np.array([0.0, 6.0, 12.0, 21.0, 24.0])
        vazao = np.full(t.size, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, vazao, [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()
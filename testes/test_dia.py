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


class TestRegressaoIssue11(unittest.TestCase):
    """Testes de regressão para a issue #11 (Trapezio.integrar_tabela em malha irregular)."""

    def test_trapezio_tabela_malha_nao_uniforme(self):
        """Trapezio.integrar_tabela calcula área correta em malha com passos desiguais."""
        x = np.array([0.0, 1.0, 3.0])
        y = np.array([2.0, 2.0, 2.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 6.0)

    def test_trapezio_tabela_reta_com_falha_de_leitura(self):
        """Trapezio.integrar_tabela integra função linear exatamente mesmo com salto no espaçamento."""
        x = np.array([0.0, 1.0, 2.0, 4.0])
        y = 2.0 * x + 1.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 20.0)


class TestDiaContrato(unittest.TestCase):
    """Testes de regras do contrato de ajustar_polinomio e dia_de_operacao."""

    def test_ajustar_polinomio_grau_negativo_levanta_value_error(self):
        """ajustar_polinomio levanta ValueError se grau for negativo."""
        with self.assertRaises(ValueError):
            ajustar_polinomio(np.array([1.0, 2.0]), np.array([3.0, 4.0]), -1)

    def test_dia_de_operacao_limite_faixa_ausente_levanta_value_error(self):
        """dia_de_operacao levanta ValueError se algum limite tarifário (0, 18, 21, 24) faltar em t."""
        t_sem_18 = np.array([0.0, 6.0, 12.0, 21.0, 24.0])
        q = np.full_like(t_sem_18, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t_sem_18, q, np.array([40.0]), np.array([0.8]), Trapezio())


if __name__ == "__main__":
    unittest.main()

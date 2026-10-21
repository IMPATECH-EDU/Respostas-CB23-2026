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
class TestRegressaoIssue11(unittest.TestCase):
    """Testes de regressão para integração trapezoidal em malha irregular."""

    def test_trapezio_linear_com_intervalo_irregular(self):
        """Trapézio integra uma função linear exatamente mesmo com uma leitura perdida."""
        x = np.array([0.0, 1.0, 3.0, 4.0])
        y = x.copy()
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 8.0)

    def test_trapezio_constante_com_intervalos_irregulares(self):
        """Vazão constante deve integrar pelo tempo total apesar dos intervalos desiguais."""
        x = np.array([0.0, 1.0, 3.0, 4.0])
        y = np.full(x.size, 2.0)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 8.0)


class TestContratosDia(unittest.TestCase):
    """Testes adicionais dos contratos do Marco 4."""

    def test_ajustar_polinomio_rejeita_grau_negativo(self):
        """Ajuste polinomial rejeita grau negativo."""
        with self.assertRaises(ValueError):
            ajustar_polinomio(np.array([0.0, 1.0]), np.array([1.0, 2.0]), -1)

    def test_dia_de_operacao_exige_limites_de_tarifa(self):
        """Balanço diário rejeita um registro sem os limites das faixas tarifárias."""
        with self.assertRaises(ValueError):
            dia_de_operacao(
                np.array([0.0, 1.0, 24.0]),
                np.array([10.0, 10.0, 10.0]),
                np.array([40.0]),
                np.array([0.8]),
                Trapezio(),
            )


if __name__ == "__main__":
    unittest.main()

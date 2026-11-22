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
    """Testes de regressao da issue #11 escritos antes da correcao de Trapezio.integrar_tabela."""

    def test_trapezio_tabela_malha_irregular_constante(self):
        """Trapezio em malha nao uniforme integra funcao constante usando largura de cada intervalo."""
        x = [0.0, 0.25, 1.0, 2.0]
        y = [4.0, 4.0, 4.0, 4.0]
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 8.0)

    def test_trapezio_tabela_malha_irregular_linear(self):
        """Trapezio integra exatamente funcao afim em pontos com espacamentos distintos."""
        x = [0.0, 0.5, 2.0, 4.0]
        y = [1.0, 2.0, 5.0, 9.0]
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 20.0)


class TestDiaContrato(unittest.TestCase):
    """Testes de contrato de ajustar_polinomio e dia_de_operacao fora da aceitacao."""

    def test_ajustar_polinomio_rejeita_grau_negativo_e_dimensoes_invalidas(self):
        """Grau negativo ou vetores 2D/desiguais levantam ValueError em ajustar_polinomio."""
        with self.assertRaises(ValueError):
            ajustar_polinomio(np.array([0.0, 1.0]), np.array([1.0, 2.0]), -1)
        with self.assertRaises(ValueError):
            ajustar_polinomio(np.array([[0.0, 1.0]]), np.array([[1.0, 2.0]]), 0)
        with self.assertRaises(ValueError):
            ajustar_polinomio(np.array([0.0, 1.0]), np.array([1.0]), 0)

    def test_ajustar_polinomio_grau_zero_retorna_media(self):
        """Ajuste de grau zero devolve array de tamanho 1 igual a media de y."""
        coef = ajustar_polinomio(np.array([1.0, 2.0, 4.0]), np.array([2.0, 5.0, 8.0]), 0)
        self.assertEqual(len(coef), 1)
        self.assertAlmostEqual(float(coef[0]), 5.0)

    def test_dia_de_operacao_exige_todos_os_limites_tarifarios(self):
        """Falta de qualquer limite das faixas tarifarias (ex. 18 h) levanta ValueError."""
        t = np.array([0.0, 12.0, 21.0, 24.0])
        q = np.full_like(t, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, q, np.array([40.0]), np.array([0.8]), Trapezio())


if __name__ == "__main__":
    unittest.main()

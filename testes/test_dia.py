"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import numpy as np
import unittest 
from elevatoria.dia import ajustar_polinomio
from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestTrapezioRegressao(unittest.TestCase):
    def test_constante_em_malha_irregular(self):
        """Integra uma constante usando as larguras reais dos intervalos."""
        x = np.array([0.0, 1.0, 3.0])
        y = np.array([2.0, 2.0, 2.0])

        resultado = Trapezio().integrar_tabela(x, y)

        self.assertAlmostEqual(resultado, 6.0)

    def test_reta_em_malha_irregular(self):
        """Integra exatamente uma reta em pontos com espaçamento irregular."""
        x = np.array([0.0, 1.0, 3.0])
        y = np.array([0.0, 1.0, 3.0])

        resultado = Trapezio().integrar_tabela(x, y)

        self.assertAlmostEqual(resultado, 4.5)


class TestAjustarPolinomioContrato(unittest.TestCase):
    def test_rejeita_grau_negativo(self):
        """Rejeita um grau negativo mesmo com pontos suficientes."""
        x = np.array([0.0, 1.0, 2.0])
        y = np.array([1.0, 3.0, 5.0])

        with self.assertRaises(ValueError):
            ajustar_polinomio(x, y, -1)

    def test_rejeita_entradas_bidimensionais(self):
        """Rejeita x ou y bidimensional, mesmo com tamanhos iguais."""
        vetor = np.array([0.0, 1.0, 2.0])
        matriz = vetor.reshape(3, 1)

        for x, y in ((matriz, vetor), (vetor, matriz)):
            with self.subTest(x_shape=x.shape, y_shape=y.shape):
                with self.assertRaises(ValueError):
                    ajustar_polinomio(x, y, 1)


if __name__ == "__main__":
    unittest.main()

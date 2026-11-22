"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

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


if __name__ == "__main__":
    unittest.main()

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

class TestRegressaoIssue11(unittest.TestCase):

    def test_trapezio_usa_largura_de_cada_intervalo(self):
        """Calcula corretamente a integral em uma malha irregular."""
        x = [0.0, 1.0, 3.0]
        y = [1.0, 3.0, 7.0]

        resultado = Trapezio().integrar_tabela(x, y)

        self.assertAlmostEqual(resultado, 12.0)

    def test_trapezio_com_vazao_constante(self):
        """Calcula corretamente a integral constante com intervalos diferentes."""
        x = [0.0, 1.0, 3.0, 6.0]
        y = [4.0, 4.0, 4.0, 4.0]

        resultado = Trapezio().integrar_tabela(x, y)

        self.assertAlmostEqual(resultado, 24.0)

if __name__ == "__main__":
    unittest.main()

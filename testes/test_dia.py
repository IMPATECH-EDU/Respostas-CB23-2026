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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestTrapezio(unittest.TestCase):
    """Testes de regressão da issue #11."""

    def test_regressao_trapezio(self):
        """O erro do Trapezio é maior do que deveria ser"""
        self.assertAlmostEqual(Trapezio().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.75)

    def test_regressao_trapezio_tabela(self):
        """Só pra verificar se o erro do Trapezio com tabela também é maior do que deveria ser"""
        x = [0.0, 1.5, 3.0]
        y = [xi ** 2 for xi in x]
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 9.75)

if __name__ == "__main__":
    unittest.main()

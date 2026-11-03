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


class TestTrapezioRegressao(unittest.TestCase):
    """Regressões da issue #11 para integração em malhas irregulares."""

    def test_trapezio_constante_malha_irregular(self) -> None:
        """Uma constante mantém a área total com intervalos de larguras diferentes."""
        x = [0.0, 1.0, 3.0]
        y = [2.0, 2.0, 2.0]
        integral = Trapezio().integrar_tabela(x, y)
        # Área do retângulo: 2 * (3 - 0) = 6.
        self.assertAlmostEqual(integral, 6.0)

    def test_trapezio_reta_malha_irregular(self) -> None:
        """A reta y=x integra exatamente com intervalos de larguras 2, 1 e 3."""
        x = [0.0, 2.0, 3.0, 6.0]
        y = [0.0, 2.0, 3.0, 6.0]
        integral = Trapezio().integrar_tabela(x, y)
        # Integral de x entre 0 e 6: 6**2 / 2 = 18.
        self.assertAlmostEqual(integral, 18.0)


if __name__ == "__main__":
    unittest.main()

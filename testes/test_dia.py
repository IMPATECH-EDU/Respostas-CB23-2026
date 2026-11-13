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
    """Testes de regressão do trapézio em malha irregular (issue #11)."""

    def test_funcao_constante_em_malha_irregular(self) -> None:
        """Uma função constante usa a largura total mesmo com intervalos diferentes."""
        resultado = Trapezio().integrar_tabela([0.0, 1.0, 3.0], [2.0, 2.0, 2.0])

        self.assertAlmostEqual(resultado, 6.0)

    def test_reta_em_malha_irregular(self) -> None:
        """O trapézio integra uma reta exatamente também em malha irregular."""
        resultado = Trapezio().integrar_tabela([0.0, 1.0, 3.0], [1.0, 3.0, 7.0])

        self.assertAlmostEqual(resultado, 12.0)


if __name__ == "__main__":
    unittest.main()

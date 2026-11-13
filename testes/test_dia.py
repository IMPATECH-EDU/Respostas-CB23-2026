"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.integracao import Simpson, Trapezio
from elevatoria.dia import ajustar_polinomio


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


class TestAjustarPolinomio(unittest.TestCase):
    """Verifica entradas inválidas no ajuste por mínimos quadrados."""

    def test_grau_negativo(self) -> None:
        """Um grau negativo levanta ValueError com uma mensagem explicativa."""
        with self.assertRaisesRegex(ValueError, "grau"):
            ajustar_polinomio([0.0, 1.0], [1.0, 2.0], -1)

    def test_tamanhos_diferentes(self) -> None:
        """Os vetores de entrada e saída devem ter o mesmo tamanho."""
        with self.assertRaisesRegex(ValueError, "mesmo tamanho"):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_entrada_bidimensional(self) -> None:
        """O ajuste rejeita matrizes tanto em x quanto em y."""
        for x, y in [([[0.0, 1.0]], [1.0, 2.0]),
                     ([0.0, 1.0], [[1.0, 2.0]])]:
            with self.subTest(x=x, y=y), self.assertRaisesRegex(ValueError, "1D"):
                ajustar_polinomio(x, y, 1)


if __name__ == "__main__":
    unittest.main()

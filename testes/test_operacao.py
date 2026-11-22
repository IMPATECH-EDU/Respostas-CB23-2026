"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressao da issue #9 escritos antes da correcao de Newton."""

    def test_newton_colebrook_converge_em_poucas_iteracoes(self):
        """Newton resolve Colebrook para Re=1e4 com tolerancia 1e-12 em ate 6 iteracoes."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_newton_reavalia_derivada_em_pontos_distintos(self):
        """Newton recalcula a derivada a cada iteracao para manter convergencia quadratica."""
        pontos: list[float] = []

        def df(x: float) -> float:
            pontos.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertGreater(len(set(pontos)), 1)
        self.assertLessEqual(resultado.iteracoes, 6)


if __name__ == "__main__":
    unittest.main()

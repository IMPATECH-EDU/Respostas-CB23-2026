"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoNewton(unittest.TestCase):
    """Testes de regressão da issue #9 ANTES da correção."""

    def test_newton_iteracoes_colebrook_re_1e4(self):
        """Para Re = 10^4 em Colebrook, Newton deve convergir em no máximo 6 iterações."""
        from fornecido.hidraulica import fator_atrito_colebrook
        from elevatoria.raizes import Newton
        _, res = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(res.iteracoes, 6)

    def test_newton_convergencia_quadratica_polinomio(self):
        """Para f(x) = x^2 - 2, Newton deve convergir quadraticamente em no máximo 6 iterações."""
        from elevatoria.raizes import Newton
        res = Newton(tol=1e-12).encontrar(lambda x: x ** 2 - 2.0, 0.0, 2.0)
        self.assertLessEqual(res.iteracoes, 6)


if __name__ == "__main__":
    unittest.main()

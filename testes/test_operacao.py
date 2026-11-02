"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import numpy as np

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import Tubulacao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestIssue9Regressao(unittest.TestCase):
    def test_newton_convergencia_quadratica(self):
        """Verifica se o método de Newton apresenta ordem de convergência quadrática (p > 1.8)."""
        def f(x):
            return x**2 - 2.0

        def df(x):
            return 2.0 * x

        newton = Newton(tol=1e-12, df=df)
        res = newton.encontrar(f, 1.0, 2.0)
        p = ordem_convergencia(res.historico, res.raiz)
        self.assertGreater(p, 1.8)

    def test_newton_poucas_iteracoes_para_precisao_alta(self):
        """Garante que o Newton exige no máximo 6 iterações para f(x) = x^2 - 2 com tol=1e-10."""
        def f(x):
            return x**2 - 2.0

        def df(x):
            return 2.0 * x

        newton = Newton(tol=1e-10, df=df)
        res = newton.encontrar(f, 1.0, 2.0)
        self.assertLessEqual(res.iteracoes, 6)


class TestOperacaoContrato(unittest.TestCase):
    def test_ponto_operacao_rejeita_intervalo_invalido(self):
        """Levanta ValueError se a for maior ou igual a b."""
        c = CurvaCalibracao(np.array([0.0, 50.0, 100.0]), np.array([50.0, 30.0, 10.0]), "linear")
        tub = Tubulacao(comprimento=100.0, diametro=0.2, rugosidade=0.0001, desnivel=10.0, resolvedor=Bisseccao())
        with self.assertRaises(ValueError):
            ponto_operacao(c, tub, Bisseccao(), a=50.0, b=10.0)

    def test_ordem_convergencia_poucos_erros(self):
        """Levanta ValueError quando há menos de 3 erros acima do piso especificado."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.5, 1.0], 1.0)


if __name__ == "__main__":
    unittest.main()
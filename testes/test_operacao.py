"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9: o Newton precisa recalcular a derivada a cada passo."""

    def test_recalcula_a_derivada_a_cada_iteracao(self):
        """Issue #9: a derivada é avaliada uma vez por iteração, e não uma vez só."""
        chamadas = []

        def df(x):
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-10, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 4.0)
        self.assertEqual(len(chamadas), resultado.iteracoes)

    def test_converge_em_poucas_iteracoes(self):
        """Issue #9: x² - 2 a partir de 2 converge quadraticamente, em no máximo 6 iterações."""
        resultado = Newton(tol=1e-10).encontrar(lambda x: x * x - 2.0, 0.0, 4.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=9)
        self.assertLessEqual(resultado.iteracoes, 6)


class TubulacaoFalsa:
    """Sistema de teste: altura exigida constante, sem hidráulica."""

    def __init__(self, altura):
        self._altura = altura

    def altura_sistema(self, Q):
        return self._altura


class TestPontoOperacao(unittest.TestCase):
    """Testes de `ponto_operacao` (issue #8) com uma bomba reta: H = 40 - 0,4·Q."""

    def setUp(self):
        self.bomba = CurvaCalibracao([0.0, 50.0, 100.0], [40.0, 20.0, 0.0], "linear")

    def test_intervalo_invalido(self):
        """ponto_operacao: a >= b levanta ValueError."""
        for a, b in [(60.0, 60.0), (80.0, 20.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(self.bomba, TubulacaoFalsa(20.0), Bisseccao(), a, b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """ponto_operacao: [a, b] fora do domínio da bomba levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, TubulacaoFalsa(20.0), Bisseccao(), 10.0, 150.0)

    def test_nao_convergiu(self):
        """ponto_operacao: se o resolvedor não convergir, levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, TubulacaoFalsa(20.0), Bisseccao(tol=1e-12, max_iter=3))

    def test_erro_do_resolvedor_chega_a_quem_chamou(self):
        """ponto_operacao: sem troca de sinal, o ValueError da bissecção não é tratado."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, TubulacaoFalsa(100.0), Bisseccao(tol=1e-10))

    def test_vazao_e_altura(self):
        """ponto_operacao: devolve Q = 50 L/s e a altura da bomba nesse ponto (20 m)."""
        ponto = ponto_operacao(self.bomba, TubulacaoFalsa(20.0), Bisseccao(tol=1e-10))
        self.assertAlmostEqual(ponto.vazao, 50.0, places=6)
        self.assertAlmostEqual(ponto.altura, self.bomba(ponto.vazao))
        self.assertAlmostEqual(ponto.altura, 20.0, places=5)


class TestOrdemConvergencia(unittest.TestCase):
    """Testes de `ordem_convergencia` (issue #8): o piso de erro."""

    def test_ignora_erros_no_nivel_do_arredondamento(self):
        """ordem_convergencia: um erro de 1e-15 (abaixo do piso) não entra na estimativa."""
        historico = [1.1, 1.01, 1.0001, 1.0 + 1e-15]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, delta=0.01)

    def test_piso_e_relativo_ao_tamanho_da_raiz(self):
        """ordem_convergencia: com raiz 1000, o piso é piso·|raiz| e o erro 1e-12 é ignorado."""
        historico = [1001.0, 1000.1, 1000.001, 1000.0 + 1e-12]
        self.assertAlmostEqual(ordem_convergencia(historico, 1000.0), 2.0, delta=0.01)


if __name__ == "__main__":
    unittest.main()
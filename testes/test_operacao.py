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
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook


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


class TestOperacaoContrato(unittest.TestCase):
    """Testes de contrato para ponto_operacao e ordem_convergencia nao cobertos pela aceitacao."""

    def setUp(self):
        vazoes = np.arange(0.0, 101.0, 10.0)
        self.bomba = CurvaCalibracao(vazoes, 50.0 - 0.004 * vazoes ** 2, "spline")
        self.tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

    def test_ponto_operacao_rejeita_intervalo_invalido_ou_fora_do_dominio(self):
        """Intervalo invertido ou fora de bomba.dominio levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(), a=60.0, b=60.0)
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(), a=10.0, b=110.0)

    def test_ponto_operacao_levanta_erro_se_nao_convergir(self):
        """Levanta ValueError quando o resolvedor encerra sem convergir."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(tol=1e-12, max_iter=1))

    def test_ordem_convergencia_respeita_piso_relativo_a_raiz(self):
        """Descarta erros abaixo de piso * max(1, |raiz|) antes de estimar a ordem."""
        raiz = 1000.0
        # Apenas os 3 primeiros erros superam piso * 1000 = 1e-11; os ultimos ficam no ruido.
        historico = [1001.0, 1000.1, 1000.001, 1000.0 + 1e-12, 1000.0 + 1e-13]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz, piso=1e-14), 2.0, delta=0.05)
        with self.assertRaises(ValueError):
            ordem_convergencia(historico[1:], raiz, piso=1e-14)


if __name__ == "__main__":
    unittest.main()

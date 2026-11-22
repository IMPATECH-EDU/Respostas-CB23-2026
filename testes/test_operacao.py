"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

import numpy as np

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook

RUGOSIDADE_RELATIVA = 0.15e-3 / 0.20
VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")


def _tubulacao() -> Tubulacao:
    """A adutora da estação, com o Newton resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Newton(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton calculava a derivada uma vez só e convergia linearmente."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Colebrook com Re = 1e4 e tol = 1e-12 converge em no máximo 6 iterações (eram 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_2_converge_rapido(self):
        """x² − 2 a partir de x0 = 1 converge em no máximo 6 iterações (eram mais de 30)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_avaliada_a_cada_iteracao(self):
        """Com df fornecida, df é chamada uma vez por iteração, sempre no ponto atual."""
        pontos = []

        def df(x: float) -> float:
            pontos.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertEqual(len(pontos), resultado.iteracoes)
        self.assertEqual(pontos, list(resultado.historico[:-1]))


class TestContratoPontoOperacao(unittest.TestCase):
    """Issue #8: regras do contrato de ponto_operacao que os testes de aceitação não verificam."""

    def test_intervalo_invertido(self):
        """a >= b levanta ValueError antes de chamar o resolvedor."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=90.0, b=40.0)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Um intervalo que sai do domínio do ensaio (0 a 100 L/s) levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=10.0, b=120.0)

    def test_resolvedor_que_nao_converge(self):
        """Se o resolvedor para em max_iter sem convergir, ponto_operacao levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "convergiu"):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(tol=1e-10, max_iter=3))


class TestContratoOrdemConvergencia(unittest.TestCase):
    """Issue #8: regras do contrato de ordem_convergencia que os testes de aceitação não verificam."""

    def test_piso_relativo_a_raiz(self):
        """O piso é relativo a |raiz|: com raiz 1e6, um erro de 1e-9 fica abaixo dele e é ignorado."""
        raiz = 1e6
        historico = [raiz + 0.5 ** k for k in range(1, 6)] + [raiz + 1e-9]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 1.0, delta=1e-6)

    def test_usa_os_tres_ultimos_acima_do_piso(self):
        """Erros 1e-1, 1e-2, 1e-6 dão p = log(1e-4)/log(1e-1) = 4, ignorando os erros iniciais."""
        historico = [3.0, 2.0, 1.1, 1.01, 1.000001, 1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 4.0, delta=1e-6)

    def test_erros_consecutivos_iguais(self):
        """Dois erros consecutivos iguais levantam ValueError, e não ZeroDivisionError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.5, 0.5, 1.5, 1.25], 1.0)


if __name__ == "__main__":
    unittest.main()

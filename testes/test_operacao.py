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

VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")


def _tubulacao_padrao() -> Tubulacao:
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoIssue9(unittest.TestCase):
    """Testes de regressão para a issue #9 (convergência lenta do Newton)."""

    def test_newton_poucas_iteracoes_colebrook(self):
        """Newton deve convergir na equação de Colebrook para Re=10^4 em no máximo 6 iterações."""
        _, res = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(res.iteracoes, 6)

    def test_newton_ordem_convergencia_quadratica(self):
        """Newton deve apresentar ordem de convergência quadrática (p > 1.8) ao encontrar raiz."""
        res = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 1.0, 2.0)
        erros = [abs(x - math.sqrt(2.0)) for x in res.historico if abs(x - math.sqrt(2.0)) > 1e-13]
        self.assertGreaterEqual(len(erros), 3)
        p = math.log(erros[-1] / erros[-2]) / math.log(erros[-2] / erros[-3])
        self.assertGreater(p, 1.8)


class TestOperacaoContrato(unittest.TestCase):
    """Testes de regras do contrato de ponto_operacao e ordem_convergencia."""

    def test_ponto_operacao_intervalo_invalido(self):
        """ponto_operacao levanta ValueError se a >= b."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao_padrao(), Bisseccao(), a=50.0, b=50.0)
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao_padrao(), Bisseccao(), a=60.0, b=40.0)

    def test_ponto_operacao_fora_do_dominio(self):
        """ponto_operacao levanta ValueError se [a, b] ultrapassar o domínio da curva da bomba."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao_padrao(), Bisseccao(), a=-5.0, b=50.0)
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao_padrao(), Bisseccao(), a=10.0, b=120.0)

    def test_ordem_convergencia_poucos_erros_levanta_value_error(self):
        """ordem_convergencia levanta ValueError se houver menos de 3 erros acima do piso."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.01, 1.0001], 1.0)


if __name__ == "__main__":
    unittest.main()

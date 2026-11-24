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


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: o Newton deve convergir quadraticamente (derivada recalculada a cada passo)."""

    def test_poucas_iteracoes_em_colebrook(self):
        """Colebrook com Re = 1e4 converge em no máximo 6 iterações."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-10))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_dois_em_poucas_iteracoes(self):
        """x² - 2 em [0, 4] converge em no máximo 6 iterações, e não em dezenas."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 4.0)
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=10)

    def test_erro_cai_mais_rapido_que_linear(self):
        """Perto da raiz, cada erro é menor que o quadrado do anterior vezes uma constante."""
        resultado = Newton(tol=1e-13).encontrar(lambda x: x * x - 2.0, 0.0, 4.0)
        erros = [abs(x - math.sqrt(2.0)) for x in resultado.historico]
        # o último passo (erro ~1e-16) está no nível do arredondamento
        e0, e1, e2 = erros[-4], erros[-3], erros[-2]
        self.assertLess(e1, 2.0 * e0 ** 2)
        self.assertLess(e2, 2.0 * e1 ** 2)


class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: regras do contrato de `ponto_operacao` que a aceitação não verifica."""

    def setUp(self):
        self.tub = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

    def test_intervalo_invertido(self):
        """Com a >= b, ponto_operacao levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, self.tub, Bisseccao(), a=90.0, b=20.0)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Um intervalo que sai do domínio da bomba (0 a 100) levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, self.tub, Bisseccao(), a=10.0, b=150.0)

    def test_resolvedor_que_nao_converge(self):
        """Se o resolvedor para por max_iter, ponto_operacao levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, self.tub, Bisseccao(tol=1e-12, max_iter=3))


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: regras do contrato de `ordem_convergencia` que a aceitação não verifica."""

    def test_ignora_erros_abaixo_do_piso(self):
        """Erros no nível do arredondamento são descartados antes de estimar p."""
        historico = [1 + 1e-1, 1 + 1e-2, 1 + 1e-4, 1 + 1e-8, 1 + 1e-16, 1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, delta=0.01)

    def test_so_dois_erros_acima_do_piso(self):
        """Com só dois erros acima do piso, o resultado é ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1 + 1e-1, 1 + 1e-2, 1.0], 1.0)


if __name__ == "__main__":
    unittest.main()

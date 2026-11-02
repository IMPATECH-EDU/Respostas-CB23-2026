"""Testes de aceitação do Marco 3 (código fornecido; NÃO ALTERE).

Conferem o contrato público de `elevatoria/operacao.py` (issue #8) e documentam o uso do
código que já existia: `elevatoria/raizes.py` e `fornecido/hidraulica.py`. Passar em todos
eles é necessário, mas não basta: eles não cobrem todos os casos (veja a issue #9). Os seus
próprios testes ficam em `testes/`.
"""
import math
import unittest

import numpy as np

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import PontoOperacao, ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, MetodoRaiz, Newton, ResultadoRaiz
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook

VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²


def tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestPontoOperacao(unittest.TestCase):
    """Issue #8: ponto_operacao."""

    def test_bomba_e_sistema_se_igualam(self):
        tub = tubulacao()
        ponto = ponto_operacao(BOMBA, tub, Bisseccao(tol=1e-10))
        self.assertIsInstance(ponto, PontoOperacao)
        self.assertIsInstance(ponto.resultado, ResultadoRaiz)
        self.assertTrue(10.0 <= ponto.vazao <= 100.0)
        self.assertAlmostEqual(ponto.altura, BOMBA(ponto.vazao))
        self.assertLess(abs(BOMBA(ponto.vazao) - tub.altura_sistema(ponto.vazao)), 1e-6)

    def test_metodos_concordam(self):
        tub = tubulacao()
        bis = ponto_operacao(BOMBA, tub, Bisseccao(tol=1e-10))
        new = ponto_operacao(BOMBA, tub, Newton(tol=1e-10))
        self.assertAlmostEqual(bis.vazao, new.vazao, delta=1e-6)

    def test_usa_o_intervalo(self):
        ponto = ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10), a=40.0, b=90.0)
        self.assertTrue(40.0 <= ponto.vazao <= 90.0)
        with self.assertRaises(ValueError):   # sem troca de sinal em [10, 40]
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10), a=10.0, b=40.0)


class TestOrdemConvergencia(unittest.TestCase):
    """Issue #8: ordem_convergencia."""

    def test_quadratica(self):
        # começa devagar (erros caindo à metade) e termina quadrática: valem os últimos erros
        historico = [1.5, 1.25, 1.125, 1 + 1e-2, 1 + 1e-4, 1 + 1e-8, 1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, delta=0.01)

    def test_linear(self):
        historico = [1 + 0.5 ** k for k in range(1, 30)] + [1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 1.0, delta=0.01)

    def test_poucos_erros(self):
        with self.assertRaises(ValueError):
            ordem_convergencia([1.5, 1.0], 1.0)


class TestCodigoExistente(unittest.TestCase):
    """Código que já existia na base: exemplos de uso."""

    def test_metodos_de_raiz(self):
        with self.assertRaises(TypeError):
            MetodoRaiz()
        for metodo in (Bisseccao(tol=1e-12), Newton(tol=1e-12)):
            with self.subTest(metodo=type(metodo).__name__):
                resultado = metodo.encontrar(lambda x: x * x - 2, 0.0, 2.0)
                self.assertTrue(resultado.convergiu)
                self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=9)
        with self.assertRaises(ValueError):
            Bisseccao().encontrar(lambda x: x * x + 1, -1.0, 1.0)

    def test_hidraulica(self):
        f, _ = fator_atrito_colebrook(1e5, 0.15e-3 / 0.20, Bisseccao(tol=1e-12))
        self.assertAlmostEqual(f, 0.02130, delta=5e-5)
        tub = tubulacao()
        self.assertEqual(tub.altura_sistema(0.0), 18.0)
        self.assertAlmostEqual(tub.altura_sistema(60.0), 33.227, delta=1e-3)


if __name__ == "__main__":
    unittest.main()

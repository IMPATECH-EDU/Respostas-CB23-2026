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

import math

from elevatoria.operacao import ordem_convergencia
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook

import numpy as np

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ponto_operacao
from fornecido.hidraulica import Tubulacao


class TestNewton(unittest.TestCase):
    """Issue #9: o Newton deve ter ordem de convergência perto de 2."""

    def test_ordem_colebrook_re_10_000(self):
        """O caso do relato: em Colebrook com Re = 10^4, a ordem do Newton é maior que 1.8."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        ordem = ordem_convergencia(resultado.historico, resultado.raiz)
        self.assertGreater(ordem, 1.8)

    def test_ordem_colebrook_re_100_000(self):
        """Em Colebrook com Re = 10^5, a ordem do Newton também é maior que 1.8."""
        _, resultado = fator_atrito_colebrook(1e5, 0.15e-3 / 0.20, Newton(tol=1e-12))
        ordem = ordem_convergencia(resultado.historico, resultado.raiz)
        self.assertGreater(ordem, 1.8)

    def test_ordem_raiz_de_2(self):
        """Na raiz de x² - 2 em [0, 2], a ordem do Newton é maior que 1.8."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        ordem = ordem_convergencia(resultado.historico, math.sqrt(2))
        self.assertGreater(ordem, 1.8)


VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²


def tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestPontoOperacao(unittest.TestCase):
    """Issue #8: regras do contrato de ponto_operacao que os testes de aceitação não verificam."""

    def test_intervalo_invertido(self):
        """Com a >= b, levanta ValueError mesmo com o Newton, que não confere o intervalo."""
        for a, b in [(90.0, 40.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, tubulacao(), Newton(tol=1e-10), a=a, b=b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Com [a, b] saindo do domínio da bomba (0 a 100 L/s), levanta ValueError mesmo com o Newton."""
        for a, b in [(-10.0, 90.0), (10.0, 130.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, tubulacao(), Newton(tol=1e-10), a=a, b=b)

    def test_resolvedor_nao_convergiu(self):
        """Se o resolvedor para em max_iter sem convergir, levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10, max_iter=3))

if __name__ == "__main__":
    unittest.main()

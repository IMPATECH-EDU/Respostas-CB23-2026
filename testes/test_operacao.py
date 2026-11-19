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


def adutora() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: o Newton convergia devagar. Escritos antes da correção."""

    def test_colebrook_com_re_1e4(self):
        """Colebrook em Re = 1e4 converge em até 6 iterações (o relato via 10)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_erro_cai_ao_quadrado(self):
        """Em x² - 2 com a derivada exata, cada erro fica abaixo do quadrado do anterior."""
        r = Newton(tol=1e-12, df=lambda x: 2 * x).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        erros = [abs(x - math.sqrt(2)) for x in r.historico]
        for k in (1, 2, 3):
            with self.subTest(k=k):
                self.assertLess(erros[k + 1], erros[k] ** 2)


class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: quando ponto_operacao recusa o intervalo ou o resultado."""

    def test_intervalo_vazio(self):
        """a = b levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "a < b"):
            ponto_operacao(BOMBA, adutora(), Bisseccao(), a=80.0, b=80.0)

    def test_intervalo_alem_do_ensaio(self):
        """b = 120 L/s passa do ensaio, que vai até 100 L/s, e levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(BOMBA, adutora(), Bisseccao(), a=10.0, b=120.0)

    def test_resolvedor_que_nao_converge(self):
        """Bissecção com max_iter=5 não chega a tol=1e-12, e isso vira ValueError."""
        with self.assertRaisesRegex(ValueError, "convergiu"):
            ponto_operacao(BOMBA, adutora(), Bisseccao(tol=1e-12, max_iter=5))

    def test_newton_escapando_do_intervalo(self):
        """Em [10, 40], sem raiz, o Newton iria parar em 62 L/s; ponto_operacao recusa."""
        with self.assertRaisesRegex(ValueError, "fora"):
            ponto_operacao(BOMBA, adutora(), Newton(tol=1e-10), a=10.0, b=40.0)


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: o piso relativo de ordem_convergencia e o caso degenerado."""

    def test_piso_relativo_a_raiz(self):
        """Com raiz 1e6 o piso vira 1e-8, e o erro de 1e-9 fica fora da conta."""
        raiz = 1e6
        historico = [raiz + 1e-1, raiz + 1e-2, raiz + 1e-4, raiz + 1e-9]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 2.0, delta=0.01)

    def test_erros_parados(self):
        """Erros que não mudam deixam a ordem indefinida e levantam ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([2.0, 2.0, 2.0], 1.0)


if __name__ == "__main__":
    unittest.main()

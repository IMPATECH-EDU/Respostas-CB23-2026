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

VAZOES = np.arange(0.0,101.0,10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")

def tubulacao():
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))

class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: o Newton calculava a derivada uma vez só e convergia devagar."""
    def test_raiz_de_dois_em_poucas_iteracoes(self):
        """Newton para x² - 2 com tol 1e-12 converge em no máximo 7 iterações (o defeito dava 32)."""
        resultado = Newton(tol=1e-12, df=lambda x: 2 * x).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 7)

def test_derivada_e_chamada_a_cada_iteracao(self):
    """Com df fornecida, ela é avaliada uma vez por iteração (o defeito a chamava uma vez só)."""
    chamadas = []
    def df(x):
        chamadas.append(x)
        return 2 * x
    resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2, 0.0, 2.0)
    self.assertEqual(len(chamadas), resultado.iteracoes)

def test_erros_caem_quadraticamente(self):
    """Perto da raiz, cada erro é no máximo o quadrado do anterior (os dígitos dobram)."""
    raiz = 2 ** 0.5
    resultado = Newton(tol=1e-12, df=lambda x: 2 * x).encontrar(lambda x: x * x - 2, 0.0, 2.0)
    erros = [abs(x - raiz) for x in resultado.historico]
    pares = [(e0, e1) for e0, e1 in zip(erros, erros[1:]) if 1e-7 < e0 < 1e-1]
    self.assertGreaterEqual(len(pares), 2)
    for e0, e1 in pares:
        self.assertLessEqual(e1, e0 ** 2)

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """O caso do relato: Colebrook com Re = 1e4 pelo Newton leva no máximo 6 iterações (eram 10)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

if __name__ == "__main__":
    unittest.main()

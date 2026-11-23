"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from elevatoria.calibracao import CurvaCalibracao
from fornecido.hidraulica import Tubulacao
import numpy as np

VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²


def tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoIssue9(unittest.TestCase):
    """Testes de regressão para a issue #9 (convergência quadrática do Newton)."""

    def test_newton_convergencia_quadratica(self):
        """Verifica que o Newton atinge ordem de convergência quadrática (~2) em função não linear."""
        res = Newton(tol=1e-13).encontrar(lambda x: x ** 2 - 2.0, 0.0, 4.0)
        self.assertTrue(res.convergiu)
        self.assertAlmostEqual(ordem_convergencia(res.historico, res.raiz), 2.0, delta=0.05)

    def test_newton_poucas_iteracoes(self):
        """Garante que o Newton converge em poucas iterações (<= 7) em vez de decair para linear."""
        res = Newton(tol=1e-12).encontrar(lambda x: x ** 3 - 2.0 * x - 5.0, 0.0, 5.0)
        self.assertTrue(res.convergiu)
        self.assertLessEqual(res.iteracoes, 7)


class TestContratoOperacao(unittest.TestCase):
    """Testes de contrato para ponto_operacao e ordem_convergencia."""

    def test_ponto_operacao_intervalo_degenerado_ou_invertido(self):
        """Levanta ValueError quando a >= b em ponto_operacao."""
        tub = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Newton(tol=1e-12))
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tub, Bisseccao(), a=50.0, b=50.0)
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tub, Bisseccao(), a=60.0, b=40.0)

    def test_ponto_operacao_fora_do_dominio(self):
        """Levanta ValueError quando [a, b] ultrapassa os limites de bomba.dominio."""
        tub = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Newton(tol=1e-12))
        d_min, d_max = BOMBA.dominio
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tub, Bisseccao(), a=d_min - 1.0, b=d_max)
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tub, Bisseccao(), a=d_min, b=d_max + 1.0)

    def test_ponto_operacao_resolvedor_nao_converge(self):
        """Levanta ValueError quando o resolvedor retorna convergiu=False."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-12, max_iter=1))

    def test_ordem_convergencia_piso_escalado_pela_raiz(self):
        """Descarta erros abaixo de piso * max(1, |raiz|) antes de estimar a ordem."""
        raiz = 1e6
        historico = [raiz + 1e-1, raiz + 1e-2, raiz + 1e-4, raiz + 1e-10, raiz + 1e-12, raiz]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz, piso=1e-14), 2.0, delta=0.01)
        with self.assertRaises(ValueError):
            ordem_convergencia(historico[1:], raiz, piso=1e-14)

if __name__ == "__main__":
    unittest.main()

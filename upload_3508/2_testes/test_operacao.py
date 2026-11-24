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

RUGOSIDADE_RELATIVA = 0.15e-3 / 0.20     # a adutora da estação


def _quadrado_menos_dois(x: float) -> float:
    """f(x) = x² - 2, de raiz sqrt(2)."""
    return x * x - 2.0


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton precisa recalcular a derivada a cada iteração (convergência quadrática)."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Colebrook com Re = 1e4 converge em no máximo 6 iterações, e não em 10 como no relato."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_exata_tambem_e_reavaliada(self):
        """Com df fornecida, sqrt(2) sai em no máximo 6 iterações: df também deve ser chamada a cada passo."""
        resultado = Newton(tol=1e-12, df=lambda x: 2.0 * x).encontrar(_quadrado_menos_dois, 0.0, 2.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_erro_novo_limitado_pelo_quadrado_do_anterior(self):
        """Perto da raiz, e_(k+1) <= e_k² em f = x² - 2 (no Newton, e_(k+1) ~ e_k² / (2 sqrt(2)))."""
        resultado = Newton(tol=1e-12).encontrar(_quadrado_menos_dois, 0.0, 2.0)
        erros = [abs(x - math.sqrt(2.0)) for x in resultado.historico]
        pares = [(e, prox) for e, prox in zip(erros, erros[1:]) if e < 0.1 and prox > 1e-14]
        self.assertGreaterEqual(len(pares), 2)
        pior_razao = max(prox / (e * e) for e, prox in pares)   # Newton: ≈ 1/(2√2) ≈ 0,35
        self.assertLessEqual(pior_razao, 1.0)




class TestContratoPontoOperacao(unittest.TestCase):
    """Issue #8: regras da docstring de ponto_operacao que os testes de aceitação não verificam."""

    def setUp(self):
        vazoes = np.arange(0.0, 101.0, 10.0)
        self.bomba = CurvaCalibracao(vazoes, 45.0 - 0.0022 * vazoes ** 2, "spline")
        self.tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

    def test_intervalo_invertido_ou_vazio(self):
        """a >= b é ValueError, para a = b e para a > b."""
        for a, b in [(50.0, 50.0), (80.0, 20.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(self.bomba, self.tubulacao, Bisseccao(), a=a, b=b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """[a, b] que passa de 100 L/s (fim do ensaio) é ValueError antes de resolver."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(), a=10.0, b=120.0)

    def test_resolvedor_que_nao_converge(self):
        """Uma bissecção com só 3 iterações não converge: ValueError, sem devolver um ponto ruim."""
        with self.assertRaisesRegex(ValueError, "não convergiu"):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(tol=1e-10, max_iter=3))

    def test_newton_com_raiz_fora_do_intervalo(self):
        """Em [10, 40] não há raiz; o Newton escapa para Q ~ 65, e isso é ValueError."""
        with self.assertRaisesRegex(ValueError, "fora de"):
            ponto_operacao(self.bomba, self.tubulacao, Newton(tol=1e-10), a=10.0, b=40.0)


class TestContratoOrdemConvergencia(unittest.TestCase):
    """Issue #8: regras da docstring de ordem_convergencia que a aceitação não verifica."""

    def test_erros_abaixo_do_piso_sao_ignorados(self):
        """Ruído de arredondamento no fim (1e-16) não entra: valem 1e-2, 1e-4 e 1e-8."""
        historico = [2.0 + e for e in (1e-1, 1e-2, 1e-4, 1e-8, 3e-16, -4e-16)]
        self.assertAlmostEqual(ordem_convergencia(historico, 2.0), 2.0, delta=0.01)

    def test_piso_relativo_ao_tamanho_da_raiz(self):
        """Com raiz 1e6, o corte é 1e-14 · 1e6 = 1e-8: o erro 1e-9 já não conta."""
        historico = [1e6 + e for e in (1.0, 1e-1, 1e-3, 1e-9)]
        self.assertAlmostEqual(ordem_convergencia(historico, 1e6), 2.0, delta=0.01)

    def test_convergencia_cubica(self):
        """Erros 1e-1, 1e-3, 1e-9 dão ordem 3."""
        self.assertAlmostEqual(ordem_convergencia([0.1, 1e-3, 1e-9], 0.0), 3.0, delta=0.01)

    def test_erros_parados(self):
        """Dois erros iguais seguidos não permitem estimar a ordem: ValueError, não ZeroDivisionError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.5, 1.5, 1.25], 1.0)


if __name__ == "__main__":
    unittest.main()

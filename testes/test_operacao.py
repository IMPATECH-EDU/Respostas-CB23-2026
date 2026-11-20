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

# Bomba de teste definida só entre 20 e 90 L/s: H = 48 − 0,003·Q².
_Q = np.arange(20.0, 91.0, 10.0)
BOMBA_CURTA = CurvaCalibracao(_Q, 48.0 - 0.003 * _Q ** 2, "spline")


def _adutora() -> Tubulacao:
    """A adutora da estação, resolvendo Colebrook pelo Newton."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Newton(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton usava a derivada do ponto inicial em todas as iterações."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Em Re = 10⁴ o Newton resolve Colebrook em no máximo 6 iterações (antes levava 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_dois_converge_quadraticamente(self):
        """Em x² − 2 a partir de 1, o erro de cada passo é da ordem do quadrado do anterior."""
        resultado = Newton(tol=1e-12, df=lambda x: 2.0 * x).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertLessEqual(resultado.iteracoes, 6)
        erros = [abs(x - math.sqrt(2.0)) for x in resultado.historico[:4]]   # antes do arredondamento
        for anterior, seguinte in zip(erros, erros[1:]):
            self.assertLess(seguinte, anterior ** 2)       # e_{k+1} ≈ e_k² / (2√2) < e_k²

    def test_derivada_reavaliada_em_cada_aproximacao(self):
        """Com df fornecida, ela é chamada em cada aproximação, e não só no ponto inicial."""
        pontos = []

        def derivada(x: float) -> float:
            pontos.append(x)
            return 3.0 * x * x

        resultado = Newton(tol=1e-12, df=derivada).encontrar(lambda x: x ** 3 - 8.0, 1.0, 4.0)
        self.assertAlmostEqual(resultado.raiz, 2.0, places=10)
        self.assertEqual(len(set(pontos)), resultado.iteracoes)


class TestContratoPontoOperacao(unittest.TestCase):
    """Regras da docstring de ponto_operacao que os testes de aceitação não verificam."""

    def test_intervalo_invertido_ou_degenerado(self):
        """a >= b levanta ValueError antes de chamar o resolvedor."""
        for a, b in [(60.0, 30.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA_CURTA, _adutora(), Bisseccao(), a, b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Os valores padrão [10, 100] saem do domínio [20, 90] da bomba: ValueError."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(BOMBA_CURTA, _adutora(), Bisseccao())

    def test_resolvedor_que_nao_converge(self):
        """Se o resolvedor para em max_iter sem convergir, ponto_operacao levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA_CURTA, _adutora(), Bisseccao(tol=1e-12, max_iter=3), 20.0, 90.0)

    def test_dentro_do_dominio_funciona(self):
        """Com [a, b] dentro do domínio, a bomba e o sistema se igualam na vazão encontrada."""
        adutora = _adutora()
        ponto = ponto_operacao(BOMBA_CURTA, adutora, Newton(tol=1e-10), 20.0, 90.0)
        self.assertTrue(ponto.resultado.convergiu)
        self.assertAlmostEqual(ponto.altura, adutora.altura_sistema(ponto.vazao), places=6)


class TestContratoOrdemConvergencia(unittest.TestCase):
    """Regras da docstring de ordem_convergencia que os testes de aceitação não verificam."""

    def test_piso_escala_com_a_raiz(self):
        """Com raiz 1e6, o piso vira 1e-8: o erro 1e-9 é descartado e a ordem continua 2."""
        raiz = 1e6
        historico = [raiz + e for e in (1e-1, 1e-2, 1e-4, 1e-8)] + [raiz + 1e-9]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 2.0, delta=0.05)

    def test_erros_abaixo_do_piso_nao_contam(self):
        """Erros abaixo do piso não completam os 3 necessários: ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([2.0 + 1e-3, 2.0 + 1e-6, 2.0 + 1e-15, 2.0], 2.0)

    def test_usa_os_tres_ultimos_uteis(self):
        """Uma fase rápida no começo não muda a estimativa: valem só os três últimos erros úteis."""
        historico = [1e-1, 1e-3, 1e-9] + [1e-9 / 2 ** k for k in range(1, 6)]   # raiz 0
        self.assertAlmostEqual(ordem_convergencia(historico, 0.0), 1.0, delta=1e-9)


if __name__ == "__main__":
    unittest.main()

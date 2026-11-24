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
from elevatoria.raizes import Bisseccao, Newton, ResultadoRaiz
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook

RUGOSIDADE_RELATIVA = 0.15e-3 / 0.20
VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²


def tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class ResolvedorEspiao:
    """Resolvedor falso: guarda `f`, `a` e `b` e devolve um resultado combinado."""

    def __init__(self, resultado: ResultadoRaiz) -> None:
        self.resultado = resultado
        self.chamada = None

    def encontrar(self, f, a, b):
        """Registra os argumentos e devolve o resultado combinado."""
        self.chamada = (f, a, b)
        return self.resultado


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton calculava a derivada uma vez só."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Re = 1e4 em Colebrook converge em até 6 iterações (antes: 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_dois_em_poucas_iteracoes(self):
        """Em x² - 2, chega a 1e-12 em até 8 iterações (antes: 32)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 8)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)

    def test_derivada_e_avaliada_a_cada_iteracao(self):
        """`df` é chamada uma vez por iteração."""
        chamadas = []

        def df(x: float) -> float:
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertEqual(len(chamadas), resultado.iteracoes)
        self.assertGreater(len(chamadas), 1)

    def test_erro_cai_mais_rapido_que_linear(self):
        """Cada erro entre 1e-14 e 1e-2 é menor que o anterior elevado a 1,5."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        erros = [abs(x - math.sqrt(2.0)) for x in resultado.historico]
        pares = [(e, seguinte) for e, seguinte in zip(erros, erros[1:])
                 if e < 1e-2 and seguinte > 1e-14]
        self.assertGreaterEqual(len(pares), 2)
        for e, seguinte in pares:
            with self.subTest(erro=e):
                self.assertLess(seguinte, e ** 1.5)


class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: regras de ponto_operacao que a aceitação não cobre."""

    def test_intervalo_invertido_ou_vazio(self):
        """a >= b levanta ValueError antes de chamar o resolvedor."""
        for a, b in [(50.0, 40.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, tubulacao(), Bisseccao(), a=a, b=b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Intervalo fora do domínio da bomba (0 a 100 L/s) levanta ValueError."""
        for a, b in [(10.0, 120.0), (-5.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, tubulacao(), Bisseccao(), a=a, b=b)

    def test_resolvedor_que_nao_converge(self):
        """Resolvedor que para em max_iter sem convergir levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Newton(tol=1e-12, max_iter=1))

    def test_passa_f_e_o_intervalo_ao_resolvedor(self):
        """O resolvedor recebe a, b e f = bomba(Q) - altura do sistema."""
        tub = tubulacao()
        espiao = ResolvedorEspiao(ResultadoRaiz(50.0, 3, True, (40.0, 50.0)))
        ponto_operacao(BOMBA, tub, espiao, a=20.0, b=80.0)
        f, a, b = espiao.chamada
        self.assertEqual((a, b), (20.0, 80.0))
        self.assertAlmostEqual(f(35.0), BOMBA(35.0) - tub.altura_sistema(35.0))

    def test_devolve_o_resultado_do_resolvedor(self):
        """A vazão é a raiz do resolvedor e `resultado` é o objeto que ele devolveu."""
        resultado = ResultadoRaiz(61.5, 7, True, (40.0, 61.5))
        ponto = ponto_operacao(BOMBA, tubulacao(), ResolvedorEspiao(resultado))
        self.assertIs(ponto.resultado, resultado)
        self.assertAlmostEqual(ponto.vazao, 61.5)
        self.assertAlmostEqual(ponto.altura, BOMBA(61.5))


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: regras de ordem_convergencia que a aceitação não cobre."""

    def test_piso_cresce_com_o_modulo_da_raiz(self):
        """Com raiz 1e6 o piso é 1e-8: erros de 5e-9 e 3e-9 ficam de fora e p = 2."""
        raiz = 1e6
        historico = [raiz + e for e in (1e-1, 1e-2, 1e-4, 5e-9, 3e-9)]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 2.0, delta=0.02)

    def test_piso_escolhido_pelo_chamador(self):
        """Com piso 1e-3, só dois erros passam e p não existe."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.1, 1.01, 1.0001], 1.0, piso=1e-3)

    def test_erros_iguais_levantam_erro(self):
        """Dois erros iguais zerariam o denominador."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.5, 1.5, 1.5], 1.0)

    def test_ordem_do_newton_em_raiz_de_dois(self):
        """No Newton em x² - 2, a ordem estimada fica perto de 2."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        ordem = ordem_convergencia(resultado.historico, resultado.raiz)
        self.assertAlmostEqual(ordem, 2.0, delta=0.2)


if __name__ == "__main__":
    unittest.main()

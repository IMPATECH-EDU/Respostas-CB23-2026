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
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²
RUGOSIDADE_RELATIVA = 0.15e-3 / 0.20


def _tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton precisa recalcular a derivada a cada iteração."""

    def test_colebrook_poucas_iteracoes(self):
        """Colebrook com Re = 1e4 converge em no máximo 6 iterações (o defeito dava 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_ordem_quadratica(self):
        """A ordem de convergência estimada do Newton em x² - 2 é cerca de 2 (o defeito dava 1)."""
        resultado = Newton(tol=1e-13).encontrar(lambda x: x * x - 2.0, 0.0, 4.0)
        self.assertGreater(ordem_convergencia(resultado.historico, resultado.raiz), 1.8)

    def test_derivada_avaliada_a_cada_iteracao(self):
        """Com `df` fornecida, ela é chamada uma vez por iteração (o defeito chamava uma só)."""
        chamadas = []

        def df(x: float) -> float:
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 4.0)
        self.assertGreater(resultado.iteracoes, 1)
        self.assertEqual(len(chamadas), resultado.iteracoes)

    def test_newton_vence_a_bisseccao_em_x2_menos_2(self):
        """Em x² - 2, o Newton usa menos de um quarto das iterações da bissecção."""
        f = lambda x: x * x - 2.0
        newton = Newton(tol=1e-12).encontrar(f, 0.0, 4.0)
        bisseccao = Bisseccao(tol=1e-12).encontrar(f, 0.0, 4.0)
        self.assertLess(newton.iteracoes, bisseccao.iteracoes / 4)


class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: regras do contrato de `ponto_operacao` que a aceitação não verifica."""

    def test_intervalo_invertido(self):
        """Com a >= b, levanta ValueError."""
        for a, b in [(60.0, 40.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=a, b=b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Um intervalo que passa do domínio da bomba (0 a 100 L/s) levanta ValueError."""
        for a, b in [(10.0, 120.0), (-5.0, 90.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=a, b=b)

    def test_resolvedor_que_nao_converge(self):
        """Se o resolvedor para por max_iter sem convergir, levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(tol=1e-12, max_iter=3))

    def test_vazao_e_a_raiz_do_resultado(self):
        """A vazão devolvida é a raiz do `ResultadoRaiz`, e a altura é a da bomba nessa vazão."""
        ponto = ponto_operacao(BOMBA, _tubulacao(), Newton(tol=1e-10))
        self.assertEqual(ponto.vazao, ponto.resultado.raiz)
        self.assertAlmostEqual(ponto.altura, float(BOMBA(ponto.vazao)))


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: regras do contrato de `ordem_convergencia` que a aceitação não verifica."""

    def test_ignora_erros_abaixo_do_piso(self):
        """Erros no nível do arredondamento (abaixo do piso) não entram na estimativa."""
        historico = [1 + 1e-2, 1 + 1e-4, 1 + 1e-8, 1.0, 1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, delta=0.01)

    def test_usa_os_tres_ultimos_erros(self):
        """Só os três últimos erros acima do piso contam, não a média de todo o histórico."""
        historico = [3.0, 2.0, 1.5] + [1 + 0.5 ** k for k in range(1, 12)]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 1.0, delta=0.01)

    def test_piso_acompanha_a_escala_da_raiz(self):
        """O piso é relativo a max(1, |raiz|): em raiz 1e6, um erro de 1e-9 já está no piso."""
        raiz = 1e6
        historico = [raiz + 1.0, raiz + 1e-2, raiz + 1e-4, raiz + 1e-9]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 1.0, delta=0.01)

    def test_piso_deixa_menos_de_tres_erros(self):
        """Se o piso descarta erros e sobram menos de 3, levanta ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1 + 1e-2, 1 + 1e-4, 1.0, 1.0], 1.0)

    def test_erros_iguais(self):
        """Dois erros consecutivos iguais (0/0 na fórmula) levantam ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.5, 1.5, 1.25], 1.0)


if __name__ == "__main__":
    unittest.main()
"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest
from typing import Callable

import numpy as np

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton, ResultadoRaiz
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# ---------------------------------------------------------------------------------------
# Issue #9: testes de regressão do Newton (escritos antes da correção)
# ---------------------------------------------------------------------------------------
class TestNewtonRegressao(unittest.TestCase):
    """Issue #9: o Newton tem que convergir quadraticamente."""

    def test_colebrook_em_re_1e4(self):
        """O caso do relato: em Re = 1e4 o fator de atrito sai em no máximo 6 iterações."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_dois(self):
        """x² - 2 a partir de x0 = 1 converge em no máximo 6 iterações (não em ~30)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_calculada_em_cada_ponto(self):
        """A derivada df é chamada uma vez por iteração, sempre no ponto atual."""
        pontos = []

        def df(x):
            pontos.append(x)
            return 2 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertEqual(pontos, list(resultado.historico[:-1]))


# ---------------------------------------------------------------------------------------
# Issue #8: regras do contrato que os testes de aceitação não verificam
# ---------------------------------------------------------------------------------------
VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")


def tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class ResolvedorDeMentira:
    """Resolvedor que só anota as chamadas e devolve uma resposta pronta (segue o protocolo)."""

    def __init__(self, raiz: float, convergiu: bool = True) -> None:
        self.chamadas = 0
        self._resposta = ResultadoRaiz(raiz, 1, convergiu, (raiz,))

    def encontrar(self, f: Callable[[float], float], a: float, b: float) -> ResultadoRaiz:
        """Conta a chamada e devolve a resposta pronta, sem olhar para `f`."""
        self.chamadas += 1
        return self._resposta


class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: validações de ponto_operacao."""

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """b além do último ponto do ensaio levanta ValueError sem chamar o resolvedor."""
        falso = ResolvedorDeMentira(60.0)
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), falso, a=10.0, b=120.0)
        self.assertEqual(falso.chamadas, 0)

    def test_intervalo_invertido(self):
        """a >= b levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(), a=70.0, b=70.0)

    def test_resolvedor_que_nao_converge(self):
        """Se o resultado vem com convergiu=False, ponto_operacao levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-12, max_iter=5))

    def test_raiz_fora_do_intervalo(self):
        """Uma "raiz" que o resolvedor diz ter achado fora de [a, b] é recusada."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), ResolvedorDeMentira(20.0), a=40.0, b=90.0)

    def test_newton_no_ponto_de_operacao_e_quadratico(self):
        """Com Newton dentro (Colebrook) e fora, a ordem estimada no ponto passa de 1,8."""
        # Com a bissecção dentro, f(Q) carrega um "ruído" de ~1e-12 e o último erro do
        # Newton para nesse nível: a ordem estimada cai para ~0,8 sem o método ter culpa.
        tub = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Newton(tol=1e-12))
        ponto = ponto_operacao(BOMBA, tub, Newton(tol=1e-10))
        self.assertGreater(ordem_convergencia(ponto.resultado.historico, ponto.vazao), 1.8)


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: detalhes de ordem_convergencia."""

    def test_piso_relativo_ao_tamanho_da_raiz(self):
        """Com raiz 1e6 o piso vira 1e-8: o erro de 1e-9 é ignorado e a ordem fica 1."""
        raiz = 1e6
        historico = [raiz + 1e-2, raiz + 1e-3, raiz + 1e-4, raiz + 1e-9]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 1.0, delta=0.01)

    def test_erros_que_nao_diminuem(self):
        """Erros iguais deixam a fórmula sem sentido (divisão por log 1): ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.5, 0.5, 1.5, 1.25], 1.0)


if __name__ == "__main__":
    unittest.main()

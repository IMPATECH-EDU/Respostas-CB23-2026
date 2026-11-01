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
from fornecido.hidraulica import fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Issue #9: regressão do Newton

RUGOSIDADE_RELATIVA = 0.15e-3 / 0.20


class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9 (escritos antes da correção)."""

    def test_poucas_iteracoes_para_a_raiz_de_dois(self):
        """Newton em x² - 2 a partir de 1 converge em poucas iterações (o defeito levava dezenas)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=10)
        self.assertLessEqual(resultado.iteracoes, 8)

    def test_derivada_recalculada_a_cada_iteracao(self):
        """Com df fornecida, ela é chamada uma vez por iteração e não só no ponto inicial."""
        chamadas = []

        def df(x: float) -> float:
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        self.assertEqual(len(chamadas), resultado.iteracoes)
        self.assertGreater(len(set(chamadas)), 1)

    def test_erro_cai_com_o_quadrado_a_cada_passo(self):
        """Em x² - 2, cada erro é no máximo o quadrado do anterior (convergência quadrática)."""
        resultado = Newton(tol=1e-13).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        erros = [abs(x - math.sqrt(2)) for x in resultado.historico]
        for anterior, seguinte in zip(erros, erros[1:]):
            if anterior > 1e-7:
                self.assertLessEqual(seguinte, anterior ** 2)

    def test_colebrook_re_1e4_com_cinco_ou_seis_iteracoes(self):
        """No Colebrook com Re = 1e4 o Newton gasta no máximo 6 iterações (eram 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)


# Issue #8: regras do contrato que os testes de aceitação não verificam

class TestNewtonComOrdem(unittest.TestCase):
    """Newton e ordem_convergencia juntos, no problema de Colebrook."""

    def test_ordem_do_newton_no_colebrook(self):
        """A ordem de convergência medida no Colebrook com Re = 1e5 é próxima de 2."""
        _, resultado = fator_atrito_colebrook(1e5, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertGreater(ordem_convergencia(resultado.historico, resultado.raiz), 1.8)


class _SistemaQuadratico:
    """Sistema simulado: altura exigida 18 + 0,002·Q² (a bomba abaixo é 50 - 0,004·Q²)."""

    def altura_sistema(self, vazao: float) -> float:
        """Altura exigida pelo sistema para a vazão dada."""
        return 18.0 + 0.002 * vazao ** 2


VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")


class TestPontoOperacaoContrato(unittest.TestCase):
    """Regras de `ponto_operacao` que os testes de aceitação não verificam."""

    def test_valor_analitico(self):
        """Com bomba e sistema quadráticos, Q = sqrt(32 / 0,006) e H = 50 - 0,004·Q²."""
        ponto = ponto_operacao(BOMBA, _SistemaQuadratico(), Bisseccao(tol=1e-12))
        q = math.sqrt(32.0 / 0.006)
        self.assertAlmostEqual(ponto.vazao, q, places=6)
        self.assertAlmostEqual(ponto.altura, 50.0 - 0.004 * q ** 2, places=6)

    def test_intervalo_invertido_ou_vazio(self):
        """Com a >= b a função levanta ValueError."""
        for a, b in [(60.0, 40.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _SistemaQuadratico(), Bisseccao(), a=a, b=b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """Um intervalo que sai do domínio da bomba (0 a 100 L/s) levanta ValueError."""
        for a, b in [(-5.0, 90.0), (10.0, 130.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _SistemaQuadratico(), Bisseccao(), a=a, b=b)

    def test_resolvedor_que_nao_convergiu(self):
        """Se o resolvedor para por max_iter sem convergir, levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _SistemaQuadratico(), Bisseccao(tol=1e-12, max_iter=3))

    def test_newton_e_bisseccao_no_mesmo_ponto(self):
        """Com o sistema quadrático, Newton e bissecção dão a mesma vazão."""
        bis = ponto_operacao(BOMBA, _SistemaQuadratico(), Bisseccao(tol=1e-12))
        new = ponto_operacao(BOMBA, _SistemaQuadratico(), Newton(tol=1e-12))
        self.assertAlmostEqual(bis.vazao, new.vazao, places=6)
        self.assertLess(new.resultado.iteracoes, bis.resultado.iteracoes)


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Regras de `ordem_convergencia` que os testes de aceitação não verificam."""

    def test_erros_no_nivel_do_arredondamento_sao_ignorados(self):
        """Erros nulos no fim do histórico (raiz exata) não entram na estimativa."""
        historico = [1 + 1e-1, 1 + 1e-2, 1 + 1e-4, 1 + 1e-8, 1.0, 1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, delta=0.01)

    def test_piso_escolhido_pelo_usuario(self):
        """Com piso 1e-6, o erro de 1e-12 sai da conta e a ordem estimada muda de 4 para 2."""
        historico = [1 + 1e-1, 1 + 1e-2, 1 + 1e-4, 1 + 1e-12]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 4.0, delta=0.05)
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0, piso=1e-6), 2.0, delta=0.05)

    def test_piso_cresce_com_o_tamanho_da_raiz(self):
        """O piso é piso · max(1, |raiz|): para raiz 1000 o erro de 1e-12 já fica abaixo dele."""
        erros = [1e-1, 1e-2, 1e-4, 1e-12]
        raiz = 1000.0
        historico = [raiz + e for e in erros]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 2.0, delta=0.05)

    def test_erros_repetidos_levantam_value_error(self):
        """Se os dois primeiros dos três últimos erros são iguais, a razão é indefinida: ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.25, 1.25, 1.125], 1.0)


if __name__ == "__main__":
    unittest.main()

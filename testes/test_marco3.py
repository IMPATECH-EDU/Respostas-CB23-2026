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


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²


def _tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestNewtonRegressaoIssue9(unittest.TestCase):
    """Issue #9: regressão do Newton lento (derivada calculada uma única vez)."""

    def test_regressao_derivada_recalculada_a_cada_iteracao(self):
        """A derivada fornecida é avaliada uma vez por iteração, e não só no ponto inicial."""
        chamadas = []

        def df(x: float) -> float:
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 1.0, 3.0)
        self.assertTrue(resultado.convergiu)
        self.assertEqual(len(chamadas), resultado.iteracoes)

    def test_regressao_colebrook_re_1e4_converge_quadraticamente(self):
        """Em Colebrook com Re = 1e4 o Newton leva no máximo 7 iterações (o defeito dava 10)."""
        f, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 7)
        self.assertAlmostEqual(f, 0.03202, delta=5e-5)


class TestOperacaoContrato(unittest.TestCase):
    """Issue #8: regras do contrato de `ponto_operacao` e `ordem_convergencia` fora da aceitação."""

    def test_ponto_operacao_rejeita_intervalo_invalido(self):
        """`a >= b` e intervalos que saem do domínio da bomba [0, 100] levantam ValueError."""
        for a, b in [(50.0, 50.0), (60.0, 40.0), (10.0, 120.0), (-5.0, 90.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _tubulacao(), Bisseccao(tol=1e-10), a=a, b=b)

    def test_ponto_operacao_levanta_se_o_resolvedor_nao_convergir(self):
        """Com poucas iterações o resolvedor não converge e `ponto_operacao` levanta ValueError."""
        for resolvedor in (Newton(tol=1e-10, max_iter=1), Bisseccao(tol=1e-10, max_iter=3)):
            with self.subTest(metodo=type(resolvedor).__name__), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _tubulacao(), resolvedor)

    def test_ordem_convergencia_aplica_o_piso_relativo_a_raiz(self):
        """O piso é `piso * max(1, |raiz|)`, e menos de 3 erros acima dele levanta ValueError."""
        # raiz = 10: o limite vale 1e-3 * 10 = 1e-2; o erro 2e-3 fica de fora e p = 1.
        historico = [10.4, 10.2, 10.1, 10.05, 10.002]
        self.assertAlmostEqual(ordem_convergencia(historico, 10.0, piso=1e-3), 1.0, places=6)
        # cinco aproximações, mas só dois erros acima do piso padrão.
        with self.assertRaises(ValueError):
            ordem_convergencia([1.1, 1.01, 1.0, 1.0, 1.0], 1.0)


if __name__ == "__main__":
    unittest.main()

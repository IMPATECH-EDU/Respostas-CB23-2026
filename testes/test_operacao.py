"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import numpy as np

from elevatoria.raizes import Bisseccao, Newton
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from fornecido.hidraulica import fator_atrito_colebrook, Tubulacao
from elevatoria.calibracao import CurvaCalibracao

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")


def _tubulacao() -> Tubulacao:
    """Cria a tubulação padrão da estação."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: testes de regressão para o cálculo da derivada em `Newton`."""

    def test_newton_converge_em_poucas_iteracoes_colebrook(self):
        """Resolve Colebrook para Re=1e4 em no máximo 6 iterações (não 10)."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_newton_ordem_quadratica_em_funcao_nao_linear(self):
        """Apresenta ordem de convergência quadrática (~2) em f(x) = x³ - 2."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x ** 3 - 2.0, 0.0, 4.0)
        self.assertGreater(ordem_convergencia(resultado.historico, resultado.raiz), 1.8)


class TestContratoOperacao(unittest.TestCase):
    """Issue #8: regras de contrato de `ponto_operacao` e `ordem_convergencia`."""

    def test_ponto_operacao_rejeita_intervalo_invalido(self):
        """Levanta ValueError se a >= b ou se a < 0."""
        for a, b in [(50.0, 50.0), (60.0, 40.0), (-5.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=a, b=b)

    def test_ponto_operacao_rejeita_fora_do_dominio_da_bomba(self):
        """Levanta ValueError se [a, b] ultrapassar o domínio da curva da bomba."""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, _tubulacao(), Bisseccao(), a=10.0, b=150.0)

    def test_ordem_convergencia_rejeita_erros_nulos_ou_nao_decrescentes(self):
        """Levanta ValueError quando os últimos erros são nulos ou não decrescem."""
        with self.assertRaises(ValueError):
            ordem_convergencia([2.0, 1.0, 1.0, 1.0], 1.0)
        with self.assertRaises(ValueError):
            ordem_convergencia([1.1, 1.2, 1.3, 1.4], 1.0)

# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

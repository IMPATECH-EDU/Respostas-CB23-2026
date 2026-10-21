"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

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
class TestRegressaoIssue9(unittest.TestCase):
    """Testes de regressão da convergência lenta do método de Newton."""

    def test_newton_colebrook_reduz_iteracoes(self):
        """Newton recalculando a derivada resolve Colebrook em menos de oito iterações."""
        _, resultado = fator_atrito_colebrook(
            1e4, 0.15e-3 / 0.20, Newton(tol=1e-12)
        )
        self.assertTrue(resultado.convergiu)
        self.assertLess(resultado.iteracoes, 8)

    def test_newton_colebrook_tem_convergencia_quadratica(self):
        """A ordem de convergência do Newton para Colebrook deve ser próxima de dois."""
        _, resultado = fator_atrito_colebrook(
            1e4, 0.15e-3 / 0.20, Newton(tol=1e-12)
        )
        ordem = ordem_convergencia(resultado.historico, resultado.raiz)
        self.assertGreater(ordem, 1.8)


class TestContratosOperacao(unittest.TestCase):
    """Testes adicionais dos contratos das funções de operação."""

    def test_ponto_operacao_rejeita_intervalo_fora_do_dominio(self):
        """Ponto de operação rejeita intervalo que extrapola a curva da bomba."""
        bomba = CurvaCalibracao([0.0, 50.0, 100.0], [50.0, 40.0, 10.0], "linear")
        tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao())
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tubulacao, Bisseccao(), a=-1.0, b=50.0)

    def test_ordem_convergencia_ignora_erros_abaixo_do_piso(self):
        """Ordem usa os últimos três erros acima do piso relativo à raiz."""
        historico = [1001.0, 1000.1, 1000.001, 1000.0 + 1e-12, 1000.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1000.0), 2.0, delta=0.01)


if __name__ == "__main__":
    unittest.main()

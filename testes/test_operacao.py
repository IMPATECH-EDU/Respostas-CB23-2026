"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import math

from elevatoria.raizes import Bisseccao, Newton
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestNewton(unittest.TestCase):
    """Testes de regressão da velocidade de convergência do Newton (issue #9)."""

    def test_raiz_quadrada_com_derivada_exata(self) -> None:
        """Newton encontra a raiz de x² - 2 em até seis iterações com derivada exata."""
        metodo = Newton(tol=1e-12, max_iter=6, df=lambda x: 2 * x)
        resultado = metodo.encontrar(lambda x: x * x - 2, 0.0, 2.0)

        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=10)

    def test_colebrook_com_derivada_numerica(self) -> None:
        """Colebrook para Re = 10000 converge em até seis iterações de Newton."""
        metodo = Newton(tol=1e-12, max_iter=6)
        fator, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, metodo)

        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(fator, 0.03202, delta=5e-5)


class TestPontoOperacao(unittest.TestCase):
    """Verifica as validações do cálculo do ponto de operação."""

    def setUp(self) -> None:
        """Prepara uma curva de bomba e uma tubulação para os testes."""
        self.bomba = CurvaCalibracao([0, 50, 100], [50, 40, 10], "spline")
        self.tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao())

    def test_intervalo_invertido_ou_vazio(self) -> None:
        """O limite inicial deve ser menor que o final."""
        for a, b in [(90.0, 10.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaisesRegex(ValueError, "a < b"):
                ponto_operacao(self.bomba, self.tubulacao, Bisseccao(), a, b)

    def test_intervalo_fora_do_dominio(self) -> None:
        """Os dois limites do intervalo devem pertencer ao domínio da bomba."""
        for a, b in [(-1.0, 90.0), (10.0, 101.0)]:
            with self.subTest(a=a, b=b), self.assertRaisesRegex(ValueError, "domínio"):
                ponto_operacao(self.bomba, self.tubulacao, Bisseccao(), a, b)

    def test_resolvedor_nao_convergiu(self) -> None:
        """Um resolvedor que atinge max_iter sem convergir provoca ValueError."""
        metodo = Bisseccao(tol=1e-12, max_iter=1)
        with self.assertRaisesRegex(ValueError, "não convergiu"):
            ponto_operacao(self.bomba, self.tubulacao, metodo)


class TestOrdemConvergencia(unittest.TestCase):
    """Verifica o piso relativo e a seleção dos últimos erros úteis."""

    def test_piso_proporcional_a_raiz(self) -> None:
        """Erros pequenos em relação à raiz são ignorados mesmo acima do piso absoluto."""
        historico = [1016.0, 1004.0, 1000.25, 1000.01, 1000.0]
        ordem = ordem_convergencia(historico, 1000.0, piso=1e-4)

        self.assertAlmostEqual(ordem, 2.0)

    def test_ignora_erros_pequenos_no_meio(self) -> None:
        """O histórico mantém a ordem dos erros úteis ao remover valores abaixo do piso."""
        historico = [0.5, 0.25, 1e-16, 0.125, 0.0]
        ordem = ordem_convergencia(historico, 0.0)

        self.assertAlmostEqual(ordem, 1.0)


if __name__ == "__main__":
    unittest.main()

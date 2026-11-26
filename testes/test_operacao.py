"""Testes próprios do Marco 3: regressão do Newton e contratos da operação."""
import math
import unittest

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import Tubulacao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo de uso da bissecção fornecido no esqueleto."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: a derivada numérica precisa ser recalculada a cada iteração."""

    def test_raiz_quadrada_de_dois_converge_em_poucas_iteracoes(self):
        """Newton com derivada recalculada converge quadraticamente para sqrt(2)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x*x - 2.0, 0.5, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=11)
        self.assertLess(resultado.iteracoes, 8)

    def test_derivada_numerica_e_reavaliada_no_ponto_atual(self):
        """A derivada fornecida deve ser chamada em cada aproximação, não apenas no início."""
        pontos = []
        def derivada(x):
            pontos.append(x)
            return 2.0*x
        resultado = Newton(tol=1e-12, df=derivada).encontrar(lambda x: x*x - 2.0, 0.5, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertEqual(len(pontos), resultado.iteracoes)
        self.assertGreater(len(set(pontos)), 1)

    def test_colebrook_re_1e4_converge_rapidamente(self):
        """O Newton resolve Colebrook para Re=1e4 em menos iterações que o código defeituoso."""
        from fornecido.hidraulica import fator_atrito_colebrook
        fator, resultado = fator_atrito_colebrook(1e4, 0.15e-3/0.20, Newton(tol=1e-12))
        self.assertAlmostEqual(fator, 0.03202, delta=5e-5)
        self.assertLessEqual(resultado.iteracoes, 6)


class TestContratoOperacao(unittest.TestCase):
    """Casos de contrato adicionais para as funções da issue #8."""

    @classmethod
    def setUpClass(cls):
        cls.bomba = CurvaCalibracao([0, 25, 50, 75, 100], [60, 55, 45, 30, 10], "spline")
        cls.tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Newton(tol=1e-12))

    def test_intervalo_invertido_e_rejeitado(self):
        """O contrato exige a < b."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(), 80, 20)

    def test_intervalo_fora_do_dominio_e_rejeitado(self):
        """O intervalo de busca não pode extrapolar o domínio da curva da bomba."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(), 10, 110)

    def test_ordem_convergencia_ignora_erros_abaixo_do_piso(self):
        """Erros menores que o piso relativo são ignorados ao selecionar os três últimos."""
        raiz = 1e6
        historico = [raiz + 0.5, raiz + 0.25, raiz + 0.125, raiz + 1e-9]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 1.0, places=10)

    def test_ordem_convergencia_exige_tres_erros_validos(self):
        """Menos de três erros acima do piso deve produzir ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.0, 1.0 + 1e-16, 1.0], 1.0)


if __name__ == "__main__":
    unittest.main()

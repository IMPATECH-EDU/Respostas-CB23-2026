"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoNewton(unittest.TestCase):
    """Testes de regressão da issue #9 ANTES da correção."""

    def test_newton_iteracoes_colebrook_re_1e4(self):
        """Para Re = 10^4 em Colebrook, Newton deve convergir em no máximo 6 iterações."""
        from fornecido.hidraulica import fator_atrito_colebrook
        from elevatoria.raizes import Newton
        _, res = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertLessEqual(res.iteracoes, 6)

    def test_newton_convergencia_quadratica_polinomio(self):
        """Para f(x) = x^2 - 2, Newton deve convergir quadraticamente em no máximo 6 iterações."""
        from elevatoria.raizes import Newton
        res = Newton(tol=1e-12).encontrar(lambda x: x ** 2 - 2.0, 0.0, 2.0)
        self.assertLessEqual(res.iteracoes, 6)


class TestOperacaoContrato(unittest.TestCase):
    """Testes de regras do contrato de ponto_operacao e ordem_convergencia."""

    def setUp(self):
        import numpy as np
        from elevatoria.calibracao import CurvaCalibracao
        from elevatoria.raizes import Bisseccao
        from fornecido.hidraulica import Tubulacao
        vazoes = np.arange(0.0, 101.0, 10.0)
        self.bomba = CurvaCalibracao(vazoes, 50.0 - 0.004 * vazoes ** 2, "spline")
        self.tub = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

    def test_intervalo_invalido_a_maior_igual_b(self):
        """ponto_operacao com a >= b deve levantar ValueError."""
        from elevatoria.operacao import ponto_operacao
        from elevatoria.raizes import Bisseccao
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tub, Bisseccao(tol=1e-10), a=50.0, b=50.0)

    def test_intervalo_fora_do_dominio(self):
        """ponto_operacao com [a, b] fora do domínio da bomba levanta ValueError."""
        from elevatoria.operacao import ponto_operacao
        from elevatoria.raizes import Bisseccao
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tub, Bisseccao(tol=1e-10), a=-5.0, b=50.0)
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tub, Bisseccao(tol=1e-10), a=10.0, b=120.0)

    def test_nao_convergencia_levanta_erro(self):
        """Se o resolvedor não convergir (atingir max_iter), levanta ValueError."""
        from elevatoria.operacao import ponto_operacao
        from elevatoria.raizes import Bisseccao
        # Com max_iter=1 a bissecção não atinge tol=1e-12
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tub, Bisseccao(tol=1e-12, max_iter=1), a=10.0, b=100.0)

    def test_ordem_convergencia_poucos_erros_com_piso(self):
        """ordem_convergencia com menos de 3 erros acima do piso levanta ValueError."""
        from elevatoria.operacao import ordem_convergencia
        with self.assertRaises(ValueError):
            ordem_convergencia([1.0001, 1.00001, 1.0], 1.0, piso=1e-3)


if __name__ == "__main__":
    unittest.main()

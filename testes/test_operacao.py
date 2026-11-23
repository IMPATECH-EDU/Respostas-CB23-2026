"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from elevatoria.calibracao import CurvaCalibracao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton calculava a derivada uma vez só e convergia linearmente."""

    @staticmethod
    def f(x: float) -> float:
        """x² - 2, cuja raiz positiva é √2."""
        return x * x - 2.0

    def test_raiz_de_dois_em_no_maximo_seis_iteracoes(self):
        """Partindo de 1,5, o Newton chega a √2 com tol 1e-12 em no máximo 6 iterações."""
        resultado = Newton(tol=1e-12).encontrar(self.f, 0.0, 3.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_digitos_corretos_dobram_a_cada_iteracao(self):
        """Com 2 iterações a partir de 1,5, o erro já é menor que 1e-5 (convergência quadrática)."""
        historico = Newton(tol=1e-12).encontrar(self.f, 0.0, 3.0).historico
        self.assertLess(abs(historico[2] - math.sqrt(2.0)), 1e-5)


class TestContratoOperacao(unittest.TestCase):
    """Regras das docstrings da issue #8 que os testes de aceitação não verificam."""

    BOMBA = CurvaCalibracao([0.0, 50.0, 100.0], [50.0, 40.0, 20.0], "linear")

    def test_intervalo_invertido_levanta_value_error(self):
        """a >= b levanta ValueError antes de chamar o resolvedor."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.BOMBA, None, Bisseccao(), a=80.0, b=20.0)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """[a, b] que sai do domínio da bomba ([0, 100]) levanta ValueError."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.BOMBA, None, Bisseccao(), a=10.0, b=150.0)

    def test_ordem_ignora_erros_abaixo_do_piso(self):
        """Erros no nível do arredondamento (0 e 1e-16) são ignorados: a ordem continua 2."""
        historico = [1 + 1e-1, 1 + 1e-2, 1 + 1e-4, 1 + 1e-8, 1 + 1e-16, 1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, places=6)


if __name__ == "__main__":
    unittest.main()

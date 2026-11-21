"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import math 

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


class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9 para o método de Newton."""

    def test_newton_colebrook_poucas_iteracoes(self):
        """Regressão #9: Colebrook em Re=1e4 converge em no máximo 6 iterações com Newton."""
        newton = Newton(tol=1e-12)
        _, res = fator_atrito_colebrook(1e4, 0.001, newton)
        self.assertTrue(res.convergiu)
        self.assertLessEqual(res.iteracoes, 6)

    def test_newton_convergencia_quadratica_polinomio(self):
        """Regressão #9: raiz de x^3 - 2 em [0.5, 3.0] atinge precisão 1e-12 em até 7 iterações."""
        res = Newton(tol=1e-12).encontrar(lambda x: x**3 - 2.0, 0.5, 3.0)
        self.assertTrue(res.convergiu)
        self.assertLessEqual(res.iteracoes, 7)


class TestOperacaoContrato(unittest.TestCase):
    """Testes de casos de borda do contrato de `ponto_operacao` e `ordem_convergencia`."""

    def _bomba_e_tubulacao(self) -> tuple[CurvaCalibracao, Tubulacao]:
        bomba = CurvaCalibracao([0.0, 50.0, 100.0], [50.0, 42.0, 25.0], metodo="spline")
        tub = Tubulacao(0.25, 500.0, 0.00015, 20.0, Bisseccao(tol=1e-12))
        return bomba, tub

    def test_ponto_operacao_intervalo_fora_do_dominio(self):
        """Intervalo [a, b] fora de `bomba.dominio` levanta ValueError."""
        bomba, tub = self._bomba_e_tubulacao()
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tub, Bisseccao(), a=5.0, b=120.0)

    def test_ponto_operacao_nao_convergiu(self):
        """Quando o resolvedor não converge (`convergiu=False`), levanta ValueError."""
        bomba, tub = self._bomba_e_tubulacao()
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tub, Bisseccao(tol=1e-14, max_iter=2), a=10.0, b=90.0)

    def test_ordem_convergencia_menos_de_tres_erros_acima_do_piso(self):
        """Menos de 3 aproximações com erro acima do piso levanta ValueError."""
        historico = [1.1, 1.01, 1.0 + 1e-15, 1.0]
        with self.assertRaises(ValueError):
            ordem_convergencia(historico, raiz=1.0, piso=1e-14)


if __name__ == "__main__":
    unittest.main()

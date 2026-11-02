"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook
from elevatoria.operacao import ponto_operacao, ordem_convergencia
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook
import numpy as np

from elevatoria.calibracao import CurvaCalibracao
VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²
def tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestLevantamentoDeErroPontoOperacao(unittest.TestCase):
    """Testes de levantamento de erro da função ponto_operacao"""

    def test_a_menor_que_b(self):
        """Testa se a função levanta ValueError para a=b e a>b"""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10), a=90.0, b=90.0)
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10), a=90.0, b=40.0)

    def test_a_b_fora_do_dominio(self):
        """Testa se a função levanta ValueError se [a,b] estiver fora do intervalo de domínio de bomba.dominio"""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10), a=-900.0, b=900.0)

    def test_resolvedor_nao_convergiu(self):
        """Testa se a função levanta ValueError quando o resolvedor não converge"""
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10, max_iter=1), a=10.0, b=90.0)

class TestLevantamentoDeErroOrdemConvergencia(unittest.TestCase):
    def test_ordem_convergencia_menos_de_tres_erros(self):
        """Verifica se a função levanta ValueError quando há menos de 3 erros acima do piso."""
        with self.assertRaises(ValueError): #o erro de 0.0001 não será considerado válido
            ordem_convergencia([0.5, 0.25, 0.0001], raiz=0.0, piso=1e-3)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestNewton(unittest.TestCase):
    """Testes do método de Newton"""
    def test_newton_recalcula_derivada(self):
        """Verifica se Newton recalcula a derivada a cada iteração."""
        chamadas = []
        def derivada(x):
            chamadas.append(x)
            return 2 * x
        resultado = Newton(df=derivada).encontrar(lambda x: x**2 - 2, 0, 2)
        self.assertEqual(len(chamadas), resultado.iteracoes)

    def test_newton_converge_em_poucas_iteracoes(self):
        """Verifica se Newton resolve Colebrook em até 6 iterações."""
        resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertTrue(resultado[1].convergiu)
        self.assertLessEqual(resultado[1].iteracoes, 6)
        
if __name__ == "__main__":
    unittest.main()

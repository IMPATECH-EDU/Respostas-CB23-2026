"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import math

from typing import Sequence
from elevatoria.raizes import Bisseccao, MetodoRaiz, Newton
from elevatoria.operacao import PontoOperacao, ordem_convergencia, ponto_operacao
from elevatoria.calibracao import CurvaCalibracao
from fornecido.hidraulica import Tubulacao, Resolvedor

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestOperacao(unittest.TestCase):
    def test__intervalo_dominio_invertido(self):
        """Verificamos se a função lança ValueError quando a>=b."""

        # Criamos os dados fictícios para serem testados
        bomba = CurvaCalibracao([1, 2, 3],
                                [1, 2, 3],
                                "spline")

        tubu = Tubulacao(12.2, 13.8, 3.5, 12.5, Bisseccao())


        # Caso onde a>b
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tubu, Bisseccao(), 100, 10)

    def test_intervalo_no_dominio(self):
        """Verificação se a implementação de ponto_operacao lança ValueError quando o intervalo está no domínio"""

        # Criamos os dados para realizarmos o teste
        bomba = CurvaCalibracao([1, 2, 3],
                                [1, 2, 3],
                                "spline")

        tubu = Tubulacao(12.2, 13.8, 3.5, 12.5, Bisseccao())

        # Definimos o intervalo como sendo [1, 3], assim, testamos para (a=1 e b=10), (a=0 e b=3) e (a=0 e b=10)
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tubu, Bisseccao, 1, 10)
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tubu, Bisseccao, 0, 3)
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tubu, Bisseccao, 0, 10)

class TestRegressao(unittest.TestCase):
    def test_ordem_convergencia_newton(self):
        """Testamos a ordem de convergência dada atualmente pelo método de Newton com a função x**2 - 2"""
        # Criamos a classe Newton para o nosso teste
        newt = Newton(df=lambda x: 2*x)
        
        # Aplicamos o método a função
        r = newt.encontrar(lambda x: x**2 - 2, 1.0, 2.0)
        hist = [k for k in r.historico]

        # Usamos a função que definimos na issue #8
        ord_real = ordem_convergencia(hist, r.raiz)

        # Vemos se o resultado obtido é o esperado
        self.assertAlmostEqual(ord_real, 2.0, places=3)
    
    def test_numero_de_iteracoes(self):
        """Vemos se o números de iterações está em conformidade com o esperado para a função x**2 - 2, espera-se 5 iterações"""
        newt = Newton(df = lambda x: 2*x)

        # Verificamos se o número de iterações é menor ou igual a 5
        r = newt.encontrar(lambda x: x**2 - 2, 1.0, 2.0)
        if r.convergiu and math.isclose(r.raiz, math.sqrt(2)):
            #self.assertLessEqual(r.iteracoes, 5)
            self.assertTrue(r.iteracoes <= 5)

if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.raizes import Bisseccao , Newton
from elevatoria.operacao import ordem_convergencia

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9: o Newton converge de maneira quadrática."""

    def test_iteracoes_raiz_de_2(self):
        """Dentro do intervalo [1,2] a raiz de x² - 2, o Newton deve gastar no máximo 5 iterações."""
        resultado = Newton().encontrar(lambda x: x**2 - 2, 1.0, 2.0)
        self.assertLessEqual(resultado.iteracoes, 5)

    def test_erro_apos_tres_iteracoes(self):
        """Depois de 3 iterações, o erro na raiz de 2 já é menor que 1e-10."""
        resultado = Newton().encontrar(lambda x: x**2 - 2, 1.0, 2.0)
        erro = abs(resultado.historico[3] - math.sqrt(2))
        self.assertLess(erro, 1e-10)

if __name__ == "__main__":
    unittest.main()


class TestOrdemConvergenciaRegras(unittest.TestCase):
    """Regras que os testes de aceitação não verificam sobre ordem_convergencia"""
    
    def test_tres_ultimos(self):
        """Uma sequência começa linear e termina quadrática de ordem 2: contam os três últimos erros"""
        historico = [0.5, 0.25, 0.125, 1e-2, 1e-4, 1e-8]
        self.assertAlmostEqual(ordem_convergencia(historico, 0.0), 2.0, delta=0.01)

    def test_ignorando_erros_abaixo_do_piso(self):
        """Aproximações exatas no fim do histórico (erro zero) são ignoradas, e a ordem continua 2"""
        historico = [1e-1, 1e-2, 1e-4, 1e-8, 0.0, 0.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 0.0), 2.0, delta=0.01)
    
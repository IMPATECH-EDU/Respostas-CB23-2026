"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import numpy as np

from elevatoria.integracao import Simpson, Trapezio
from elevatoria.dia import ajustar_polinomio, dia_de_operacao


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestIntegracaoTrapezio(unittest.TestCase):
    def test_exato_para_afim_com_tabela_irregular(self):
        """Método do trapézio calcula a área de função afim com erro 0"""
        valores_x = [1,4,6,8,9]
        valores_y = [2*x for x in valores_x]
        #A função é f(x) = 2x, a área correta é: ∫2x dx = x² -> área = 9² - 1² = 81 -1 = 80
        integrador = Trapezio()
        #Usa assertAlmostEqual pra evitar erros de ponto flutuante
        self.assertAlmostEqual(integrador.integrar_tabela(x=valores_x,y=valores_y), 80)
    
    def test_exato_para_constante_com_tabela_irregular(self):
        """Método do trapézio calcula a área de função constante com erro 0"""
        valores_x = [0,1,6,10]
        valores_y = [1,1,1,1]
        #A função é f(x)=1, a área correta é (10-0)*1 = 10
        integrador = Trapezio()
        #Usa assertAlmostEqual pra evitar erros de ponto flutuante
        self.assertAlmostEqual(integrador.integrar_tabela(x=valores_x,y=valores_y), 10)

class TestLevantamentoDeErroAjustarPolinomio(unittest.TestCase):
    def test_x_y_tamanhos_diferentes(self):
        """ajustar_polinomio levanta erro para len(x)!=len(y)"""
        with self.assertRaises(ValueError):
            ajustar_polinomio([1,2,3,4],[4],2)            

class TestLevantamentoDeErroDiaDeOperacao(unittest.TestCase):
    def test_faixas_faltando(self):
        """dia_de_operacao levanta erro para algum elemento de (0, 18, 21, 24) faltando em t"""
        t = np.asarray([0,4,18,19,21])
        with self.assertRaises(ValueError):
            dia_de_operacao(t,[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],Trapezio())

if __name__ == "__main__":
    unittest.main()

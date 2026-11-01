"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest, numpy

from elevatoria.integracao import Simpson, Trapezio
from elevatoria.dia import ajustar_polinomio




class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)

    def teste_para_trapezio_com_malha_nao_uniforme(self):
        x = [0.0, 0.1, 0.2, 0.4, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9, 1]
        y = x

        resultado = 1*1/2

        self.assertAlmostEqual(resultado, Trapezio().integrar_tabela(x,y))

    def teste_intervalos_em_não_uniforme(self):
        x = [0.0, 1.0, 3]
        y = [1.0,1.0,1.0]

        resultado_esperado = 3

        ultimo_intervalo = 3 - 1 

        self.assertAlmostEqual(ultimo_intervalo, Trapezio().integrar_tabela(x,y) - 1)

    def teste_grau_negativo(self):
        x = [1,2,3]
        y = [4,5,6]
        grau = -1

        with self.assertRaises(ValueError):
            ajustar_polinomio(x,y,grau)

    def teste_listas_tamanhos_distintos(self):
        x= [1,2,3,4]
        y=[5,6,7]
        grau = 2

        with self.assertRaises(ValueError):
            ajustar_polinomio(x,y,grau)



    


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

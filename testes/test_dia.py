"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import numpy as np
from elevatoria.integracao import Simpson, Trapezio
from elevatoria.dia import ajustar_polinomio



class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


"""O defeito do código atual é que ele calcula a largura usando apenas os dois primeiros pontos e 
reaproveita essa largura para todos os trapézios. 
Isso funciona quando os intervalos são uniformes, mas pode gerar resultados incorretos quando os espaçamentos variam."""

class TestRegressaoTrapezio(unittest.TestCase):

    def test_malha_irregular(self):
        """Verifica se a integração calcula corretamente uma tabela com espaçamento irregular."""
        x = np.array([0.0, 1.0, 3.0])
        y = np.array([0.0, 2.0, 2.0])

        resultado = Trapezio().integrar_tabela(x, y)

        self.assertAlmostEqual(resultado, 5.0)

    def test_malha_irregular_com_valores_diferentes(self):
        """Verifica a integração em uma malha irregular com diferentes valores de y."""
        x = np.array([0.0, 2.0, 5.0])
        y = np.array([1.0, 3.0, 4.0])

        resultado = Trapezio().integrar_tabela(x, y)

        self.assertAlmostEqual(resultado, 14.5)

class TestAjustarPolinomio(unittest.TestCase):
    def test_def_correto(self):
        """Testamos se a implementação da função está correta com um caso simples"""
        
        # Fazemos um teste para um caso com o grau 1, polinômio de grau 1
        x__1=np.array([0, 1, 2, 3])
        y__1=np.array([2, 5, 8, 11])
        grau_1=1

        resul_esper=[2.0, 3.0]
        resul_obti=ajustar_polinomio(x__1, y__1, grau_1)

        np.testing.assert_allclose(resul_obti, resul_esper)

if __name__ == "__main__":
    unittest.main()

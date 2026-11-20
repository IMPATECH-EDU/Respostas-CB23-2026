"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from elevatoria.integracao import Trapezio
from elevatoria.integracao import Simpson
import numpy as np
from elevatoria.dia import ajustar_polinomio, dia_de_operacao


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestTrapezioMalhaIrregular(unittest.TestCase):
    """Testes de regressão da issue #11: integração por trapézio em malha irregular."""
    
    def test_malha_irregular_linha_reta(self):
        """Integra f(x) = 2x em malha não uniforme e verifica se a área é exata."""
        x = np.array([0.0, 1.0, 3.0, 4.0])  # dx = [1, 2, 1]
        y = 2.0 * x                         # f(x) = 2x, integral em [0, 4] = 16.0
        area = Trapezio().integrar_tabela(x, y)
        self.assertAlmostEqual(area, 16.0)

    def test_comparacao_malha_uniforme_vs_irregular(self):
        """Verifica se a remoção de pontos altera o resultado proporcionalmente aos intervalos reais."""
        x = np.array([0.0, 0.25, 0.75, 1.0]) # falha no instante 0.5
        y = np.array([10.0, 10.0, 10.0, 10.0])
        area = Trapezio().integrar_tabela(x, y)
        self.assertAlmostEqual(area, 10.0)


class TestCurvasBombaEBalanco(unittest.TestCase):
    """Verifica o levantamento de erros em casos anormais do modulo dia."""
    def test_grau_negativo(self):
        """Verifica se o uso de um grau negativo como parâmetro levantará erro."""
        with self.assertRaises(ValueError):
            x = np.array([8.0, 9.0, 10.0])
            y = np.array([11.0, 12.0, 13.0])
            funcao = ajustar_polinomio(x, y, -1)

    def test_limite_faixa_ausente(self):
        '''Verifica se, caso algum limite de faixa não estiver presente em t, levantará erro.'''
        with self.assertRaises(ValueError):
            t = np.array([0.0, 18.0, 21.0])
            dia_de_operacao(t, t, t, t, Trapezio())


if __name__ == "__main__":
    unittest.main()

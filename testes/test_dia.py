"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestTrapezioRegressao(unittest.TestCase):
    """Testes de regressão da issue #11: o trapézio com pontos na malha não uniforme."""

    def test_constante_malha_irregular(self):
        """A integral de 1 em [0, 3], com pontos 0, 1 e 3, dá 3."""
        resultado = Trapezio().integrar_tabela([0.0, 1.0, 3.0], [1.0, 1.0, 1.0])
        self.assertAlmostEqual(resultado, 3.0)

    def test_linear_malha_irregular(self):
        """O trapézio é exato para retas: a integral de x em [0, 3], com pontos 0, 2 e 3, dá 4,5."""
        resultado = Trapezio().integrar_tabela([0.0, 2.0, 3.0], [0.0, 2.0, 3.0])
        self.assertAlmostEqual(resultado, 4.5)

class TestDiaRegras(unittest.TestCase):
    """Regras de ajustar_polinomio e dia_de_operacao que os testes de aceitação não verificam."""

    def test_grau_negativo(self):
        """ajustar_polinomio com grau negativo levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_falta_limite_de_faixa(self):
        """Sem o instante 18 h no registro, dia_de_operacao levanta ValueError."""
        t = np.linspace(0.0, 24.0, 97)
        t = t[t != 18.0]
        vazao = np.full(t.size, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, vazao, [40.0], [0.8], Trapezio())

if __name__ == "__main__":
    unittest.main()

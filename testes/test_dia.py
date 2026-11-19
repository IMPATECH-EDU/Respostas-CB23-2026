"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: Trapezio.integrar_tabela deve aceitar malha não uniforme."""

    def test_reta_em_malha_irregular(self):
        """∫ x dx de 0 a 3 com pontos 0, 1 e 3 dá 4,5 (o trapézio é exato para retas)."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x), 4.5)

    def test_constante_da_o_comprimento_do_intervalo(self):
        """Integrar a constante 1 numa malha irregular dá o comprimento do intervalo."""
        x = np.array([0.0, 0.25, 0.75, 1.0, 2.0, 2.5])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.ones_like(x)), 2.5)

    def test_reta_na_malha_do_registro_com_falhas(self):
        """Na malha real do dia (com leituras perdidas), ∫ (2t + 1) dt de 0 a 24 dá 600."""
        t, _ = vazao_registrada(3507)
        self.assertGreater(np.ptp(np.diff(t)), 0.0)   # a malha é mesmo irregular
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, 2 * t + 1), 600.0)


if __name__ == "__main__":
    unittest.main()

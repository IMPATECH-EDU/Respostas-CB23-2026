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


class TestTrapezioTabelaRegressao(unittest.TestCase):
    """Issue #11: integrar_tabela do trapézio em malha não uniforme."""

    def test_reta_em_malha_irregular_e_exata(self):
        """O trapézio integra uma reta exatamente, qualquer que seja o espaçamento."""
        x = np.array([0.0, 0.25, 0.5, 1.0, 1.25, 2.0])   # passos 0,25 e 0,5 e 0,75
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 8.0)

    def test_constante_da_comprimento_total(self):
        """y = 1 integra para x[-1] - x[0], mesmo com o primeiro passo diferente dos outros."""
        x = np.array([0.0, 1.0, 1.5, 2.0, 2.5])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.ones_like(x)), 2.5)

    def test_registro_com_falhas_igual_ao_np_trapezoid(self):
        """No registro real do dia (89 de 97 leituras), o resultado coincide com np.trapezoid."""
        t, q = vazao_registrada(123456)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, q), float(np.trapezoid(q, t)))


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan não compensava o arredondamento."""

    def test_um_milhao_de_decimos(self):
        """1 000 000 parcelas de 0,1 somam 100 000 com erro menor que 1e-9 (o ingênuo erra 1,3e-6)."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 1_000_000)
        self.assertLess(abs(acumulador.total - 100_000.0), 1e-9)

    def test_parcelas_menores_que_o_ulp(self):
        """Dez parcelas de 1e-16 somadas a 1,0 não se perdem: o total é 1 + 1e-15."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertGreater(acumulador.total, 1.0)
        self.assertTrue(math.isclose(acumulador.total, 1.0 + 1e-15, rel_tol=0, abs_tol=2.3e-16))

    def test_melhor_que_o_ingenuo(self):
        """Com parcelas de 0,1, o erro do Kahan é pelo menos 1000 vezes menor que o do ingênuo."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        for acumulador in (kahan, ingenuo):
            acumulador.adicionar_todos([0.1] * 100_000)
        self.assertLess(abs(kahan.total - 10_000.0), abs(ingenuo.total - 10_000.0) / 1000)


if __name__ == "__main__":
    unittest.main()

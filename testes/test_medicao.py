"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest
from decimal import Decimal

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o Kahan não compensava o arredondamento."""

    def test_um_milhao_de_parcelas_de_um_decimo(self):
        """1 milhão de parcelas de 0,1 somam 100000 com erro abaixo de 1e-9 (antes: 1,3e-6)."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)
        self.assertLess(abs(Decimal(acumulador.total) - Decimal(100_000)), Decimal("1e-9"))

    def test_kahan_bem_melhor_que_o_ingenuo(self):
        """O erro do Kahan é pelo menos 1000 vezes menor que o do ingênuo."""
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        for _ in range(200_000):
            ingenuo.adicionar(0.1)
            kahan.adicionar(0.1)
        exato = Decimal(20_000)
        erro_ingenuo = abs(Decimal(ingenuo.total) - exato)
        erro_kahan = abs(Decimal(kahan.total) - exato)
        self.assertGreater(erro_ingenuo, 0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)

    def test_parcelas_menores_que_meio_ulp_nao_se_perdem(self):
        """Dez parcelas de 1e-16 somadas a 1,0 não somem: o total chega perto de 1 + 1e-15."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar(1.0)
        for _ in range(10):
            acumulador.adicionar(1e-16)
        self.assertGreater(acumulador.total, 1.0)
        self.assertAlmostEqual(acumulador.total, 1.0 + 1e-15, delta=3e-16)

    def test_bate_com_fsum(self):
        """Com parcelas de ordens de grandeza diferentes, fica a 1e-12 de math.fsum."""
        parcelas = [10.0 ** (k % 7 - 3) * (1 + 0.01 * k) for k in range(5000)]
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos(parcelas)
        self.assertLess(abs(acumulador.total - math.fsum(parcelas)), 1e-12)


if __name__ == "__main__":
    unittest.main()

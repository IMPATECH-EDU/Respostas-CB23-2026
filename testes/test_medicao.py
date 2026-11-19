"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import sys
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan deve compensar o erro de arredondamento."""

    def test_milhao_de_pulsos_de_0_1(self):
        """Um milhão de parcelas de 0,1 somam 100000 com erro desprezível (caso do relato)."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos(0.1 for _ in range(1_000_000))
        self.assertAlmostEqual(kahan.total, 100_000.0, delta=1e-9)

    def test_parcelas_pequenas_nao_somem(self):
        """Dez parcelas de 1e-16 somadas a 1,0 não se perdem, como na soma ingênua."""
        parcelas = [1.0] + [1e-16] * 10
        kahan = AcumuladorKahan()
        kahan.adicionar_todos(parcelas)
        # math.fsum é a soma corretamente arredondada; Kahan deve ficar a 1 ulp dela.
        self.assertAlmostEqual(kahan.total, math.fsum(parcelas), delta=sys.float_info.epsilon)

    def test_kahan_bem_melhor_que_ingenuo(self):
        """Com 10000 parcelas de 0,1, o erro do Kahan é mil vezes menor que o do ingênuo."""
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        parcelas = [0.1] * 10_000
        ingenuo.adicionar_todos(parcelas)
        kahan.adicionar_todos(parcelas)
        erro_ingenuo = abs(ingenuo.total - 1000.0)
        erro_kahan = abs(kahan.total - 1000.0)
        self.assertGreater(erro_ingenuo, 0.0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)


if __name__ == "__main__":
    unittest.main()

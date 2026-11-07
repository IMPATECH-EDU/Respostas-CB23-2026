"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from decimal import Decimal

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestKahanRegressao(unittest.TestCase):
    """Issue #7: o AcumuladorKahan precisa de fato compensar o arredondamento."""

    def test_dez_decimos_dao_exatamente_um(self):
        """Dez parcelas de 0,1: o ingênuo dá 0,999...9; Kahan deve dar o float 1.0 exato."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 10)
        self.assertEqual(kahan.total, 1.0)   # igualdade exata: é o que a compensação garante

    def test_parcelas_menores_que_o_ulp_nao_se_perdem(self):
        """1 + dez parcelas de 1e-16: o ingênuo fica em 1.0; Kahan recupera o 1e-15 somado."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertAlmostEqual(kahan.total - 1.0, 1e-15, delta=2.3e-16)

    def test_erro_muito_menor_que_o_ingenuo(self):
        """Em 100 000 parcelas de 0,1 L, o erro de Kahan é ao menos mil vezes menor."""
        n, ideal = 100_000, Decimal(10_000)
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        for acumulador in (ingenuo, kahan):
            acumulador.adicionar_todos([0.1] * n)
        erro_ingenuo = abs(Decimal(ingenuo.total) - ideal)
        erro_kahan = abs(Decimal(kahan.total) - ideal)
        self.assertGreater(erro_ingenuo, 0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)


if __name__ == "__main__":
    unittest.main()

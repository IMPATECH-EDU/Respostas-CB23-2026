"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Testes de regressão para o defeito da issue #7 no AcumuladorKahan."""

    def test_kahan_um_milhao_de_decimos(self):
        """Soma 1 000 000 de parcelas de 0,1 L sem acumular erro de arredondamento."""
        acc = AcumuladorKahan()
        acc.adicionar_todos([0.1] * 1_000_000)
        self.assertAlmostEqual(acc.total, 100_000.0, places=9)

    def test_kahan_parcelas_pequenas_apos_grande(self):
        """Compensa parcelas menores que metade do ULP somadas após um número grande."""
        acc = AcumuladorKahan()
        acc.adicionar(1e10)
        acc.adicionar_todos([5e-7] * 10_000)
        self.assertAlmostEqual(acc.total, 1e10 + 0.005, places=6)


if __name__ == "__main__":
    unittest.main()
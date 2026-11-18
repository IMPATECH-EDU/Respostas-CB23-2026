"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import (AcumuladorIngenuo, AcumuladorKahan)


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)

    def test_acumulador_kahan_1(self):
        """100_000_000 pulsos de 0,1 deveria dar 100_000_000.0"""
        kahan = AcumuladorKahan()
        for _ in range (100_000_000):
            kahan.adicionar(0.1)
        self.assertAlmostEqual(kahan.total, 10_000_000)

    def test_acumulador_kahan_2(self):
        """500_000_000 pulsos de 0,1 deveria dar 500_000_000.0"""
        kahan_2 = AcumuladorKahan()
        for _ in range (10_000_000):
            kahan_2.adicionar(0.1)
        self.assertAlmostEqual(kahan_2.total, 1_000_000)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

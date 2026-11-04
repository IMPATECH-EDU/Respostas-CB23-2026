"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from math import isclose


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestAcumuladorKahan(unittest.TestCase):
    """Testa o acumulador de Kahan."""

    def test_acumulação_exata_1(self):
        """Testa a acumulação usando assertAlmostEqual"""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1]*1_000_000)
        valor = acumulador.total
        self.assertAlmostEqual(valor, 100_000.0)

    def test_acumulação_exata_2(self):
        """Testa a acumulação usando o math.isclose"""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1]*2_000_000)
        valor = acumulador.total
        self.assertTrue(isclose(valor, 200_000.0, rel_tol=1e-12))



if __name__ == "__main__":
    unittest.main()

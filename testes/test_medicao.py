"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)



import math
from itertools import repeat
from elevatoria.acumuladores import AcumuladorKahan


class TestKahanRegressao(unittest.TestCase):
    """Regressões da compensação de arredondamento da issue #7."""

    def test_pulsos_decimais(self) -> None:
        """Cem mil pulsos decimais não acumulam o erro da soma ingênua."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos(repeat(0.1, 100_000))
        self.assertAlmostEqual(acumulador.total, 10_000.0, delta=1e-11)

    def test_parcelas_menores_que_ulp(self) -> None:
        """Parcelas unitárias perdidas isoladamente são recuperadas pela compensação."""
        acumulador = AcumuladorKahan()
        parcelas = [float(2 ** 54), 1.0, 1.0, 1.0, 1.0]
        acumulador.adicionar_todos(parcelas)
        self.assertAlmostEqual(acumulador.total, math.fsum(parcelas), delta=0.5)


if __name__ == "__main__":
    unittest.main()

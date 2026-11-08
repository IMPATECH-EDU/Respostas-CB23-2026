"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan

import math

class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestAcumuladorKahan(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorKahan().total, 0.0)

    def test_com_100_000_parcelas(self):
        """A Soma de 100_000 parcelas de 0.1 é 10_000."""
        acumulador = AcumuladorKahan()
        for _ in range(100_000):
            acumulador.adicionar(0.1)
        self.assertEqual(acumulador.total, 10_000.0)

    def test_com_10_000_000_parcelas(self):
        """A Soma de 10_000_000 parcelas de 0.1 é 1_000_000."""
        acumulador = AcumuladorKahan()
        for _ in range(10_000_000):
            acumulador.adicionar(0.1)
        self.assertEqual(acumulador.total, 1_000_000.0)

    def test_parcelas_pequenas_nao_somem(self):
        """1.0 seguido de 10 parcelas de 1e-16 dá o mesmo que math.fsum, e não 1.0."""
        valores = [1.0] + [1e-16] * 10
        acumulador = AcumuladorKahan()
        for x in valores:
            acumulador.adicionar(x)
        self.assertEqual(acumulador.total, math.fsum(valores))

    def test_parcelas_diferentes(self):
        """A Soma de 1000 vezes 0.1, 0.2 e 0.3 dá o mesmo que math.fsum."""
        valores = [0.1, 0.2, 0.3] * 1000
        acumulador = AcumuladorKahan()
        for x in valores:
            acumulador.adicionar(x)
        self.assertEqual(acumulador.total, math.fsum(valores))

if __name__ == "__main__":
    unittest.main()

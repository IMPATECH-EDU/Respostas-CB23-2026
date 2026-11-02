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

import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan


class TestRegressãoAcumuladorKahan(unittest.TestCase):
    """Testes de regressão do AcumuladorKahan."""

    def test_duzentosk_pulsos(self):
        """200000 parcelas de 0,1 devem somar 20000.0 sem o erro do acumulador ingênuo."""
        acumulador = AcumuladorKahan()
        for _ in range(200_000):
            acumulador.adicionar(0.1)
        self.assertAlmostEqual(acumulador.total, 20000.0, places=9)

    def test_parcelas_pequenas_nao_somem(self):
        """Parcelas de 1e-16 somadas a 1.0 não se perdem, pois o total é superior a 1.0."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar(1.0)
        for _ in range(10):
            acumulador.adicionar(1e-16)
        self.assertGreater(acumulador.total, 1.0)
# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

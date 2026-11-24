"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo
from elevatoria.acumuladores import AcumuladorKahan


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestAcumuladorKahan(unittest.TestCase):

    def test_desoma(self):
        """Soma 1000 vezes o valor 0.1, o resultado deve ser 100."""
        a = AcumuladorKahan()
        b = [0.1 for i in range(1000)]
        for valor in b:
            a.adicionar(valor)
        resultado = a.total
        self.assertEqual(resultado, 100)
    def test_cancelamento(self):
        """soma 1e16+1.0+1.0-1e16, deve resultar em 2.0"""
        a = AcumuladorKahan()
        b = [1e16,1.0,1.0,-1e16]
        for valor in b:
            a.adicionar(valor)
        resultado = a.total
        self.assertEqual(resultado,2.0)


if __name__ == "__main__":
    unittest.main()

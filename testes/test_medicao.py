"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestKahanRegressao(unittest.TestCase):
    """Issue #7: o AcumuladorKahan não compensava nada. Escritos antes da correção."""

    def test_milhao_de_decimos(self):
        """Um milhão de parcelas de 0,1 L dá exatamente 100000.0, como pede o relato."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 1_000_000)
        self.assertEqual(kahan.total, 100000.0)   # aqui a igualdade exata é o que se testa

    def test_parcelas_menores_que_o_ulp(self):
        """Dez parcelas de 1e-16 depois de 1.0 não se perdem: o total vira 1 + 1e-15."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertTrue(math.isclose(kahan.total, 1.0 + 1e-15, rel_tol=0.0, abs_tol=1e-16))


if __name__ == "__main__":
    unittest.main()

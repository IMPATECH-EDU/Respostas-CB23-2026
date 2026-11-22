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


# ---------------------------------------------------------------------------------------
# Issue #7: regressão do AcumuladorKahan (escritos antes da correção; falham no original)
# ---------------------------------------------------------------------------------------
class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: a soma de Kahan precisa compensar o arredondamento de verdade.

    Aqui a igualdade exata é o que se quer testar: a soma compensada deve dar o float
    correto, e não um valor apenas próximo.
    """

    def test_dez_parcelas_de_um_decimo_dao_exatamente_um(self):
        """0,1 somado 10 vezes dá 1.0 exato (a soma direta dá 0.9999999999999999)."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 10)
        self.assertEqual(kahan.total, 1.0)

    def test_parcelas_pequenas_nao_somem(self):
        """Dez parcelas de 1e-16 somadas a 1.0 aparecem no total, como em math.fsum."""
        valores = [1.0] + [1e-16] * 10
        kahan = AcumuladorKahan()
        kahan.adicionar_todos(valores)
        self.assertEqual(kahan.total, math.fsum(valores))
        self.assertGreater(kahan.total, 1.0)

    def test_um_milhao_de_pulsos(self):
        """O caso do relato: 1 000 000 de pulsos de 0,1 L totalizam 100000.0 exatos."""
        kahan = AcumuladorKahan()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
        self.assertEqual(kahan.total, 100000.0)


if __name__ == "__main__":
    unittest.main()

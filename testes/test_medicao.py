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


# ---------------------------------------------------------------------------------------
# Issue #7: testes de regressão do AcumuladorKahan (escritos antes da correção)
# ---------------------------------------------------------------------------------------
class TestKahanRegressao(unittest.TestCase):
    """Issue #7: a soma de Kahan tem que compensar o arredondamento."""

    def test_dez_decimos_dao_exatamente_um(self):
        """Dez parcelas de 0.1: a soma ingênua dá 0.9999999999999999 e a de Kahan, 1.0."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 10)
        # aqui a igualdade exata é o ponto: é isso que separa Kahan da soma ingênua
        self.assertEqual(kahan.total, 1.0)

    def test_parcelas_menores_que_meio_ulp(self):
        """1.0 seguido de 10000 parcelas de 1e-16: a ingênua perde todas, Kahan não perde."""
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        for acumulador in (ingenuo, kahan):
            acumulador.adicionar(1.0)
            acumulador.adicionar_todos([1e-16] * 10_000)
        self.assertEqual(ingenuo.total, 1.0)          # cada 1.0 + 1e-16 arredonda para 1.0
        self.assertAlmostEqual(kahan.total, 1.0 + 1e-12, delta=1e-15)

    def test_um_milhao_de_pulsos(self):
        """O caso do relato: 1 000 000 de parcelas de 0,1 L somam exatamente 100000.0 L."""
        kahan = AcumuladorKahan()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
        self.assertEqual(kahan.total, 100000.0)


if __name__ == "__main__":
    unittest.main()

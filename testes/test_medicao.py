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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan não compensava o arredondamento."""

    def test_um_milhao_de_decimos_da_exatamente_cem_mil(self):
        """Um milhão de parcelas de 0,1 somadas com Kahan dão exatamente 100000.0."""
        acc = AcumuladorKahan()
        acc.adicionar_todos([0.1] * 1_000_000)
        self.assertEqual(acc.total, 100000.0)

    def test_kahan_erra_menos_que_a_soma_ingenua(self):
        """Com dez mil parcelas de 0,1, o erro de Kahan é menor que o da soma ingênua."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        kahan.adicionar_todos([0.1] * 10_000)
        ingenuo.adicionar_todos([0.1] * 10_000)
        self.assertLess(abs(kahan.total - 1000.0), abs(ingenuo.total - 1000.0))

    def test_parcela_pequena_depois_de_uma_grande_nao_se_perde(self):
        """1e16 + 1 + 1 com Kahan dá 1e16 + 2; a soma ingênua perde as duas parcelas de 1."""
        acc = AcumuladorKahan()
        acc.adicionar_todos([1e16, 1.0, 1.0])
        self.assertTrue(math.isclose(acc.total, 1e16 + 2, rel_tol=0, abs_tol=0.5))


if __name__ == "__main__":
    unittest.main()

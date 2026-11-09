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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoKahan(unittest.TestCase):
    """Testes de regressão da issue #7 ANTES da correção."""

    def test_kahan_um_milhao_de_pulsos(self):
        """Totalização de 1 000 000 parcelas de 0.1 L deve totalizar 100000.0 exatos."""
        from elevatoria.acumuladores import AcumuladorKahan
        acc = AcumuladorKahan()
        for _ in range(1_000_000):
            acc.adicionar(0.1)
        self.assertEqual(acc.total, 100000.0)

    def test_kahan_difere_de_acumulador_ingenuo(self):
        """AcumuladorKahan não deve produzir o mesmo erro acumulado do AcumuladorIngenuo."""
        from elevatoria.acumuladores import AcumuladorKahan
        kahan = AcumuladorKahan()
        ingenuo = AcumuladorIngenuo()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
            ingenuo.adicionar(0.1)
        self.assertNotEqual(kahan.total, ingenuo.total)


if __name__ == "__main__":
    unittest.main()

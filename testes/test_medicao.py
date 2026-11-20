"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import random
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
    """Issue #7: o AcumuladorKahan somava igual ao ingênuo, sem compensar nada."""

    def test_pulsos_de_um_decimo(self):
        """10⁵ pulsos de 0,1 L dão exatamente 10000.0, onde a soma ingênua já erra."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        pulsos = [0.1] * 100_000
        kahan.adicionar_todos(pulsos)
        ingenuo.adicionar_todos(pulsos)
        self.assertNotEqual(ingenuo.total, 10_000.0)   # o problema existe
        self.assertEqual(kahan.total, 10_000.0)        # e o Kahan o resolve (igualdade exata)

    def test_parcelas_menores_que_meio_ulp(self):
        """Parcelas que somem sozinhas ao lado de 1.0 se acumulam na correção e aparecem no total."""
        kahan = AcumuladorKahan()
        kahan.adicionar(1.0)
        kahan.adicionar_todos([1e-16] * 1000)          # cada 1e-16 é menor que meio ulp de 1.0
        self.assertTrue(math.isclose(kahan.total, 1.0 + 1e-13, rel_tol=1e-15))

    def test_concorda_com_fsum(self):
        """Em valores aleatórios de magnitudes variadas, o Kahan fica a ~1 ulp da soma exata (math.fsum)."""
        gerador = random.Random(3472)
        valores = [gerador.uniform(0.0, 1.0) * 10.0 ** gerador.randint(-8, 3) for _ in range(20_000)]
        kahan = AcumuladorKahan()
        kahan.adicionar_todos(valores)
        exato = math.fsum(valores)
        self.assertLessEqual(abs(kahan.total - exato), 2 * math.ulp(exato))


if __name__ == "__main__":
    unittest.main()

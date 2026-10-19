"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.medicao import medir
from elevatoria.dados import Registro


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)

class TestRegressaoIssue7(unittest.TestCase):
    """Testes de regressão do defeito numérico no AcumuladorKahan (Issue #7)."""

    def test_soma_um_milhao_de_decimos(self):
        """A soma de um milhão de parcelas de 0.1 deve dar exatamente 100000.0 com Kahan."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)
        # O teste exige igualdade exata para comprovar a compensação do erro de truncamento
        self.assertEqual(acumulador.total, 100000.0)

    def test_perda_de_precisao_com_parcelas_desiguais(self):
        """Soma de um valor grande seguido de muitos pequenos retém a precisão dos menores."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar(10000.0)
        # Em float64, 10000.0 + 1e-12 perde o 1e-12 num acumulador ingênuo
        for _ in range(10_000):
            acumulador.adicionar(1e-12)
        # A compensação de Kahan deve preservar a mantissa acumulada e resultar no valor exato
        self.assertEqual(acumulador.total, 10000.00000001)


if __name__ == "__main__":
    unittest.main()

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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestKahanRegressao(unittest.TestCase):
    def test_soma_um_milhao_de_decimos(self):
        """Totaliza um milhão de parcelas de 0,1 L com erro sob controle."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)

        self.assertAlmostEqual(acumulador.total, 100_000.0, delta=1e-9)

    def test_recupera_duas_parcelas_pequenas(self):
        """Recupera duas parcelas unitárias somadas após um valor grande."""
        acumulador = AcumuladorKahan()
        for parcela in (1e16, 1.0, 1.0, -1e16):
            acumulador.adicionar(parcela)

        self.assertAlmostEqual(acumulador.total, 2.0, delta=1e-12)

if __name__ == "__main__":
    unittest.main()

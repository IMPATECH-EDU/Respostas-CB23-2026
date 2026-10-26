"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.medicao import medir, CurvaCalibracao
from fornecido.testes_aceitacao.test_aceitacao_m2 import registros



class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)

    def test_kahan_soma_de_pequenos(self):
        "Soma várias parcelas de 0.1"
        a = AcumuladorKahan()
        for _ in range(10_000_000):
            a.adicionar(0.1)
        self.assertAlmostEqual(a.total, 1_000_000)

    def test_kahan_pequeno_com_grande(self):
        "Soma um inteiro grande com vários números pequenos em relação a ele"
        b = AcumuladorKahan()
        b.adicionar(1000000)
        for _ in range(1000000):
            b.adicionar(1e-6)
        self.assertAlmostEqual(b.total, 1000001)

    def test_medir_u_sistematica_negativa(self):
        
        """Levanta ValueError se u_sistematica for negativa."""
        IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
        with self.assertRaises(ValueError):
            medir(registros("PT101", [10, 11, 10, 11, 10]), "PT101", IDENTIDADE, u_sistematica=-1.0)

    def test_medir_mad_zero(self):
        """Levanta ValueError se a MAD for zero (série sem variação nas leituras principais)."""
        IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
        
        # Leituras totalmente constantes geram desvio absoluto mediano zero
        constantes = [10, 10, 10, 10, 10, 10, 10, 10]
        with self.assertRaises(ValueError):
            medir(registros("PT101", constantes), "PT101", IDENTIDADE)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

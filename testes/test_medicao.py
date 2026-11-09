"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def registros(tag: str, contagens: list) -> list:
    """Registros de leitura da `tag`, um a cada 6 s, com as contagens dadas."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]

class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Regressão da issue #7: o AcumuladorKahan precisa compensar o arredondamento."""

    def test_parcelas_pequenas(self):
        """Dez parcelas de 0.1 somam exatamente 1.0."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 10)
        self.assertEqual(acumulador.total, 1.0)

    def test_parcelas_muito_pequenas(self):
        """10 parcelas de números muito pequenos somados a 1.0 devem somar quase 1.0 + 1e-15"""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertAlmostEqual(acumulador.total, 1.0 + 1e-15, delta=1e-16)

class TestMedirContrato(unittest.TestCase):
    """Regras do contrato de `medir` que os testes de aceitação não cobrem."""

    def test_u_sistematica_negativa(self):
        """Uma incerteza sistemática negativa levanta ValueError."""
        regs = registros("PT101", [10, 11, 9, 10])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, u_sistematica=-1.0)

    def test_mad_zero(self):
        """Leituras todas iguais têm mad zero e levantam ValueError."""

        regs = registros("PT101", [10, 10, 10, 10])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)

if __name__ == "__main__":
    unittest.main()

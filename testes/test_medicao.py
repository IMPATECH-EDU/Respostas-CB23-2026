"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
from datetime import datetime, timedelta
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def _registros(tag: str, contagens: list[float]) -> list[Registro]:
    """Cria registros sintéticos para uma tag a partir de uma lista de contagens."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Testes de regressão para o defeito da issue #7 no AcumuladorKahan."""

    def test_kahan_um_milhao_de_decimos(self):
        """Soma 1 000 000 de parcelas de 0,1 L sem acumular erro de arredondamento."""
        acc = AcumuladorKahan()
        acc.adicionar_todos([0.1] * 1_000_000)
        self.assertAlmostEqual(acc.total, 100_000.0, places=9)

    def test_kahan_parcelas_pequenas_apos_grande(self):
        """Compensa parcelas menores que metade do ULP somadas após um número grande."""
        acc = AcumuladorKahan()
        acc.adicionar(1e10)
        acc.adicionar_todos([5e-7] * 10_000)
        self.assertAlmostEqual(acc.total, 1e10 + 0.005, places=6)


class TestMedirContrato(unittest.TestCase):
    """Casos do contrato de `medir` não cobertos pelos testes de aceitação."""

    def test_u_sistematica_negativa(self):
        """Levanta ValueError quando u_sistematica é negativa."""
        regs = _registros("PT101", [10, 11, 9, 10, 12])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, u_sistematica=-0.5)

    def test_mad_zero(self):
        """Levanta ValueError quando a MAD das leituras é zero."""
        regs = _registros("PT101", [100, 100, 100, 100, 100])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)

    def test_fora_do_dominio_da_curva(self):
        """Propaga o ValueError da curva quando há contagem fora do domínio."""
        regs = _registros("PT101", [10, 11, 9, 5000])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)


if __name__ == "__main__":
    unittest.main()
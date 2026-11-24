"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import (AcumuladorIngenuo, AcumuladorKahan)
from elevatoria.medicao import medir
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from datetime import datetime, timedelta


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)

    def test_acumulador_kahan_1(self):
        """100_000_000 pulsos de 0,1 deveria dar 100_000_000.0"""
        kahan = AcumuladorKahan()
        for _ in range (100_000_000):
            kahan.adicionar(0.1)
        self.assertAlmostEqual(kahan.total, 10_000_000)

    def test_acumulador_kahan_2(self):
        """500_000_000 pulsos de 0,1 deveria dar 500_000_000.0"""
        kahan_2 = AcumuladorKahan()
        for _ in range (10_000_000):
            kahan_2.adicionar(0.1)
        self.assertAlmostEqual(kahan_2.total, 1_000_000)

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def _regs(tag: str, contagens: list[float]) -> list[Registro]:
    """Cria registros fictícios da `tag` a cada 6 s."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: testes de regressão para `AcumuladorKahan`."""

    def test_kahan_um_milhao_de_decimos(self):
        """Soma 1.000.000 de parcelas de 0,1 L compensando o erro de arredondamento."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 1_000_000)
        self.assertLess(abs(kahan.total - 100_000.0), 1e-12)

    def test_kahan_parcelas_pequenas_apos_grande(self):
        """Preserva parcelas pequenas somadas após um acumulador de grande magnitude."""
        kahan = AcumuladorKahan()
        kahan.adicionar(1e8)
        kahan.adicionar_todos([1e-5] * 1_000)
        self.assertLess(abs(kahan.total - (1e8 + 0.01)), 1e-12)


class TestContratoMedir(unittest.TestCase):
    """Issue #6: regras de contrato de `medir` não cobertas pela aceitação."""

    def test_medir_rejeita_u_sistematica_negativa(self):
        """Levanta ValueError quando u_sistematica é negativa."""
        with self.assertRaises(ValueError):
            medir(_regs("PT101", [100, 101, 99, 100]), "PT101", IDENTIDADE, u_sistematica=-0.5)

    def test_medir_rejeita_mad_zero(self):
        """Levanta ValueError quando todas as leituras são idênticas (MAD = 0)."""
        with self.assertRaises(ValueError):
            medir(_regs("PT101", [150, 150, 150, 150]), "PT101", IDENTIDADE)

    def test_medir_rejeita_menos_de_duas_validas_apos_filtro(self):
        """Levanta ValueError se o descarte de espúrias deixar menos de 2 leituras válidas."""
        with self.assertRaises(ValueError):
            medir(_regs("PT101", [100, 100, 200, 500, 600]), "PT101", IDENTIDADE, limiar=0.1)

# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

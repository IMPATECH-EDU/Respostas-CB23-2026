"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
from datetime import datetime, timedelta
import math
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def _criar_registros(tag: str, contagens: list[float]) -> list[Registro]:
    """Cria lista de Registro a cada 6 segundos."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [
        Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
        for i, c in enumerate(contagens)
    ]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoIssue7(unittest.TestCase):
    """Testes de regressão para a issue #7 (AcumuladorKahan)."""

    def test_kahan_precisao_muitas_parcelas(self):
        """AcumuladorKahan compensa erro de arredondamento em 1000000 de parcelas de 0.1."""
        kahan = AcumuladorKahan()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
        self.assertAlmostEqual(kahan.total, 100_000.0, places=5)

    def test_kahan_diferente_de_ingenuo_em_longa_sequencia(self):
        """AcumuladorKahan produz erro pelo menos 1000 vezes menor que o AcumuladorIngenuo."""
        kahan = AcumuladorKahan()
        ingenuo = AcumuladorIngenuo()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
            ingenuo.adicionar(0.1)
        erro_ingenuo = abs(ingenuo.total - 100_000.0)
        erro_kahan = abs(kahan.total - 100_000.0)
        self.assertLess(erro_kahan, erro_ingenuo / 1000.0)


class TestMedirContrato(unittest.TestCase):
    """Testes de regras do contrato de medir que os testes de aceitação não verificam."""

    def test_u_sistematica_negativa_levanta_value_error(self):
        """medir levanta ValueError se u_sistematica for negativa."""
        regs = _criar_registros("PT101", [100.0, 102.0, 101.0, 99.0])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, u_sistematica=-0.5)

    def test_mad_zero_levanta_value_error(self):
        """medir levanta ValueError se todas as contagens forem idênticas (MAD igual a zero)."""
        regs = _criar_registros("PT101", [100.0, 100.0, 100.0, 100.0])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)

    def test_menos_de_duas_leituras_validas_levanta_value_error(self):
        """medir levanta ValueError se após descarte de espúrias sobrarem menos de 2 leituras válidas."""
        # Se temos 3 pontos, dois muito distantes e um isolado:
        regs = _criar_registros("PT101", [100.0, 100.1, 1000.0, 2000.0, 3000.0])
        # Com limiar pequeno para descartar quase tudo ou poucas leituras válidas restantes
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, limiar=0.5)


if __name__ == "__main__":
    unittest.main()

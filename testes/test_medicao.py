"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime, timedelta

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.medicao import medir


IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0],
                             [0.0, 2000.0, 4095.0], "linear")


def registros(tag: str, contagens: list) -> list:
    """Cria registros consecutivos com a tag e as contagens informadas."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag,
                     {"contagens": float(contagem)})
            for i, contagem in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoAcumuladorKahan(unittest.TestCase):
    """Regressões da issue #7."""

    def test_um_milhao_de_decimos(self):
        """A soma compensada de um milhão de décimos deve ser exata."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 1_000_000)
        self.assertAlmostEqual(acumulador.total, 100_000.0, places=12)

    def test_parcelas_pequenas_apos_valor_grande(self):
        """A soma compensada preserva parcelas pequenas após um valor grande."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar(17_012_007.0)
        acumulador.adicionar_todos([0.1] * 1_000)
        self.assertAlmostEqual(acumulador.total, 17012107.0, places=12)


class TestMedirContrato(unittest.TestCase):
    """Testes adicionais das regras de contrato de medir."""

    def test_incerteza_sistematica_negativa(self):
        """Incerteza sistemática negativa deve levantar ValueError."""
        regs = registros("PT101", [10, 11])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, u_sistematica=-1.0)

    def test_mad_zero(self):
        """Leituras constantes devem levantar ValueError quando a MAD é zero."""
        regs = registros("PT101", [10, 10, 10])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)


if __name__ == "__main__":
    unittest.main()

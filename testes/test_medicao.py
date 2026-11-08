"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.medicao import medir
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from math import isclose


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestAcumuladorKahan(unittest.TestCase):
    """Testa o acumulador de Kahan."""

    def test_acumulação_exata_1(self):
        """Testa a acumulação usando assertAlmostEqual"""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1]*1_000_000)
        valor = acumulador.total
        self.assertAlmostEqual(valor, 100_000.0)

    def test_acumulação_exata_2(self):
        """Testa a acumulação usando o math.isclose"""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1]*2_000_000)
        valor = acumulador.total
        self.assertTrue(isclose(valor, 200_000.0, rel_tol=1e-12))


class TestMedir(unittest.TestCase):
    """Testes para a função medir."""

    IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")

    @staticmethod
    def registros(tag: str, contagens: list[float | int], nivel: str = "INFO") -> list[Registro]:
        """Função auxiliar para criar registros do teste."""
        return [
            Registro(
                instante=float(i),
                nivel = nivel,
                tag=tag,
                valores={"contagens": float(c)}
            )
            for i, c in enumerate(contagens)
        ]

    def test_u_sistematica_negativa(self):
        """Testa se incerteza sistemática negativa levanta ValueError."""
        regs = self.registros("PT101", [10, 11, 9, 10, 12, 11, 10, 9])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", self.IDENTIDADE, u_sistematica=-1.0)

    def test_mad_zero(self):
        """Testa se série constante (MAD zero) levanta ValueError."""
        regs = self.registros("PT101", [10] * 8)
        with self.assertRaises(ValueError):
            medir(regs, "PT101",self.IDENTIDADE)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
NORMAIS = [10, 11, 9, 10, 12, 11, 10, 9]


def _registros(tag: str, contagens: list) -> list:
    """Registros de leitura da `tag`, um a cada 6 s, com as contagens dadas."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan não compensava o arredondamento."""

    def test_um_milhao_de_decimos(self):
        """1 000 000 parcelas de 0,1 somam 100 000 com erro menor que 1e-9 (o ingênuo erra 1,3e-6)."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 1_000_000)
        self.assertLess(abs(acumulador.total - 100_000.0), 1e-9)

    def test_parcelas_menores_que_o_ulp(self):
        """Dez parcelas de 1e-16 somadas a 1,0 não se perdem: o total é 1 + 1e-15."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertGreater(acumulador.total, 1.0)
        self.assertTrue(math.isclose(acumulador.total, 1.0 + 1e-15, rel_tol=0, abs_tol=2.3e-16))

    def test_melhor_que_o_ingenuo(self):
        """Com parcelas de 0,1, o erro do Kahan é pelo menos 1000 vezes menor que o do ingênuo."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        for acumulador in (kahan, ingenuo):
            acumulador.adicionar_todos([0.1] * 100_000)
        self.assertLess(abs(kahan.total - 10_000.0), abs(ingenuo.total - 10_000.0) / 1000)


class TestContratoMedir(unittest.TestCase):
    """Issue #6: regras do contrato de medir que os testes de aceitação não verificam."""

    def test_u_sistematica_negativa(self):
        """u_sistematica < 0 levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", NORMAIS), "PT101", IDENTIDADE, u_sistematica=-0.1)

    def test_mad_zero(self):
        """Leituras todas iguais têm MAD zero, e medir levanta ValueError em vez de dividir por zero."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", [10] * 8), "PT101", IDENTIDADE)

    def test_indices_na_serie_da_tag(self):
        """Os índices das espúrias contam só as leituras da tag, e não a posição no log."""
        regs = []
        recalque = [10, 11, 9, 500, 12, 11, 10, 9, 10]
        for a, b in zip(_registros("PT101", NORMAIS + [10]), _registros("PT102", recalque)):
            regs += [a, b]
        self.assertEqual(medir(regs, "PT102", IDENTIDADE).espurias, [3])

    def test_erro_da_curva_chega_a_quem_chamou(self):
        """Uma contagem fora do domínio da curva faz o ValueError da curva subir até quem chamou."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(_registros("PT101", NORMAIS + [5000]), "PT101", IDENTIDADE)

    def test_limiar_menor_descarta_mais(self):
        """Com limiar menor, uma leitura moderadamente afastada também é descartada."""
        regs = _registros("PT101", NORMAIS + [15])
        self.assertEqual(medir(regs, "PT101", IDENTIDADE).espurias, [])
        self.assertEqual(medir(regs, "PT101", IDENTIDADE, limiar=3.0).espurias, [8])


if __name__ == "__main__":
    unittest.main()

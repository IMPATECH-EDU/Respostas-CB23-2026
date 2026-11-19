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


def leitura(i: int, tag: str, **valores: object) -> Registro:
    """Registro da `tag` no instante 08:00:00 + 6i s, com os pares chave=valor dados."""
    return Registro(datetime(2026, 10, 5, 8) + timedelta(seconds=6 * i), "INFO", tag, valores)


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestKahanRegressao(unittest.TestCase):
    """Issue #7: o AcumuladorKahan não compensava nada. Escritos antes da correção."""

    def test_milhao_de_decimos(self):
        """Um milhão de parcelas de 0,1 L dá exatamente 100000.0, como pede o relato."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 1_000_000)
        self.assertEqual(kahan.total, 100000.0)   # aqui a igualdade exata é o que se testa

    def test_parcelas_menores_que_o_ulp(self):
        """Dez parcelas de 1e-16 depois de 1.0 não se perdem: o total vira 1 + 1e-15."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertTrue(math.isclose(kahan.total, 1.0 + 1e-15, rel_tol=0.0, abs_tol=1e-16))


class TestMedirContrato(unittest.TestCase):
    """Issue #6: regras de medir que os testes de aceitação não conferem."""

    def setUp(self):
        self.contagens = [100, 101, 99, 100, 102, 98, 100, 101]
        self.regs = [leitura(i, "PT101", contagens=c) for i, c in enumerate(self.contagens)]

    def test_u_sistematica_negativa(self):
        """u_sistematica negativa levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "negativa"):
            medir(self.regs, "PT101", IDENTIDADE, u_sistematica=-0.5)

    def test_mad_zero_com_maioria_repetida(self):
        """Seis de oito leituras iguais já zeram a MAD, e medir levanta ValueError."""
        regs = [leitura(i, "PT101", contagens=c) for i, c in enumerate([100] * 6 + [101, 99])]
        with self.assertRaisesRegex(ValueError, "MAD"):
            medir(regs, "PT101", IDENTIDADE)

    def test_menos_de_duas_validas(self):
        """Com limiar 0,5 em [10, 11, 12] só a leitura do meio passa, e medir levanta ValueError."""
        regs = [leitura(i, "PT101", contagens=c) for i, c in enumerate([10, 11, 12])]
        with self.assertRaisesRegex(ValueError, "limiar"):
            medir(regs, "PT101", IDENTIDADE, limiar=0.5)

    def test_indice_e_posicao_na_serie_da_tag(self):
        """O índice da espúria conta só as leituras da tag, sem PT101 nem o alarme no meio."""
        regs = []
        for i, c in enumerate(self.contagens + [900]):
            regs += [leitura(i, "PT101", contagens=30), leitura(i, "PT102", contagens=c)]
        regs.insert(3, leitura(1, "PT102", evento="pressao_alta", limite=2000.0))
        m = medir(regs, "PT102", IDENTIDADE)
        self.assertEqual((m.espurias, m.n_validas), ([8], 8))


if __name__ == "__main__":
    unittest.main()

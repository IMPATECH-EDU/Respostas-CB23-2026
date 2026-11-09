"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoKahan(unittest.TestCase):
    """Testes de regressão da issue #7 ANTES da correção."""

    def test_kahan_um_milhao_de_pulsos(self):
        """Totalização de 1 000 000 parcelas de 0.1 L deve totalizar 100000.0 exatos."""
        from elevatoria.acumuladores import AcumuladorKahan
        acc = AcumuladorKahan()
        for _ in range(1_000_000):
            acc.adicionar(0.1)
        self.assertEqual(acc.total, 100000.0)

    def test_kahan_difere_de_acumulador_ingenuo(self):
        """AcumuladorKahan não deve produzir o mesmo erro acumulado do AcumuladorIngenuo."""
        from elevatoria.acumuladores import AcumuladorKahan
        kahan = AcumuladorKahan()
        ingenuo = AcumuladorIngenuo()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
            ingenuo.adicionar(0.1)
        self.assertNotEqual(kahan.total, ingenuo.total)


class TestMedirContrato(unittest.TestCase):
    """Testes de contrato de medir não cobertos pelos testes de aceitação."""

    def setUp(self):
        from elevatoria.calibracao import CurvaCalibracao
        from elevatoria.dados import Registro
        from datetime import datetime, timedelta
        self.curva = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
        t0 = datetime(2026, 10, 5, 8, 0, 0)
        self.regs = [
            Registro(t0 + timedelta(seconds=6 * i), "INFO", "PT101", {"contagens": float(c)})
            for i, c in enumerate([100, 102, 101, 103, 99])
        ]

    def test_u_sistematica_negativa(self):
        """u_sistematica negativa deve levantar ValueError."""
        from elevatoria.medicao import medir
        with self.assertRaises(ValueError):
            medir(self.regs, "PT101", self.curva, u_sistematica=-0.5)

    def test_mad_zero_levanta_erro(self):
        """Quando todas as leituras são idênticas, a MAD é zero e deve levantar ValueError."""
        from elevatoria.dados import Registro
        from elevatoria.medicao import medir
        from datetime import datetime, timedelta
        t0 = datetime(2026, 10, 5, 8, 0, 0)
        regs_const = [
            Registro(t0 + timedelta(seconds=6 * i), "INFO", "PT101", {"contagens": 100.0})
            for i in range(5)
        ]
        with self.assertRaises(ValueError):
            medir(regs_const, "PT101", self.curva)

    def test_menos_de_duas_leituras_validas_apos_descarte(self):
        """Se restarem menos de 2 leituras válidas após descarte de espúrias, levanta ValueError."""
        from elevatoria.dados import Registro
        from elevatoria.medicao import medir
        from datetime import datetime, timedelta
        t0 = datetime(2026, 10, 5, 8, 0, 0)
        # Cria uma série onde outliers extremos fazem sobrar menos de duas leituras com limiar agressivo
        regs_poucas = [
            Registro(t0 + timedelta(seconds=6 * i), "INFO", "PT101", {"contagens": float(c)})
            for i, c in enumerate([100, 101, 1000, 2000, 3000])
        ]
        with self.assertRaises(ValueError):
            medir(regs_poucas, "PT101", self.curva, limiar=0.01)


if __name__ == "__main__":
    unittest.main()

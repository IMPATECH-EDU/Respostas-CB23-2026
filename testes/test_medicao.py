"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime, timedelta
from decimal import Decimal

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestKahanRegressao(unittest.TestCase):
    """Testes de regressao da issue #7 escritos antes da correcao de AcumuladorKahan."""

    def test_kahan_um_milhao_de_decimos(self):
        """Soma de um milhao de parcelas 0.1 no AcumuladorKahan reduz o erro frente ao ingenuo."""
        ingenuo = AcumuladorIngenuo()
        kahan = AcumuladorKahan()
        for _ in range(1_000_000):
            ingenuo.adicionar(0.1)
            kahan.adicionar(0.1)
        ideal = Decimal("100000")
        erro_ingenuo = abs(Decimal(ingenuo.total) - ideal)
        erro_kahan = abs(Decimal(kahan.total) - ideal)
        self.assertGreater(erro_ingenuo, Decimal("0"))
        self.assertLessEqual(erro_kahan, erro_ingenuo / Decimal("1000"))

    def test_kahan_preserva_parcelas_pequenas_apos_numero_grande(self):
        """Parcelas pequenas apos valor grande nao desaparecem na soma compensada de Kahan."""
        kahan = AcumuladorKahan()
        kahan.adicionar(1e12)
        kahan.adicionar_todos([1e-4] * 10_000)
        self.assertAlmostEqual(kahan.total, 1e12 + 1.0, places=3)


class TestMedirContrato(unittest.TestCase):
    """Testes de contrato de medir nao cobertos pela aceitacao."""

    def setUp(self):
        self.curva = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
        self.t0 = datetime(2026, 10, 5, 8, 0, 0)

    def _regs(self, contagens):
        return [
            Registro(self.t0 + timedelta(seconds=6 * i), "INFO", "PT101", {"contagens": float(c)})
            for i, c in enumerate(contagens)
        ]

    def test_rejeita_incerteza_sistematica_negativa(self):
        """Incerteza sistematica negativa deve levantar ValueError."""
        regs = self._regs([100, 101, 99, 100])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", self.curva, u_sistematica=-0.1)

    def test_rejeita_serie_constante_com_mad_zero(self):
        """Leituras identicas produzem MAD nula e levantam ValueError."""
        regs = self._regs([500, 500, 500, 500])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", self.curva)

    def test_rejeita_menos_de_duas_validas_ou_fora_do_dominio(self):
        """Levanta ValueError se restar menos de 2 validas ou houver ponto fora do dominio."""
        regs_espurias = self._regs([100, 100, 101, 900, 1200, 1500])
        with self.assertRaises(ValueError):
            medir(regs_espurias, "PT101", self.curva, limiar=0.5)
        regs_fora = self._regs([100, 101, 5000])
        with self.assertRaises(ValueError):
            medir(regs_fora, "PT101", self.curva)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

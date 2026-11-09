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


def _registros(tag: str, contagens: list, chave: str = "contagens", inicio: int = 0) -> list:
    """Registros da `tag`, um a cada 6 s, com `chave` igual a cada valor de `contagens`."""
    t0 = datetime(2026, 10, 5, 8, 0, 0) + timedelta(seconds=6 * inicio)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {chave: float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan precisa mesmo compensar o arredondamento."""

    def test_kahan_milhao_de_pulsos_exato(self):
        """1 000 000 de parcelas de 0,1 L devem somar 100000.0 com Kahan (o ingênuo erra)."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
            ingenuo.adicionar(0.1)
        self.assertNotEqual(ingenuo.total, 100000.0)      # confirma que o caso é difícil
        self.assertAlmostEqual(kahan.total, 100000.0, delta=1e-9)

    def test_kahan_recupera_parcelas_pequenas(self):
        """Parcelas de 1e-16 somadas a 1.0 são perdidas pela soma ingênua, não pela de Kahan."""
        kahan = AcumuladorKahan()
        kahan.adicionar(1.0)
        for _ in range(1_000_000):
            kahan.adicionar(1e-16)
        self.assertGreater(kahan.total, 1.0)
        self.assertAlmostEqual(kahan.total, 1.0 + 1e-10, delta=1e-12)

    def test_kahan_igual_a_fsum(self):
        """Em 100 000 parcelas de 0,1, Kahan fica a no máximo 1 ulp da soma exata (fsum)."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 100_000)
        self.assertLessEqual(abs(kahan.total - math.fsum([0.1] * 100_000)),
                             math.ulp(10_000.0))


class TestMedirContrato(unittest.TestCase):
    """Issue #6: regras do contrato de `medir` que os testes de aceitação não verificam."""

    def setUp(self):
        self.contagens = [10, 11, 9, 10, 12, 11, 10, 9]

    def test_u_sistematica_negativa(self):
        """Uma incerteza sistemática negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", self.contagens), "PT101", IDENTIDADE, u_sistematica=-0.1)

    def test_mad_zero(self):
        """Leituras que dão MAD zero (mais da metade iguais) levantam ValueError."""
        regs = _registros("PT101", [10, 10, 10, 10, 10, 11])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)

    def test_indices_na_serie_da_tag(self):
        """Os índices das espúrias são posições na série da tag, ignorando outras tags e
        registros sem `contagens`."""
        regs = (_registros("PT101", [3000] * 5)
                + _registros("PT102", [0, 0], chave="alarme")
                + _registros("PT102", self.contagens[:3] + [900] + self.contagens[3:]))
        m = medir(regs, "PT102", IDENTIDADE)
        self.assertEqual(m.espurias, [3])
        self.assertEqual(m.n_validas, len(self.contagens))

    def test_limiar_controla_o_descarte(self):
        """Um limiar menor descarta mais leituras que o padrão (6)."""
        regs = _registros("PT101", self.contagens + [15])
        self.assertEqual(medir(regs, "PT101", IDENTIDADE).espurias, [])
        self.assertEqual(medir(regs, "PT101", IDENTIDADE, limiar=3.0).espurias, [8])

    def test_incerteza_sistematica_nao_diminui(self):
        """Com u_sistematica, a incerteza total é no mínimo a sistemática."""
        m = medir(_registros("PT101", self.contagens), "PT101", IDENTIDADE, u_sistematica=2.0)
        self.assertGreaterEqual(m.medida.incerteza, 2.0)

    def test_contagem_fora_do_dominio(self):
        """Contagem fora do domínio da curva: o ValueError da curva chega a quem chamou."""
        regs = _registros("PT101", self.contagens + [5000])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)

    def test_poucas_validas_depois_do_descarte(self):
        """Se sobrarem menos de 2 leituras válidas, levanta ValueError."""
        regs = _registros("PT101", [10, 11, 3000])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, limiar=0.1)


if __name__ == "__main__":
    unittest.main()
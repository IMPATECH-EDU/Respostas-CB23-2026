"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest
from datetime import datetime, timedelta

import numpy as np

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
CONTAGENS = [10, 11, 9, 10, 12, 11, 10, 9]


def _registros(tag: str, contagens: list[float]) -> list[Registro]:
    """Registros de leitura da `tag`, um a cada 6 s, com as contagens dadas."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestKahanRegressao(unittest.TestCase):
    """Issue #7: o AcumuladorKahan deve compensar o arredondamento."""

    def test_milhao_de_decimos(self) -> None:
        """1 000 000 parcelas de 0,1 somam exatamente 100000.0, como no relato da issue."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 1_000_000)
        self.assertEqual(kahan.total, 100_000.0)

    def test_parcela_pequena_nao_se_perde(self) -> None:
        """Dez parcelas de 1e-16 somadas a 1.0 aparecem no total, que a soma ingênua perde."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        for acumulador in (kahan, ingenuo):
            acumulador.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertEqual(ingenuo.total, 1.0)
        self.assertAlmostEqual(kahan.total, 1.0 + 1e-15, delta=1e-16)
        self.assertGreater(kahan.total, 1.0)

    def test_igual_a_fsum(self) -> None:
        """Com parcelas aleatórias, o Kahan concorda com math.fsum (soma exata) e o ingênuo não."""
        valores = np.random.default_rng(7).uniform(0.0, 1.0, 100_000).tolist()
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        for acumulador in (kahan, ingenuo):
            acumulador.adicionar_todos(valores)
        exata = math.fsum(valores)
        self.assertLess(abs(kahan.total - exata), abs(ingenuo.total - exata))


class TestMedirContrato(unittest.TestCase):
    """Issue #6: regras do contrato de medir que os testes de aceitação não verificam."""

    def test_u_sistematica_negativa(self) -> None:
        """Uma incerteza sistemática negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", CONTAGENS), "PT101", IDENTIDADE, u_sistematica=-0.1)

    def test_mad_zero(self) -> None:
        """Leituras quase todas iguais têm MAD zero, e o z robusto não está definido."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", [10, 10, 10, 10, 10, 11]), "PT101", IDENTIDADE)

    def test_indices_na_serie_da_tag(self) -> None:
        """Os índices das espúrias são posições na série da tag, e não no log inteiro."""
        regs = [r for par in zip(_registros("PT101", CONTAGENS + [500]),
                                 _registros("PT102", CONTAGENS * 2)) for r in par]
        self.assertEqual(medir(regs, "PT101", IDENTIDADE).espurias, [8])

    def test_espurias_em_ordem_crescente(self) -> None:
        """Várias espúrias, acima e abaixo da mediana, saem em ordem crescente."""
        contagens = [900] + CONTAGENS[:4] + [1500] + CONTAGENS[4:] + [0]
        medicao = medir(_registros("PT101", contagens), "PT101", IDENTIDADE)
        self.assertEqual(medicao.espurias, [0, 5, 10])
        self.assertEqual(medicao.n_validas, 8)

    def test_erro_da_curva_chega_a_quem_chamou(self) -> None:
        """Uma contagem fora do domínio da curva propaga o ValueError da própria curva."""
        curta = CurvaCalibracao([0.0, 10.0, 20.0], [0.0, 10.0, 20.0], "linear")
        with self.assertRaisesRegex(ValueError, "fora do domínio"):
            medir(_registros("PT101", CONTAGENS + [30]), "PT101", curta)


if __name__ == "__main__":
    unittest.main()

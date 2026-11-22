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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan não compensava o arredondamento."""

    def test_um_milhao_de_decimos_da_exatamente_cem_mil(self):
        """Um milhão de parcelas de 0,1 somadas com Kahan dão exatamente 100000.0."""
        acc = AcumuladorKahan()
        acc.adicionar_todos([0.1] * 1_000_000)
        self.assertEqual(acc.total, 100000.0)

    def test_kahan_erra_menos_que_a_soma_ingenua(self):
        """Com dez mil parcelas de 0,1, o erro de Kahan é menor que o da soma ingênua."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        kahan.adicionar_todos([0.1] * 10_000)
        ingenuo.adicionar_todos([0.1] * 10_000)
        self.assertLess(abs(kahan.total - 1000.0), abs(ingenuo.total - 1000.0))

    def test_parcela_pequena_depois_de_uma_grande_nao_se_perde(self):
        """1e16 + 1 + 1 com Kahan dá 1e16 + 2; a soma ingênua perde as duas parcelas de 1."""
        acc = AcumuladorKahan()
        acc.adicionar_todos([1e16, 1.0, 1.0])
        self.assertTrue(math.isclose(acc.total, 1e16 + 2, rel_tol=0, abs_tol=0.5))


class TestContratoMedir(unittest.TestCase):
    """Regras da docstring de medir que os testes de aceitação não verificam."""

    NORMAIS = [10, 11, 9, 10, 12, 11, 10, 9]

    def test_u_sistematica_negativa_levanta_value_error(self):
        """u_sistematica < 0 levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", self.NORMAIS), "PT101", IDENTIDADE, u_sistematica=-1.0)

    def test_mad_zero_levanta_value_error(self):
        """Leituras todas iguais têm MAD zero, e o z robusto não é definido: ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", [10] * 8), "PT101", IDENTIDADE)

    def test_espurias_em_ordem_crescente_de_posicao(self):
        """Duas espúrias, no começo e no meio, voltam como posições na série: [0, 4]."""
        contagens = [900] + self.NORMAIS[:3] + [800] + self.NORMAIS[3:]
        m = medir(_registros("PT101", contagens), "PT101", IDENTIDADE)
        self.assertEqual(m.espurias, [0, 4])
        self.assertEqual(m.n_validas, 8)

    def test_contagem_fora_do_dominio_da_curva_propaga_value_error(self):
        """Uma contagem fora do domínio da curva: o ValueError da curva chega a quem chamou."""
        curva = CurvaCalibracao([0.0, 50.0, 100.0], [0.0, 50.0, 100.0], "linear")
        with self.assertRaises(ValueError):
            medir(_registros("PT101", self.NORMAIS + [500]), "PT101", curva)


if __name__ == "__main__":
    unittest.main()

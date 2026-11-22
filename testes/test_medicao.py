"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import sys
import unittest

from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
T0 = datetime(2026, 10, 5, 8, 0, 0)


def _leituras(tag: str, contagens: list[float]) -> list[Registro]:
    """Registros de leitura da `tag`, um a cada 6 s, com as contagens dadas."""
    return [Registro(T0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertAlmostEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan deve compensar o erro de arredondamento."""

    def test_milhao_de_pulsos_de_0_1(self):
        """Um milhão de parcelas de 0,1 somam 100000 com erro desprezível (caso do relato)."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos(0.1 for _ in range(1_000_000))
        self.assertAlmostEqual(kahan.total, 100_000.0, delta=1e-9)

    def test_parcelas_pequenas_nao_somem(self):
        """Dez parcelas de 1e-16 somadas a 1,0 não se perdem, como na soma ingênua."""
        parcelas = [1.0] + [1e-16] * 10
        kahan = AcumuladorKahan()
        kahan.adicionar_todos(parcelas)
        # math.fsum é a soma corretamente arredondada; Kahan deve ficar a 1 ulp dela.
        self.assertAlmostEqual(kahan.total, math.fsum(parcelas), delta=sys.float_info.epsilon)

    def test_kahan_bem_melhor_que_ingenuo(self):
        """Com 10000 parcelas de 0,1, o erro do Kahan é mil vezes menor que o do ingênuo."""
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        parcelas = [0.1] * 10_000
        ingenuo.adicionar_todos(parcelas)
        kahan.adicionar_todos(parcelas)
        erro_ingenuo = abs(ingenuo.total - 1000.0)
        erro_kahan = abs(kahan.total - 1000.0)
        self.assertGreater(erro_ingenuo, 0.0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)


class TestContratoMedir(unittest.TestCase):
    """Issue #6: regras do contrato de medir que os testes de aceitação não verificam."""

    def setUp(self):
        self.contagens = [10, 11, 9, 10, 12, 11, 10, 9]

    def test_u_sistematica_negativa(self):
        """u_sistematica negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_leituras("PT101", self.contagens), "PT101", IDENTIDADE, u_sistematica=-0.1)

    def test_mad_zero(self):
        """Leituras com MAD zero (mais da metade iguais) levantam ValueError."""
        with self.assertRaises(ValueError):
            medir(_leituras("PT101", [50, 50, 50, 50, 51]), "PT101", IDENTIDADE)

    def test_erro_da_curva_chega_a_quem_chamou(self):
        """Uma contagem fora do domínio da curva propaga o ValueError da própria curva."""
        curva = CurvaCalibracao([0.0, 50.0, 100.0], [0.0, 50.0, 100.0], "linear")
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(_leituras("PT101", self.contagens + [500]), "PT101", curva)

    def test_indices_sao_posicoes_na_serie_da_tag(self):
        """Os índices das espúrias contam só as leituras da tag, não as linhas do log."""
        outras = _leituras("PT101", [10] * 8)
        alvo = _leituras("PT102", self.contagens[:3] + [900] + self.contagens[3:])
        alarme = Registro(T0, "ALARME", "PT102", {"evento": "pressao_alta"})
        intercalados = [r for par in zip(outras, alvo) for r in par] + [alvo[-1], alarme]
        m = medir(intercalados, "PT102", IDENTIDADE)
        self.assertEqual(m.espurias, [3])
        self.assertEqual(m.n_validas, 8)

    def test_incerteza_sem_parte_sistematica_e_o_erro_padrao(self):
        """Com u_sistematica = 0, a incerteza é só o erro padrão da média: s / sqrt(n)."""
        m = medir(_leituras("PT101", self.contagens), "PT101", IDENTIDADE)
        self.assertAlmostEqual(m.medida.incerteza, m.desvio / math.sqrt(8))


if __name__ == "__main__":
    unittest.main()

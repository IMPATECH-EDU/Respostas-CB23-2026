"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime, timedelta
from decimal import Decimal

from scipy import stats

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
    """Issue #7: o AcumuladorKahan precisa de fato compensar o arredondamento."""

    def test_dez_decimos_dao_exatamente_um(self):
        """Dez parcelas de 0,1: o ingênuo dá 0,999...9; Kahan deve dar o float 1.0 exato."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 10)
        self.assertEqual(kahan.total, 1.0)   # igualdade exata: é o que a compensação garante

    def test_parcelas_menores_que_o_ulp_nao_se_perdem(self):
        """1 + dez parcelas de 1e-16: o ingênuo fica em 1.0; Kahan recupera o 1e-15 somado."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertAlmostEqual(kahan.total - 1.0, 1e-15, delta=2.3e-16)

    def test_erro_muito_menor_que_o_ingenuo(self):
        """Em 100 000 parcelas de 0,1 L, o erro de Kahan é ao menos mil vezes menor."""
        n, ideal = 100_000, Decimal(10_000)
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        for acumulador in (ingenuo, kahan):
            acumulador.adicionar_todos([0.1] * n)
        erro_ingenuo = abs(Decimal(ingenuo.total) - ideal)
        erro_kahan = abs(Decimal(kahan.total) - ideal)
        self.assertGreater(erro_ingenuo, 0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)


def _leituras(tag: str, contagens: list, nivel: str = "INFO") -> list:
    """Registros da `tag` com as `contagens` dadas, um a cada 6 s."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), nivel, tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


#: Curva que devolve a própria contagem (kPa = contagem), para isolar a estatística.
_IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


class TestMedirContrato(unittest.TestCase):
    """Issue #6: regras do contrato de medir que os testes de aceitação não verificam."""

    def setUp(self):
        self.base = [200, 202, 199, 201, 198, 200, 203, 197]

    def test_u_sistematica_negativa(self):
        """u_sistematica < 0 é entrada inválida e levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_leituras("PT101", self.base), "PT101", _IDENTIDADE, u_sistematica=-0.1)

    def test_mad_zero(self):
        """Leituras todas iguais têm MAD zero: o z robusto não existe e medir recusa."""
        with self.assertRaises(ValueError):
            medir(_leituras("PT101", [500] * 6), "PT101", _IDENTIDADE)

    def test_erro_da_curva_chega_a_quem_chamou(self):
        """Uma contagem fora do domínio da curva propaga o ValueError da CurvaCalibracao."""
        curta = CurvaCalibracao([0.0, 100.0, 1000.0], [0.0, 100.0, 1000.0], "linear")
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(_leituras("PT101", self.base + [3000]), "PT101", curta)

    def test_indices_sao_posicoes_na_serie_da_tag(self):
        """Com outras tags e um alarme sem contagens no meio, o índice conta só as leituras."""
        regs = []
        for i, c in enumerate(self.base + [3000] + self.base):
            regs += _leituras("PT101", [50]) + _leituras("PT102", [c])
            if i == 3:
                regs.append(Registro(regs[-1].instante, "ALARME", "PT102", {"evento": "alto"}))
        m = medir(regs, "PT102", _IDENTIDADE)
        self.assertEqual(m.espurias, [8])
        self.assertEqual(m.n_validas, 16)

    def test_sem_incerteza_sistematica_sobra_o_erro_padrao(self):
        """Com u_sistematica = 0, a incerteza da medida é exatamente o erro padrão da média."""
        m = medir(_leituras("PT101", self.base), "PT101", _IDENTIDADE)
        self.assertAlmostEqual(m.medida.incerteza, float(stats.sem(self.base)))

    def test_limiar_menor_descarta_mais(self):
        """Baixar o limiar do z robusto passa a descartar leituras moderadamente afastadas."""
        dados = self.base + [215]
        self.assertEqual(medir(_leituras("PT101", dados), "PT101", _IDENTIDADE).espurias, [])
        self.assertEqual(medir(_leituras("PT101", dados), "PT101", _IDENTIDADE,
                               limiar=3.0).espurias, [8])


if __name__ == "__main__":
    unittest.main()

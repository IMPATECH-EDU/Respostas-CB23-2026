"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest
from datetime import datetime, timedelta
from decimal import Decimal

import numpy as np
from scipy import stats

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import altura_manometrica, medir

#: Curva que não muda nada (contagem = kPa), para os testes de medir ficarem legíveis.
IGUAL = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def _leituras(tag: str, contagens: list, inicio: int = 0) -> list:
    """Registros INFO de `tag` com as contagens dadas, um a cada 6 s a partir de `inicio`."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * (inicio + i)), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan precisa recuperar o que o arredondamento da soma perde."""

    def _kahan(self, parcelas):
        """Total de `parcelas` somadas uma a uma pelo AcumuladorKahan."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos(parcelas)
        return acumulador.total

    def test_milhao_de_pulsos_da_exatamente_cem_mil(self):
        """1 000 000 parcelas de 0,1 L somam exatamente 100000.0, como no relato da issue."""
        self.assertEqual(self._kahan([0.1] * 1_000_000), 100000.0)   # igualdade exata é o ponto

    def test_parcelas_menores_que_o_espacamento_nao_somem(self):
        """1e16 + dez parcelas de 1.0: cada uma some sozinha (espaçamento 2), mas juntas não."""
        self.assertEqual(self._kahan([1e16] + [1.0] * 10), 1e16 + 10)   # 1e16 + 10 é representável

    def test_dez_decimos_dao_um(self):
        """Dez parcelas de 0,1 dão 1.0 exato, e não 0.9999999999999999 como na soma direta."""
        self.assertEqual(self._kahan([0.1] * 10), 1.0)

    def test_erro_muito_menor_que_o_da_soma_ingenua(self):
        """Em 10 000 parcelas de 0,1, o erro do Kahan é pelo menos 1000 vezes menor que o ingênuo."""
        ingenuo = AcumuladorIngenuo()
        ingenuo.adicionar_todos([0.1] * 10_000)
        exato = Decimal(1000)
        erro_ingenuo = abs(Decimal(ingenuo.total) - exato)
        erro_kahan = abs(Decimal(self._kahan([0.1] * 10_000)) - exato)
        self.assertGreater(erro_ingenuo, 0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)




class TestContratoMedir(unittest.TestCase):
    """Issue #6: regras da docstring de medir que os testes de aceitação não verificam."""

    def setUp(self):
        self.normais = [100, 102, 98, 101, 99, 100, 103, 97]

    def test_u_sistematica_negativa(self):
        """u_sistematica < 0 é entrada inválida: ValueError, antes de qualquer conta."""
        with self.assertRaises(ValueError):
            medir(_leituras("PT101", self.normais), "PT101", IGUAL, u_sistematica=-0.1)

    def test_mad_zero(self):
        """Leituras quase todas iguais têm MAD zero: o z robusto não existe, ValueError."""
        with self.assertRaises(ValueError):
            medir(_leituras("PT101", [500] * 7 + [501]), "PT101", IGUAL)

    def test_erro_da_curva_chega_a_quem_chamou(self):
        """Uma contagem fora do domínio da curva faz o ValueError da curva subir até o teste."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(_leituras("PT101", self.normais + [5000]), "PT101", IGUAL)

    def test_indices_sao_posicoes_na_serie_da_tag(self):
        """Com outras tags e um alarme no meio do log, o índice da espúria conta só as leituras da tag."""
        log = []
        for i, c in enumerate(self.normais + [900] + self.normais):
            log += _leituras("PT101", [3000], i) + _leituras("PT102", [c], i)
            if i == 3:
                log.append(Registro(log[-1].instante, "ALARME", "PT102",
                                    {"evento": "pressao_alta", "limite": 2000.0}))
        m = medir(log, "PT102", IGUAL)
        self.assertEqual(m.espurias, [8])
        self.assertEqual(m.n_validas, 16)

    def test_limiar_decide_o_que_e_espuria(self):
        """Com limiar enorme nada é descartado; com o padrão, o 250 é descartado."""
        regs = _leituras("PT101", self.normais + [250])
        self.assertEqual(medir(regs, "PT101", IGUAL, limiar=1e9).espurias, [])
        self.assertEqual(medir(regs, "PT101", IGUAL).espurias, [8])

    def test_incerteza_sem_parte_sistematica_e_o_erro_padrao(self):
        """Com u_sistematica = 0, a incerteza da medida é só o erro padrão das válidas."""
        m = medir(_leituras("PT101", self.normais), "PT101", IGUAL)
        self.assertAlmostEqual(m.medida.incerteza, float(stats.sem(self.normais)))

    def test_altura_propaga_a_incerteza_da_massa_especifica(self):
        """Mesmo sem ruído sistemático, a altura tem incerteza: a de rho = 998 ± 1 entra na conta."""
        regs = _leituras("PT101", self.normais) + _leituras("PT102", [c + 1000 for c in self.normais])
        h = altura_manometrica(regs, IGUAL, u_sistematica=0.0)
        self.assertAlmostEqual(h.valor, 1000.0 * 1000 / (998.0 * 9.81))
        u_so_leituras = math.hypot(stats.sem(self.normais), stats.sem(self.normais)) * 1000 / (998.0 * 9.81)
        self.assertGreater(h.incerteza, u_so_leituras)


if __name__ == "__main__":
    unittest.main()

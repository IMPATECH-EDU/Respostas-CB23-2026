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

#: Curva que devolve a própria contagem, para os testes de `medir` checarem só a estatística.
_IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def _leituras(tag: str, contagens: list, inicio: int = 0) -> list:
    """Registros INFO da `tag` com as `contagens` dadas, um a cada 6 s a partir de `inicio`."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * (inicio + i)), "INFO", tag,
                     {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# ---------------------------------------------------------------------------------------
# Issue #7: regressão do AcumuladorKahan (escritos antes da correção; falham no original)
# ---------------------------------------------------------------------------------------
class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: a soma de Kahan precisa compensar o arredondamento de verdade.

    Aqui a igualdade exata é o que se quer testar: a soma compensada deve dar o float
    correto, e não um valor apenas próximo.
    """

    def test_dez_parcelas_de_um_decimo_dao_exatamente_um(self):
        """0,1 somado 10 vezes dá 1.0 exato (a soma direta dá 0.9999999999999999)."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 10)
        self.assertEqual(kahan.total, 1.0)

    def test_parcelas_pequenas_nao_somem(self):
        """Dez parcelas de 1e-16 somadas a 1.0 aparecem no total, como em math.fsum."""
        valores = [1.0] + [1e-16] * 10
        kahan = AcumuladorKahan()
        kahan.adicionar_todos(valores)
        self.assertEqual(kahan.total, math.fsum(valores))
        self.assertGreater(kahan.total, 1.0)

    def test_um_milhao_de_pulsos(self):
        """O caso do relato: 1 000 000 de pulsos de 0,1 L totalizam 100000.0 exatos."""
        kahan = AcumuladorKahan()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
        self.assertEqual(kahan.total, 100000.0)


# ---------------------------------------------------------------------------------------
# Issue #6: regras do contrato de medir que os testes de aceitação não verificam
# ---------------------------------------------------------------------------------------
class TestMedirContrato(unittest.TestCase):
    """Issue #6: casos de medir fora dos testes de aceitação."""

    def setUp(self):
        self.contagens = [100, 102, 98, 101, 99, 100, 103, 97]

    def test_u_sistematica_negativa(self):
        """u_sistematica < 0 levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_leituras("PT101", self.contagens), "PT101", _IDENTIDADE, u_sistematica=-0.1)

    def test_mad_zero(self):
        """Com todas as leituras iguais, a MAD é zero e medir levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_leituras("PT101", [500] * 6), "PT101", _IDENTIDADE)

    def test_indices_sao_posicoes_na_serie_da_tag(self):
        """Os índices de `espurias` contam só as leituras da tag, e não a lista de registros."""
        alarme = Registro(datetime(2026, 10, 5, 8, 0, 3), "ALARME", "PT102", {"evento": "alta"})
        regs = (_leituras("PT101", [10] * 5) + [alarme]
                + _leituras("PT102", self.contagens[:3] + [3000] + self.contagens[3:]))
        m = medir(regs, "PT102", _IDENTIDADE)
        self.assertEqual(m.espurias, [3])
        self.assertEqual(m.n_validas, len(self.contagens))

    def test_desvio_so_com_as_validas(self):
        """O desvio (ddof=1) ignora a leitura espúria."""
        m = medir(_leituras("PT101", self.contagens + [4000]), "PT101", _IDENTIDADE)
        self.assertTrue(math.isclose(m.desvio, float(np.std(self.contagens, ddof=1))))

    def test_erro_da_curva_chega_a_quem_chamou(self):
        """Uma contagem fora do domínio da curva levanta o ValueError da própria curva."""
        curta = CurvaCalibracao([0.0, 100.0, 200.0], [0.0, 100.0, 200.0], "linear")
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(_leituras("PT101", self.contagens + [250]), "PT101", curta)


if __name__ == "__main__":
    unittest.main()
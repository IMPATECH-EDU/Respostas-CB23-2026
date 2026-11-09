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


def registros(tag: str, contagens: list) -> list:
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

class TestAcumuladorKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan deve compensar o arredondamento (igualdade exata de propósito)."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorKahan().total, 0.0)

    def test_com_100_000_parcelas(self):
        """A Soma de 100_000 parcelas de 0.1 é 10_000."""
        acumulador = AcumuladorKahan()
        for _ in range(100_000):
            acumulador.adicionar(0.1)
        self.assertEqual(acumulador.total, 10_000.0)

    def test_com_10_000_000_parcelas(self):
        """A Soma de 10_000_000 parcelas de 0.1 é 1_000_000."""
        acumulador = AcumuladorKahan()
        for _ in range(10_000_000):
            acumulador.adicionar(0.1)
        self.assertEqual(acumulador.total, 1_000_000.0)

    def test_parcelas_pequenas_nao_somem(self):
        """1.0 seguido de 10 parcelas de 1e-16 dá o mesmo que math.fsum, e não 1.0."""
        valores = [1.0] + [1e-16] * 10
        acumulador = AcumuladorKahan()
        for x in valores:
            acumulador.adicionar(x)
        self.assertEqual(acumulador.total, math.fsum(valores))

    def test_parcelas_diferentes(self):
        """A Soma de 1000 vezes 0.1, 0.2 e 0.3 dá o mesmo que math.fsum."""
        valores = [0.1, 0.2, 0.3] * 1000
        acumulador = AcumuladorKahan()
        for x in valores:
            acumulador.adicionar(x)
        self.assertEqual(acumulador.total, math.fsum(valores))


class TestMedir(unittest.TestCase):
    """Issue #6: regras do contrato de medir que os testes de aceitação não verificam."""

    def setUp(self):
        self.contagens = [10, 11, 9, 10, 12, 11, 10, 9]

    def test_u_sistematica_negativa(self):
        """Uma u_sistematica negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(registros("PT101", self.contagens), "PT101", IDENTIDADE, u_sistematica=-0.1)

    def test_mad_zero(self):
        """Leituras todas iguais dão MAD zero e levantam ValueError."""
        with self.assertRaises(ValueError):
            medir(registros("PT101", [10] * 8), "PT101", IDENTIDADE)

    def test_contagem_fora_do_dominio(self):
        """Uma contagem fora do domínio da curva levanta o ValueError da própria curva."""
        with self.assertRaises(ValueError):
            medir(registros("PT101", self.contagens + [5000]), "PT101", IDENTIDADE)

    def test_indice_da_espuria_e_na_serie_da_tag(self):
        """Com 5 registros de PT101 antes, a espúria de PT102 continua com índice 8, e não 13."""
        regs = registros("PT101", [100] * 5) + registros("PT102", self.contagens + [500])
        self.assertEqual(medir(regs, "PT102", IDENTIDADE).espurias, [8])

    def test_ignora_alarmes_sem_contagens(self):
        """Um alarme da tag, sem a chave contagens, não entra na medição."""
        alarme = Registro(datetime(2026, 10, 5, 9, 0, 0), "ALARME", "PT102",
                          {"evento": "pressao_alta"})
        m = medir(registros("PT102", self.contagens) + [alarme], "PT102", IDENTIDADE)
        self.assertEqual(m.n_validas, 8)
        self.assertAlmostEqual(m.medida.valor, float(np.mean(self.contagens)))


if __name__ == "__main__":
    unittest.main()
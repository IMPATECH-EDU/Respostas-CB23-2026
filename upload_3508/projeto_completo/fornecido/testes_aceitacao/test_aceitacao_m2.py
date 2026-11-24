"""Testes de aceitação do Marco 2 (código fornecido; NÃO ALTERE).

Conferem o contrato público de `elevatoria/medicao.py` (issue #6) e documentam o uso do
código que já existia: `elevatoria/calibracao.py`, `elevatoria/acumuladores.py` e
`fornecido/medida.py`. Passar em todos eles é necessário, mas não basta: eles não cobrem
todos os casos (veja a issue #7). Os seus próprios testes ficam em `testes/`.
"""
import math
import unittest
from datetime import datetime, timedelta

import numpy as np
from scipy import stats

from elevatoria.acumuladores import (Acumulador, AcumuladorIngenuo, AcumuladorInteiro,
                                     AcumuladorKahan)
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import Medicao, altura_manometrica, medir
from fornecido.medida import Medida

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def registros(tag: str, contagens: list) -> list:
    """Registros de leitura da `tag`, um a cada 6 s, com as contagens dadas."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestMedir(unittest.TestCase):
    """Issue #6: medir."""

    def setUp(self):
        self.contagens = [10, 11, 9, 10, 12, 11, 10, 9]

    def test_media_e_incerteza(self):
        m = medir(registros("PT101", self.contagens), "PT101", IDENTIDADE, u_sistematica=2.0)
        self.assertIsInstance(m, Medicao)
        self.assertIsInstance(m.medida, Medida)
        self.assertEqual((m.tag, m.n_validas, m.espurias), ("PT101", 8, []))
        self.assertAlmostEqual(m.medida.valor, float(np.mean(self.contagens)))
        self.assertAlmostEqual(m.desvio, float(np.std(self.contagens, ddof=1)))
        self.assertAlmostEqual(m.medida.incerteza,
                               math.hypot(float(stats.sem(self.contagens)), 2.0))

    def test_descarta_espurias(self):
        m = medir(registros("PT102", self.contagens + [500]), "PT102", IDENTIDADE)
        self.assertEqual(m.espurias, [8])
        self.assertEqual(m.n_validas, 8)
        self.assertAlmostEqual(m.medida.valor, float(np.mean(self.contagens)))

    def test_usa_a_curva(self):
        dobro = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 4000.0, 8190.0], "linear")
        m = medir(registros("PT101", self.contagens), "PT101", dobro)
        self.assertAlmostEqual(m.medida.valor, 2 * float(np.mean(self.contagens)))

    def test_so_a_tag_pedida(self):
        regs = registros("PT101", self.contagens) + registros("PT102", [3000] * 8)
        self.assertEqual(medir(regs, "PT101", IDENTIDADE).n_validas, 8)

    def test_poucas_leituras(self):
        for regs in [registros("PT101", self.contagens), registros("PT102", [10])]:
            with self.subTest(n=len(regs)), self.assertRaises(ValueError):
                medir(regs, "PT102", IDENTIDADE)


class TestAlturaManometrica(unittest.TestCase):
    """Issue #6: altura_manometrica."""

    def test_valor_e_incerteza(self):
        succao = [100, 101, 99, 100, 102, 98, 100, 100]
        recalque = [1100, 1101, 1099, 1100, 1102, 1098, 1100, 1100]
        regs = registros("PT101", succao) + registros("PT102", recalque)
        altura = altura_manometrica(regs, IDENTIDADE, u_sistematica=1.5)
        self.assertIsInstance(altura, Medida)
        self.assertAlmostEqual(altura.valor, 1000.0 * 1000 / (998.0 * 9.81))
        self.assertGreater(altura.incerteza, 0.0)
        self.assertLess(altura.incerteza_relativa, 0.01)


class TestCodigoExistente(unittest.TestCase):
    """Código que já existia na base: exemplos de uso."""

    def test_curva(self):
        curva = CurvaCalibracao([0.0, 1.0, 2.0, 3.0, 4.0], [0.0, 1.0, 4.0, 9.0, 16.0], "spline")
        self.assertAlmostEqual(curva(2.5), 6.25)
        self.assertIsInstance(curva(np.array([0.5, 2.5])), np.ndarray)
        self.assertAlmostEqual(curva.derivada(2.0), 4.0)
        with self.assertRaises(ValueError):
            curva(4.5)

    def test_acumuladores(self):
        with self.assertRaises(TypeError):
            Acumulador()
        for acumulador in [AcumuladorIngenuo(), AcumuladorKahan(), AcumuladorInteiro(10)]:
            with self.subTest(acumulador=type(acumulador).__name__):
                acumulador.adicionar_todos([0.1] * 10)
                self.assertTrue(math.isclose(acumulador.total, 1.0))

    def test_medida(self):
        m = Medida(10, 0.3) + Medida(20, 0.4)
        self.assertAlmostEqual(m.incerteza, 0.5)
        self.assertAlmostEqual((2 * Medida(5, 0.1)).incerteza, 0.2)
        self.assertEqual(str(Medida(12.3456, 0.321)), "12.35 ± 0.32")


if __name__ == "__main__":
    unittest.main()

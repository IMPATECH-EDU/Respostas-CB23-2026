"""Testes de aceitação do Marco 4 (código fornecido; NÃO ALTERE).

Conferem o contrato público de `elevatoria/dia.py` (issue #10) e documentam o uso do código
que já existia: `elevatoria/integracao.py` e `fornecido/energia.py`. Passar em todos eles é
necessário, mas não basta: eles não cobrem todos os casos (veja a issue #11). Os seus
próprios testes ficam em `testes/`.
"""
import unittest

import numpy as np

from elevatoria.dia import ResumoDia, ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Integrador, Simpson, Trapezio
from fornecido.energia import potencia_eletrica, vazao_registrada

# Um dia sintético, com leituras a cada 1,5 h (os limites 0, 18, 21 e 24 h estão na malha).
T = np.arange(0.0, 24.0 + 1e-9, 1.5)


class TestAjustarPolinomio(unittest.TestCase):
    """Issue #10: ajustar_polinomio."""

    def test_reta_exata(self):
        coef = ajustar_polinomio([0.0, 1.0, 2.0, 3.0], [1.0, 3.0, 5.0, 7.0], 1)
        self.assertTrue(np.allclose(coef, [1.0, 2.0]))

    def test_igual_ao_polyfit(self):
        rng = np.random.default_rng(1)
        x = np.linspace(0.0, 100.0, 11)
        y = 45.0 - 0.0022 * x ** 2 + rng.normal(0.0, 0.15, x.size)
        coef = ajustar_polinomio(x, y, 2)
        self.assertEqual(len(coef), 3)
        self.assertTrue(np.allclose(coef, np.polyfit(x, y, 2)[::-1]))   # polyfit: ordem decrescente

    def test_poucos_pontos(self):
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0], [1.0, 2.0], 2)


class TestDiaDeOperacao(unittest.TestCase):
    """Issue #10: dia_de_operacao."""

    def test_vazao_constante(self):
        vazao = np.full(T.size, 50.0)
        resumo = dia_de_operacao(T, vazao, [40.0], [0.8], Trapezio())
        potencia = 998.0 * 9.81 * 0.050 * 40.0 / (1000.0 * 0.8)
        self.assertIsInstance(resumo, ResumoDia)
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * 50.0 * 24.0)
        self.assertAlmostEqual(resumo.energia_kwh, potencia * 24.0)
        self.assertTrue(np.allclose(resumo.custo_por_faixa,
                                    [potencia * 18 * 0.50, potencia * 3 * 1.50, potencia * 3 * 0.50]))
        self.assertAlmostEqual(resumo.custo_reais, potencia * 15.0)

    def test_vazao_variavel_e_curvas(self):
        vazao = 40.0 + T                                   # de 40 a 64 L/s
        resumo = dia_de_operacao(T, vazao, [45.0, 0.0, -0.0022], [0.6, 0.002], Trapezio())
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * (40.0 * 24.0 + 24.0 ** 2 / 2))
        potencia = potencia_eletrica(vazao, 45.0 - 0.0022 * vazao ** 2, 0.6 + 0.002 * vazao)
        self.assertAlmostEqual(resumo.energia_kwh, Trapezio().integrar_tabela(T, potencia))

    def test_tamanhos_diferentes(self):
        with self.assertRaises(ValueError):
            dia_de_operacao(T, np.full(T.size - 1, 50.0), [40.0], [0.8], Trapezio())


class TestCodigoExistente(unittest.TestCase):
    """Código que já existia na base: exemplos de uso."""

    def test_integradores(self):
        with self.assertRaises(TypeError):
            Integrador()
        cubica = lambda x: x ** 3 - 2 * x                  # ∫ de 0 a 2 = 0
        self.assertAlmostEqual(Simpson().integrar(cubica, 0.0, 2.0, 4), 0.0)
        self.assertAlmostEqual(Trapezio().integrar(lambda x: 3 * x + 1, 0.0, 2.0, 5), 8.0)
        x = np.linspace(0.0, 2.0, 9)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 8.0)
        self.assertAlmostEqual(Simpson().integrar_tabela(x, x ** 2), 8.0 / 3.0)
        with self.assertRaises(ValueError):
            Simpson().integrar(cubica, 0.0, 2.0, 3)
        with self.assertRaises(ValueError):
            Simpson().integrar_tabela([0.0, 1.0, 3.0], [0.0, 1.0, 3.0])

    def test_energia(self):
        self.assertAlmostEqual(float(potencia_eletrica(50.0, 40.0, 0.8)), 24.47595)
        t, q = vazao_registrada(123456)
        self.assertEqual((t.size, q.size), (89, 89))
        for limite in (0.0, 18.0, 21.0, 24.0):
            self.assertIn(limite, t)


if __name__ == "__main__":
    unittest.main()

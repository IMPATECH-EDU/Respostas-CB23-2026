"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import potencia_eletrica


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: o trapézio usava o primeiro passo em toda a malha."""

    def test_malha_irregular_com_reta(self):
        """x = 0, 1, 3 com y = x dá área 4,5 (antes dava 2,5)."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [0.0, 1.0, 3.0]), 4.5)

    def test_lacuna_no_registro(self):
        """Vazão 10 em x = 0, 1, 2, 4 integra 40, apesar da lacuna de 2 a 4."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 2.0, 4.0], [10.0] * 4), 40.0)

    def test_reta_em_malha_aleatoria(self):
        """Em pontos sorteados, a integral de 2x + 1 em [0, 4] é 20."""
        rng = np.random.default_rng(7)
        x = np.sort(np.concatenate(([0.0, 4.0], rng.uniform(0.0, 4.0, 20))))
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2.0 * x + 1.0), 20.0)

    def test_volume_do_dia_com_falhas(self):
        """Vazão constante com 8 leituras perdidas ainda dá 3,6 · 50 · 24 m³."""
        t = np.arange(0.0, 24.0 + 1e-9, 0.25)
        manter = np.setdiff1d(np.arange(t.size), [3, 10, 11, 25, 40, 41, 60, 90])
        volume = 3.6 * Trapezio().integrar_tabela(t[manter], np.full(manter.size, 50.0))
        self.assertAlmostEqual(volume, 3.6 * 50.0 * 24.0)


class TestAjustarPolinomio(unittest.TestCase):
    """Issue #10: ajustar_polinomio."""

    def test_recupera_parabola_longe_da_origem(self):
        """Com x de 100 a 140, recupera os coeficientes de 3 + 0,5x - 0,01x²."""
        x = np.linspace(100.0, 140.0, 25)
        coef = ajustar_polinomio(x, 3.0 + 0.5 * x - 0.01 * x ** 2, 2)
        self.assertTrue(np.allclose(coef, [3.0, 0.5, -0.01], rtol=1e-6))

    def test_entradas_invalidas(self):
        """Tamanhos diferentes, grau negativo, poucos pontos e valores não finitos levantam ValueError."""
        x = np.arange(5.0)
        casos = [(x, x[:4], 1), (x, x, -1), (x[:2], x[:2], 2), (x, np.where(x == 2, np.nan, x), 1),
                 (x.reshape(5, 1), x, 1)]
        for xi, yi, grau in casos:
            with self.subTest(grau=grau, n=len(xi)), self.assertRaises(ValueError):
                ajustar_polinomio(xi, yi, grau)

    def test_reta_por_dois_pontos(self):
        """Grau 1 com dois pontos passa pelos dois."""
        coef = ajustar_polinomio(np.array([0.0, 2.0]), np.array([1.0, 5.0]), 1)
        self.assertTrue(np.allclose(coef, [1.0, 2.0]))


class TestDiaDeOperacao(unittest.TestCase):
    """Issue #10: dia_de_operacao."""

    T = np.arange(0.0, 24.0 + 1e-9, 0.5)

    def test_regime_constante_bate_com_a_conta_a_mao(self):
        """Q, H e rendimento constantes: energia = P · 24 e custo = P · 15 (0,50·18 + 1,50·3 + 0,50·3)."""
        vazao = np.full(self.T.size, 50.0)
        resumo = dia_de_operacao(self.T, vazao, np.array([40.0]), np.array([0.7]), Trapezio())
        p = float(potencia_eletrica(np.array([50.0]), np.array([40.0]), np.array([0.7]))[0])
        self.assertAlmostEqual(resumo.energia_kwh, 24.0 * p)
        self.assertAlmostEqual(resumo.custo_reais, 15.0 * p)
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * 50.0 * 24.0)

    def test_custo_e_a_soma_das_faixas(self):
        """`custo_reais` é a soma de `custo_por_faixa`, com uma entrada por faixa."""
        vazao = 40.0 + 10.0 * np.sin(self.T / 4.0)
        resumo = dia_de_operacao(self.T, vazao, np.array([40.0, -0.01]), np.array([0.5, 0.01]),
                                 Trapezio())
        self.assertEqual(len(resumo.custo_por_faixa), 3)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))

    def test_limite_de_faixa_ausente(self):
        """Sem 18 h entre os instantes de t, levanta ValueError."""
        t = np.concatenate((np.arange(0.0, 17.5, 0.5), np.arange(18.25, 24.0 + 1e-9, 0.25)))
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), np.array([40.0]), np.array([0.7]), Trapezio())

    def test_rendimento_nao_positivo(self):
        """Rendimento zero levanta ValueError."""
        with self.assertRaises(ValueError):
            dia_de_operacao(self.T, np.full(self.T.size, 50.0), np.array([40.0]), np.array([0.0]),
                            Trapezio())

    def test_tamanhos_diferentes(self):
        """t e vazao com tamanhos diferentes levantam ValueError."""
        with self.assertRaises(ValueError):
            dia_de_operacao(self.T, np.full(self.T.size - 1, 50.0), np.array([40.0]),
                            np.array([0.7]), Trapezio())


if __name__ == "__main__":
    unittest.main()

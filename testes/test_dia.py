"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import FAIXAS_TARIFARIAS

T = np.arange(0.0, 24.01, 1.5)   # 17 instantes, de 0 h a 24 h; inclui 18 h e 21 h


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioMalhaIrregular(unittest.TestCase):
    """Testes de regressão da issue #11: o trapézio de tabela precisa usar a largura de cada passo."""

    def test_reta_em_malha_irregular(self):
        """Issue #11: ∫ x dx em x = [0, 1, 3] vale 4,5 (passos de 1 e de 2)."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x), 4.5)

    def test_constante_com_leitura_perdida(self):
        """Issue #11: ∫ 2 dx em [0, 1], com a leitura de 0,5 perdida, vale 2."""
        x = np.array([0.0, 0.25, 0.75, 1.0])
        y = np.full(4, 2.0)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 2.0)

    def test_parabola_em_malha_irregular(self):
        """Issue #11: trapézios de x² em x = [0, 0,25, 0,75, 1] somam 0,359375."""
        x = np.array([0.0, 0.25, 0.75, 1.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x ** 2), 0.359375)


class TestAjustarPolinomio(unittest.TestCase):
    """Testes de `ajustar_polinomio` (issue #10)."""

    def test_recupera_uma_parabola_exata(self):
        """ajustar_polinomio: 1 + 2x + 3x² é recuperada, em ordem crescente, de 5 pontos exatos."""
        x = np.arange(5.0)
        coef = ajustar_polinomio(x, 1.0 + 2.0 * x + 3.0 * x ** 2, 2)
        self.assertTrue(np.allclose(coef, [1.0, 2.0, 3.0]))

    def test_grau_zero_e_a_media(self):
        """ajustar_polinomio: o ajuste de grau 0 é a média dos y."""
        coef = ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 6.0], 0)
        self.assertTrue(np.allclose(coef, [3.0]))

    def test_grau_negativo(self):
        """ajustar_polinomio: grau negativo levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_tamanhos_diferentes(self):
        """ajustar_polinomio: x e y com tamanhos diferentes levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)


class TestDiaDeOperacao(unittest.TestCase):
    """Testes de `dia_de_operacao` (issue #10), com vazão constante de 50 L/s."""

    def setUp(self):
        self.vazao = np.full(T.size, 50.0)
        # altura constante de 40 m e rendimento constante de 0,8
        self.resumo = dia_de_operacao(T, self.vazao, [40.0], [0.8], Trapezio())
        self.potencia = 998.0 * 9.81 * (50.0 / 1000.0) * 40.0 / (1000.0 * 0.8)   # kW

    def test_custo_faixa_por_faixa(self):
        """dia_de_operacao: o custo de cada faixa é tarifa · potência · duração da faixa."""
        esperado = [tarifa * self.potencia * (fim - inicio)
                    for inicio, fim, tarifa in FAIXAS_TARIFARIAS]
        for obtido, previsto in zip(self.resumo.custo_por_faixa, esperado):
            self.assertAlmostEqual(obtido, previsto)

    def test_custo_total_e_a_soma_das_faixas(self):
        """dia_de_operacao: custo_reais é a soma de custo_por_faixa."""
        self.assertAlmostEqual(self.resumo.custo_reais, sum(self.resumo.custo_por_faixa))

    def test_volume_e_energia(self):
        """dia_de_operacao: 50 L/s por 24 h dão 4320 m³, e a energia é potência · 24 h."""
        self.assertAlmostEqual(self.resumo.volume_m3, 3.6 * 50.0 * 24.0)
        self.assertAlmostEqual(self.resumo.energia_kwh, self.potencia * 24.0)

    def test_limite_de_faixa_ausente(self):
        """dia_de_operacao: sem a leitura de 18 h, levanta ValueError."""
        t = np.delete(T, np.where(T == 18.0))
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()
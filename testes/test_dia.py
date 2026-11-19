"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: Trapezio.integrar_tabela deve aceitar malha não uniforme."""

    def test_reta_em_malha_irregular(self):
        """∫ x dx de 0 a 3 com pontos 0, 1 e 3 dá 4,5 (o trapézio é exato para retas)."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x), 4.5)

    def test_constante_da_o_comprimento_do_intervalo(self):
        """Integrar a constante 1 numa malha irregular dá o comprimento do intervalo."""
        x = np.array([0.0, 0.25, 0.75, 1.0, 2.0, 2.5])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.ones_like(x)), 2.5)

    def test_reta_na_malha_do_registro_com_falhas(self):
        """Na malha real do dia (com leituras perdidas), ∫ (2t + 1) dt de 0 a 24 dá 600."""
        t, _ = vazao_registrada(3507)
        self.assertGreater(np.ptp(np.diff(t)), 0.0)   # a malha é mesmo irregular
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, 2 * t + 1), 600.0)


class TestContratoAjustarPolinomio(unittest.TestCase):
    """Issue #10: regras de ajustar_polinomio que os testes de aceitação não verificam."""

    def test_grau_negativo(self):
        """grau < 0 levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_tamanhos_diferentes(self):
        """x e y de tamanhos diferentes levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0, 3.0], [1.0, 2.0, 3.0], 1)

    def test_coeficientes_em_ordem_crescente(self):
        """Com pontos exatos de 2 - x + 0,5x², os coeficientes saem como [2, -1, 0,5]."""
        x = np.linspace(-3.0, 5.0, 9)
        coef = ajustar_polinomio(x, 2.0 - x + 0.5 * x ** 2, 2)
        self.assertTrue(np.allclose(coef, [2.0, -1.0, 0.5]))

    def test_grau_zero_e_a_media(self):
        """O polinômio de grau 0 de mínimos quadrados é a média dos y."""
        y = np.array([3.0, 5.0, 10.0, 2.0])
        coef = ajustar_polinomio(np.arange(4.0), y, 0)
        self.assertEqual(len(coef), 1)
        self.assertAlmostEqual(coef[0], y.mean())


class TestContratoDiaDeOperacao(unittest.TestCase):
    """Issue #10: regras de dia_de_operacao que os testes de aceitação não verificam."""

    def setUp(self):
        self.t = np.arange(0.0, 24.0 + 1e-9, 1.5)   # 17 pontos, uniforme, com 0, 18, 21 e 24

    def test_falta_um_limite_de_faixa(self):
        """Sem a leitura das 21 h entre os instantes, levanta ValueError."""
        t = self.t[self.t != 21.0]
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_custo_total_e_a_soma_das_faixas(self):
        """custo_reais é a soma de custo_por_faixa, com uma parcela por faixa tarifária."""
        resumo = dia_de_operacao(self.t, 40.0 + self.t, [45.0, 0.0, -0.0022], [0.6, 0.002],
                                 Trapezio())
        self.assertEqual(len(resumo.custo_por_faixa), 3)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))

    def test_usa_o_integrador_recebido(self):
        """Com Simpson, o volume de uma vazão quadrática no tempo é exato."""
        vazao = 40.0 + 0.1 * self.t ** 2
        resumo = dia_de_operacao(self.t, vazao, [40.0], [0.8], Simpson())
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * (40.0 * 24.0 + 0.1 * 24.0 ** 3 / 3))


if __name__ == "__main__":
    unittest.main()

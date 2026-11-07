"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import FAIXAS_TARIFARIAS, vazao_registrada


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioTabelaRegressao(unittest.TestCase):
    """Issue #11: integrar_tabela do trapézio em malha não uniforme."""

    def test_reta_em_malha_irregular_e_exata(self):
        """O trapézio integra uma reta exatamente, qualquer que seja o espaçamento."""
        x = np.array([0.0, 0.25, 0.5, 1.0, 1.25, 2.0])   # passos 0,25 e 0,5 e 0,75
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 8.0)

    def test_constante_da_comprimento_total(self):
        """y = 1 integra para x[-1] - x[0], mesmo com o primeiro passo diferente dos outros."""
        x = np.array([0.0, 1.0, 1.5, 2.0, 2.5])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.ones_like(x)), 2.5)

    def test_registro_com_falhas_igual_ao_np_trapezoid(self):
        """No registro real do dia (89 de 97 leituras), o resultado coincide com np.trapezoid."""
        t, q = vazao_registrada(123456)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, q), float(np.trapezoid(q, t)))


class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: regras de ajustar_polinomio que os testes de aceitação não verificam."""

    def test_entradas_invalidas(self):
        """Grau negativo, tamanhos diferentes e x 2D levantam ValueError."""
        casos = [([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1),
                 ([0.0, 1.0, 2.0], [1.0, 2.0], 1),
                 ([[0.0, 1.0], [2.0, 3.0]], [1.0, 2.0], 1)]
        for x, y, grau in casos:
            with self.subTest(x=x, y=y, grau=grau), self.assertRaises(ValueError):
                ajustar_polinomio(x, y, grau)

    def test_grau_zero_e_a_media(self):
        """O polinômio constante de mínimos quadrados é a média dos y."""
        coef = ajustar_polinomio([0.0, 1.0, 5.0, 9.0], [2.0, 4.0, 3.0, 7.0], 0)
        self.assertEqual(len(coef), 1)
        self.assertAlmostEqual(coef[0], 4.0)

    def test_pontos_iguais_ao_numero_de_coeficientes_interpola(self):
        """Com len(x) = grau + 1, o ajuste passa exatamente pelos pontos."""
        x = np.array([10.0, 40.0, 70.0, 100.0])
        y = np.array([44.8, 41.3, 34.1, 23.0])
        coef = ajustar_polinomio(x, y, 3)
        self.assertTrue(np.allclose(np.polynomial.polynomial.polyval(x, coef), y))


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: regras de dia_de_operacao que os testes de aceitação não verificam."""

    def setUp(self):
        self.t = np.arange(0.0, 24.0 + 1e-9, 1.5)

    def test_falta_limite_de_faixa(self):
        """Sem a leitura das 21 h, as faixas não podem ser integradas: ValueError."""
        t = self.t[~np.isclose(self.t, 21.0)]
        with self.assertRaisesRegex(ValueError, "21"):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_custo_total_e_a_soma_das_faixas(self):
        """custo_reais é a soma de custo_por_faixa, que tem uma entrada por faixa tarifária."""
        resumo = dia_de_operacao(self.t, 40.0 + self.t, [45.0, 0.0, -0.0022], [0.6, 0.002],
                                 Trapezio())
        self.assertEqual(len(resumo.custo_por_faixa), len(FAIXAS_TARIFARIAS))
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))

    def test_usa_o_integrador_recebido(self):
        """Com Simpson, uma vazão quadrática no tempo dá o volume exato (o trapézio, não)."""
        vazao = 30.0 + 0.1 * self.t ** 2
        exato = 3.6 * (30.0 * 24.0 + 0.1 * 24.0 ** 3 / 3.0)
        simpson = dia_de_operacao(self.t, vazao, [40.0], [0.8], Simpson())
        trapezio = dia_de_operacao(self.t, vazao, [40.0], [0.8], Trapezio())
        self.assertAlmostEqual(simpson.volume_m3, exato)
        self.assertGreater(abs(trapezio.volume_m3 - exato), 1.0)


if __name__ == "__main__":
    unittest.main()

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
from fornecido.simulador import verdade_dia


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Issue #11: regressão do trapézio em malha irregular

class TestTrapezioMalhaIrregularRegressao(unittest.TestCase):
    """Testes de regressão da issue #11 (escritos antes da correção)."""

    def test_reta_em_tres_pontos_desiguais(self):
        """∫ de y = x em [0, 3] com pontos 0, 1 e 3 vale 4,5 (e não 2,5 com passo único)."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [0.0, 1.0, 3.0]), 4.5)

    def test_funcao_linear_e_exata_em_qualquer_malha(self):
        """O trapézio é exato para 3x + 1 em [0, 2], seja qual for a malha: o resultado é 8."""
        x = np.array([0.0, 0.3, 1.1, 1.2, 2.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 8.0)

    def test_soma_das_areas_de_cada_trapezio(self):
        """Com x = 0, 0,25, 1 e 2 e y = 2, 4, 4 e 8, a área é 0,75 + 3 + 6 = 9,75."""
        resultado = Trapezio().integrar_tabela([0.0, 0.25, 1.0, 2.0], [2.0, 4.0, 4.0, 8.0])
        self.assertAlmostEqual(resultado, 0.25 * 3.0 + 0.75 * 4.0 + 1.0 * 6.0)

    def test_volume_do_dia_com_leituras_perdidas(self):
        """Com as 8 leituras perdidas do registro, o volume do dia fica a menos de 1,5% da conferência."""
        t, q = vazao_registrada(3478)
        volume = 3.6 * Trapezio().integrar_tabela(t, q)
        self.assertLess(abs(volume / verdade_dia()["volume_m3"] - 1), 0.015)

# Issue #10: regras do contrato que os testes de aceitação não verificam

T = np.arange(0.0, 24.0 + 1e-9, 1.5)


class TestAjustarPolinomioContrato(unittest.TestCase):
    """Regras de `ajustar_polinomio` que os testes de aceitação não verificam."""

    def test_grau_negativo(self):
        """Um grau negativo levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_vetores_invalidos(self):
        """Vetores de tamanhos diferentes ou que não são 1D levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)
        with self.assertRaises(ValueError):
            ajustar_polinomio(np.zeros((3, 2)), np.zeros((3, 2)), 1)

    def test_grau_zero_e_a_media(self):
        """O polinômio de grau 0 que minimiza o erro quadrático é a média dos y."""
        coef = ajustar_polinomio([0.0, 1.0, 2.0, 3.0], [2.0, 4.0, 6.0, 8.0], 0)
        self.assertTrue(np.allclose(coef, [5.0]))

    def test_pontos_justos_interpolam(self):
        """Com grau + 1 pontos o polinômio passa exatamente por todos eles."""
        x = np.array([0.0, 1.0, 3.0])
        y = np.array([2.0, -1.0, 4.0])
        coef = ajustar_polinomio(x, y, 2)
        self.assertTrue(np.allclose(np.polynomial.polynomial.polyval(x, coef), y))

    def test_recupera_a_curva_com_ruido(self):
        """Com ruído pequeno, o ajuste de grau 2 recupera 45 - 0,0022·Q² com erro baixo em 10..100 L/s."""
        rng = np.random.default_rng(5)
        q = np.arange(0.0, 101.0, 10.0)
        h = 45.0 - 0.0022 * q ** 2 + rng.normal(0.0, 0.1, q.size)
        coef = ajustar_polinomio(q, h, 2)
        ajustada = np.polynomial.polynomial.polyval(q, coef)
        self.assertLess(float(np.max(np.abs(ajustada - (45.0 - 0.0022 * q ** 2)))), 0.3)


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Regras de `dia_de_operacao` que os testes de aceitação não verificam."""

    def test_limite_de_faixa_ausente(self):
        """Se o instante de 18 h não está em t, levanta ValueError."""
        t = T[T != 18.0]
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_rendimento_nao_positivo(self):
        """Rendimento zero em algum instante levanta ValueError."""
        with self.assertRaises(ValueError):
            dia_de_operacao(T, np.full(T.size, 50.0), [40.0], [0.0], Trapezio())

    def test_malha_irregular_com_leituras_perdidas(self):
        """Com leituras perdidas (malha irregular) e vazão linear, o volume é exato: 3,6·(40·24 + 288)."""
        t = np.array([0.0, 0.25, 1.0, 5.5, 18.0, 18.25, 20.0, 21.0, 22.5, 24.0])
        resumo = dia_de_operacao(t, 40.0 + t, [40.0], [0.8], Trapezio())
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * (40.0 * 24.0 + 24.0 ** 2 / 2))

    def test_custo_e_a_soma_das_faixas(self):
        """O custo total é a soma de custo_por_faixa, que tem uma entrada por faixa."""
        resumo = dia_de_operacao(T, 40.0 + T, [45.0, 0.0, -0.0022], [0.6, 0.002], Trapezio())
        self.assertEqual(len(resumo.custo_por_faixa), 3)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))

    def test_funciona_com_outro_integrador(self):
        """Simpson (malha uniforme, número ímpar de pontos por faixa) dá o mesmo resultado que o trapézio numa vazão constante."""
        vazao = np.full(T.size, 50.0)
        com_trapezio = dia_de_operacao(T, vazao, [40.0], [0.8], Trapezio())
        com_simpson = dia_de_operacao(T, vazao, [40.0], [0.8], Simpson())
        self.assertAlmostEqual(com_simpson.volume_m3, com_trapezio.volume_m3)
        self.assertTrue(np.allclose(com_simpson.custo_por_faixa, com_trapezio.custo_por_faixa))


if __name__ == "__main__":
    unittest.main()

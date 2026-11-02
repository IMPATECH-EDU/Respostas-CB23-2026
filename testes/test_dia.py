"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np
from numpy.polynomial import polynomial as P

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada
from fornecido.simulador import gerar_demanda


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# ---------------------------------------------------------------------------------------
# Issue #11: testes de regressão do trapézio (escritos antes da correção)
# ---------------------------------------------------------------------------------------
class TestTrapezioComFalhas(unittest.TestCase):
    """Issue #11: o trapézio tem que respeitar a largura de cada intervalo da tabela."""

    def test_reta_em_malha_irregular(self):
        """O trapézio é exato para uma reta, qualquer que seja o espaçamento dos pontos."""
        x = np.array([0.0, 1.0, 3.0])                # intervalos de largura 1 e 2
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2 * x + 1), 12.0)

    def test_apagar_leituras_de_uma_reta(self):
        """Tirar leituras de uma vazão que varia em linha reta não muda o volume."""
        t = np.arange(0.0, 24.0 + 1e-9, 0.25)
        q = 40.0 + 0.5 * t
        manter = np.ones(t.size, dtype=bool)
        manter[[5, 6, 40, 77]] = False               # um buraco de 45 min e dois de 30 min
        completo = Trapezio().integrar_tabela(t, q)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t[manter], q[manter]), completo)

    def test_volume_do_dia_com_falhas(self):
        """O registro com 8 leituras perdidas dá quase o mesmo volume que o registro completo."""
        t, q = vazao_registrada(3484)
        t_completo, q_completo = gerar_demanda(3484)
        com_falhas = Trapezio().integrar_tabela(t, q)
        completo = Trapezio().integrar_tabela(t_completo, q_completo)
        self.assertLess(abs(com_falhas / completo - 1), 0.005)


# ---------------------------------------------------------------------------------------
# Issue #10: regras do contrato que os testes de aceitação não verificam
# ---------------------------------------------------------------------------------------
class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: casos do contrato de ajustar_polinomio."""

    def test_grau_negativo_e_tamanhos_diferentes(self):
        """grau < 0 e x, y de tamanhos diferentes levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_abscissas_repetidas(self):
        """Quatro pontos, mas só dois valores de x: uma parábola não fica determinada."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([1.0, 1.0, 2.0, 2.0], [0.0, 1.0, 3.0, 4.0], 2)

    def test_residuo_ortogonal_as_colunas(self):
        """O resíduo do ajuste é ortogonal às colunas 1, x, x² (é o que caracteriza o mínimo)."""
        rng = np.random.default_rng(7)
        x = np.linspace(0.0, 100.0, 11)
        y = 45.0 - 0.0022 * x ** 2 + rng.normal(0.0, 0.15, x.size)
        coef = ajustar_polinomio(x, y, 2)
        residuo = y - P.polyval(x, coef)
        V = np.vander(x, 3, increasing=True)
        # Vᵀr ≈ 0, relativo ao tamanho de cada coluna
        self.assertTrue(np.allclose(V.T @ residuo / np.linalg.norm(V, axis=0), 0.0, atol=1e-9))


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: casos do contrato de dia_de_operacao."""

    def test_limite_de_faixa_faltando(self):
        """Um registro sem a leitura das 21 h levanta ValueError."""
        t = np.arange(0.0, 24.0 + 1e-9, 0.25)
        t = t[t != 21.0]
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_cada_faixa_usa_os_seus_limites(self):
        """A ponta integra de 18 h a 21 h, incluindo as duas leituras dos limites."""
        t = np.array([0.0, 9.0, 18.0, 19.5, 21.0, 22.5, 24.0])
        vazao = 30.0 + t                             # potência proporcional à vazão
        resumo = dia_de_operacao(t, vazao, [40.0], [0.8], Trapezio())
        kw_por_litro = 998.0 * 9.81 * 40.0 / (1000.0 * 0.8 * 1000.0)
        # ∫ (30 + t) dt de 18 a 21 = 90 + (21² - 18²)/2 = 148,5 (o trapézio é exato numa reta)
        self.assertAlmostEqual(resumo.custo_por_faixa[1], 1.50 * kw_por_litro * 148.5)

    def test_simpson_recusa_o_registro_com_falhas(self):
        """Com leituras faltando, o Simpson recusa a tabela, e o ValueError chega a quem chamou."""
        t, q = vazao_registrada(3484)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, q, [40.0], [0.8], Simpson())


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio

# Um dia sintético, com leituras a cada 1,5 h (os limites 0, 18, 21 e 24 h estão na malha).
T = np.arange(0.0, 24.0 + 1e-9, 1.5)


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestTrapezioTabelaRegressao(unittest.TestCase):
    """Issue #11: testes de regressão do Trapezio.integrar_tabela (escritos antes da correção)."""

    def test_malha_nao_uniforme_reta(self):
        """Malha não uniforme [0, 1, 3] com y = 3x + 1: o trapézio é exato e dá 16,5."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 16.5)

    def test_malha_nao_uniforme_constante(self):
        """y constante 2 em [0, 0.5, 2]: a integral é 2 · 2 = 4, qualquer que seja a malha."""
        x = np.array([0.0, 0.5, 2.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.full(3, 2.0)), 4.0)

    def test_registro_com_falha_igual_ao_sem_falha(self):
        """Tirar um ponto do meio de uma reta não muda a integral pelo trapézio."""
        x = np.linspace(0.0, 4.0, 9)
        y = 5.0 - x
        sem_falha = Trapezio().integrar_tabela(x, y)
        com_falha = Trapezio().integrar_tabela(np.delete(x, 3), np.delete(y, 3))
        self.assertAlmostEqual(com_falha, sem_falha)


class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: regras do contrato de ajustar_polinomio que os testes de aceitação não verificam."""

    def test_tamanhos_diferentes(self):
        """x e y de tamanhos diferentes levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_grau_negativo(self):
        """grau negativo levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_parabola_exata_em_ordem_crescente(self):
        """Pontos de y = 1 + 2x + 3x² devolvem [1, 2, 3] (ordem crescente)."""
        x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        self.assertTrue(np.allclose(ajustar_polinomio(x, 1 + 2 * x + 3 * x ** 2, 2), [1.0, 2.0, 3.0]))


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: regras do contrato de dia_de_operacao que os testes de aceitação não verificam."""

    def test_falta_limite_de_faixa(self):
        """Sem o instante 21 h em t, levanta ValueError."""
        t = T[T != 21.0]
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_custo_total_e_a_soma_das_faixas(self):
        """O custo total é a soma dos custos de cada faixa."""
        resumo = dia_de_operacao(T, 40.0 + T, [45.0, 0.0, -0.0022], [0.6, 0.002], Trapezio())
        self.assertEqual(len(resumo.custo_por_faixa), 3)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))


if __name__ == "__main__":
    unittest.main()
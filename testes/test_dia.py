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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestTrapezioMalhaIrregularRegressao(unittest.TestCase):
    """Issue #11: o trapézio sobre tabela deve usar a largura de cada intervalo."""

    def test_malha_com_um_intervalo_maior(self):
        """Para y = x em x = [0, 1, 3], a integral é 4.5 (largura 2 no último trapézio)."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [0.0, 1.0, 3.0]), 4.5)

    def test_funcao_constante_em_malha_irregular(self):
        """A integral de y = 2 sobre uma malha irregular de 0 a 10 é 20."""
        x = np.array([0.0, 1.0, 1.5, 4.0, 7.0, 10.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.full(x.size, 2.0)), 20.0)

    def test_registro_do_dia_com_falhas(self):
        """Uma vazão constante de 1 L/s no registro com falhas integra 24 em 24 h."""
        t, _ = vazao_registrada(3517)
        self.assertGreater(np.ptp(np.diff(t)), 0.0)          # a malha não é uniforme
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.ones(t.size)), 24.0)

    def test_malha_uniforme_continua_igual(self):
        """Em malha uniforme, a tabela dá o mesmo resultado que a versão com função."""
        x = np.linspace(0.0, 2.0, 9)
        com_tabela = Trapezio().integrar_tabela(x, x ** 2)
        com_funcao = Trapezio().integrar(lambda z: z ** 2, 0.0, 2.0, 8)
        self.assertAlmostEqual(com_tabela, com_funcao)


class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: regras do contrato de `ajustar_polinomio` que a aceitação não verifica."""

    def test_grau_negativo(self):
        """Grau negativo levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_tamanhos_diferentes(self):
        """x e y com tamanhos diferentes levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_nao_e_unidimensional(self):
        """Entradas 2D levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([[0.0, 1.0], [2.0, 3.0]], [[1.0, 2.0], [3.0, 4.0]], 1)

    def test_grau_zero_e_a_media(self):
        """O polinômio de grau 0 é a média dos y."""
        coef = ajustar_polinomio([0.0, 1.0, 2.0, 3.0], [2.0, 4.0, 6.0, 8.0], 0)
        self.assertTrue(np.allclose(coef, [5.0]))


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: regras do contrato de `dia_de_operacao` que a aceitação não verifica."""

    def test_limite_de_faixa_ausente(self):
        """Sem o instante das 18 h no registro, dia_de_operacao levanta ValueError."""
        t = np.array([0.0, 6.0, 12.0, 17.0, 21.0, 24.0])
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_custo_e_a_soma_das_faixas_em_malha_irregular(self):
        """No registro com falhas, o custo total é a soma do custo das três faixas."""
        t, q = vazao_registrada(3517)
        resumo = dia_de_operacao(t, q, [45.0, 0.0, -0.0022], [0.0, 0.0215, -0.00015], Trapezio())
        self.assertEqual(len(resumo.custo_por_faixa), 3)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))

    def test_simpson_nao_serve_para_o_registro_com_falhas(self):
        """Com Simpson, o registro de malha irregular levanta ValueError."""
        t, q = vazao_registrada(3517)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, q, [45.0, 0.0, -0.0022], [0.0, 0.0215, -0.00015], Simpson())


if __name__ == "__main__":
    unittest.main()

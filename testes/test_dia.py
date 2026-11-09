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

#: Um dia sintético com leituras a cada 1,5 h (os limites 0, 18, 21 e 24 h estão na malha).
T = np.arange(0.0, 24.0 + 1e-9, 1.5)


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioTabelaRegressao(unittest.TestCase):
    """Issue #11: integrar_tabela do trapézio deve aceitar malha não uniforme."""

    def test_reta_em_malha_irregular(self) -> None:
        """O trapézio é exato para retas, qualquer que seja o espaçamento dos pontos."""
        x = np.array([0.0, 0.5, 2.0, 2.25, 4.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 28.0)

    def test_constante_com_leitura_perdida(self) -> None:
        """Vazão constante com uma leitura perdida: a área continua sendo valor × duração."""
        x = np.array([0.0, 0.25, 0.75, 1.0])     # falta a leitura de 0,5 h
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.full(x.size, 50.0)), 50.0)

    def test_registro_do_dia_com_falhas(self) -> None:
        """No registro com falhas do SCADA, o resultado é a soma de cada trapézio com a sua largura."""
        t, q = vazao_registrada(123456)
        esperado = float(np.sum(np.diff(t) * (q[1:] + q[:-1]) / 2))
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, q), esperado)


class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: regras do contrato de ajustar_polinomio que os testes de aceitação não verificam."""

    def test_ordem_crescente(self) -> None:
        """Os coeficientes saem em ordem crescente: 1 + 2x + 3x² dá [1, 2, 3]."""
        x = np.linspace(-2.0, 2.0, 7)
        self.assertTrue(np.allclose(ajustar_polinomio(x, 1 + 2 * x + 3 * x ** 2, 2), [1, 2, 3]))

    def test_grau_zero_e_a_media(self) -> None:
        """O polinômio de grau 0 de mínimos quadrados é a média dos y."""
        y = np.array([1.0, 4.0, 7.0])
        self.assertTrue(np.allclose(ajustar_polinomio([0.0, 1.0, 2.0], y, 0), [y.mean()]))

    def test_entradas_invalidas(self) -> None:
        """Tamanhos diferentes, vetores 2D e grau negativo levantam ValueError."""
        casos = [([0.0, 1.0, 2.0], [1.0, 2.0], 1),
                 ([[0.0, 1.0], [2.0, 3.0]], [[1.0, 2.0], [3.0, 4.0]], 1),
                 ([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)]
        for x, y, grau in casos:
            with self.subTest(x=x, grau=grau), self.assertRaises(ValueError):
                ajustar_polinomio(x, y, grau)


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: regras do contrato de dia_de_operacao que os testes de aceitação não verificam."""

    def test_limite_de_faixa_ausente(self) -> None:
        """Sem a leitura das 18 h, não dá para separar a ponta: ValueError."""
        t = T[T != 18.0]
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_custo_total_e_a_soma_das_faixas(self) -> None:
        """Com Simpson, o custo total é a soma das faixas, e a ponta custa 3× a hora fora dela."""
        resumo = dia_de_operacao(T, np.full(T.size, 50.0), [40.0], [0.8], Simpson())
        fora, ponta, noite = resumo.custo_por_faixa
        self.assertAlmostEqual(resumo.custo_reais, fora + ponta + noite)
        self.assertAlmostEqual(ponta, 3 * noite)          # mesmas 3 h, tarifa 3× maior
        self.assertAlmostEqual(fora / 18, noite / 3)      # mesma tarifa por hora


if __name__ == "__main__":
    unittest.main()

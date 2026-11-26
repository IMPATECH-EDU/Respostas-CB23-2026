"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestRegressaoMalhaIrregular(unittest.TestCase):
    """Testes de regressão da issue #11."""

    def test_trapezio_linear_em_malha_irregular(self):
        """Integração de uma reta em malha irregular deve ser exata."""
        x = [0.0, 1.0, 3.0]
        y = [0.0, 1.0, 3.0]
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 4.5)

    def test_trapezio_usa_largura_de_cada_intervalo(self):
        """Cada trapézio deve usar seu próprio passo, inclusive após uma lacuna."""
        x = [0.0, 0.25, 0.75, 1.0]
        y = [2.0, 2.0, 2.0, 2.0]
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 2.0)


class TestContratosMarco4(unittest.TestCase):
    """Testes adicionais dos contratos da issue #10."""

    def test_ajuste_rejeita_vetores_de_dimensoes_diferentes(self):
        """O ajuste deve rejeitar x e y que não sejam vetores 1D."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([[0.0, 1.0]], [1.0, 2.0], 1)

    def test_ajuste_rejeita_grau_negativo(self):
        """O grau do polinômio precisa ser não negativo."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0], [1.0, 2.0], -1)

    def test_dia_rejeita_registro_sem_limite_tarifario(self):
        """O balanço exige leituras nos quatro limites das faixas tarifárias."""
        t = np.array([0.0, 6.0, 12.0, 18.0, 24.0])
        q = np.full(t.size, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, q, [40.0], [0.8], Trapezio())

    def test_custo_total_e_soma_das_faixas(self):
        """O custo total deve ser exatamente a soma dos custos tarifários."""
        t = np.arange(0.0, 24.0 + 1.5, 1.5)
        q = np.full(t.size, 50.0)
        resumo = dia_de_operacao(t, q, [40.0], [0.8], Trapezio())
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))


if __name__ == "__main__":
    unittest.main()

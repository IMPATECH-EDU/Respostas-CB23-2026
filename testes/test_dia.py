"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.integracao import Simpson
from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Trapezio
from fornecido.energia import vazao_registrada
import numpy as np


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

T = np.arange(0.0, 24.0 + 1e-9, 1.5)

class TestRegressaoIssue11(unittest.TestCase):
    """Testes de regressão para a issue #11 (malha não uniforme no trapézio)."""

    def test_trapezio_malha_nao_uniforme(self):
        """Verifica que Trapezio.integrar_tabela integra exatamente uma reta em malha não uniforme."""
        x = np.array([0.0, 0.25, 1.0, 2.0])
        y = 2.0 * x + 1.0  # ∫_0^2 (2x + 1) dx = 6.0 exato
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 6.0)

    def test_trapezio_vazao_constante_com_falhas(self):
        """Garante que falhas de comunicação no registro não reduzem o volume bombeado no dia."""
        t, _ = vazao_registrada(123456)  # 89 leituras com intervalos de 15, 30 e 45 min
        q = np.full_like(t, 50.0)
        resumo = dia_de_operacao(t, q, [40.0], [0.8], Trapezio())
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * 50.0 * 24.0)

class TestContratoDia(unittest.TestCase):
    """Testes de contrato adicionais para ajustar_polinomio e dia_de_operacao."""

    def test_ajustar_polinomio_entradas_invalidas(self):
        """Levanta ValueError para grau negativo, tamanhos diferentes ou entrada não 1D."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)
        with self.assertRaises(ValueError):
            ajustar_polinomio([[0.0, 1.0]], [[1.0, 2.0]], 0)

    def test_ajustar_polinomio_grau_zero(self):
        """Verifica que grau=0 devolve um único coeficiente igual à média de y."""
        y = np.array([2.0, 4.0, 6.0, 8.0])
        coef = ajustar_polinomio([0.0, 1.0, 2.0, 3.0], y, 0)
        self.assertEqual(coef.shape, (1,))
        self.assertAlmostEqual(float(coef[0]), 5.0)

    def test_dia_de_operacao_limite_de_faixa_ausente(self):
        """Levanta ValueError se algum limite tarifário (0, 18, 21 ou 24 h) faltar em t."""
        for limite in (0.0, 18.0, 21.0, 24.0):
            t_incompleto = T[~np.isclose(T, limite)]
            vazao = np.full(t_incompleto.size, 50.0)
            with self.assertRaises(ValueError):
                dia_de_operacao(t_incompleto, vazao, [40.0], [0.8], Trapezio())

    def test_dia_de_operacao_com_simpson_e_consistencia_custo(self):
        """Executa dia_de_operacao com Simpson em malha uniforme e valida soma das faixas."""
        vazao = 40.0 + T
        resumo = dia_de_operacao(T, vazao, [45.0, 0.0, -0.0022], [0.6, 0.002], Simpson())
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * (40.0 * 24.0 + 24.0 ** 2 / 2))
        self.assertEqual(len(resumo.custo_por_faixa), 3)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))

if __name__ == "__main__":
    unittest.main()

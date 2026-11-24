"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import numpy as np

from elevatoria.integracao import Simpson, Trapezio
from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from fornecido.energia import potencia_eletrica


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)

class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: testes de regressão para `Trapezio.integrar_tabela` em malha não uniforme."""

    def test_trapezio_tabela_malha_nao_uniforme_constante(self):
        """Integra função constante em malha com passos diferentes usando cada largura dx."""
        x = np.array([0.0, 1.0, 5.0])
        y = np.array([10.0, 10.0, 10.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 50.0)

    def test_trapezio_tabela_malha_nao_uniforme_linear(self):
        """Integra f(x) = 2x + 1 exatamente em malha irregular [0, 0.25, 1, 4]."""
        x = np.array([0.0, 0.25, 1.0, 4.0])
        y = 2.0 * x + 1.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 20.0)


class TestContratoDia(unittest.TestCase):
    """Issue #10: regras de contrato de `ajustar_polinomio` e `dia_de_operacao`."""

    def test_ajustar_polinomio_rejeita_grau_negativo_ou_2d(self):
        """Levanta ValueError para grau negativo ou arrays não unidimensionais."""
        with self.assertRaises(ValueError):
            ajustar_polinomio(np.array([0.0, 1.0]), np.array([1.0, 2.0]), -1)
        with self.assertRaises(ValueError):
            ajustar_polinomio(np.zeros((2, 2)), np.zeros((2, 2)), 1)

    def test_dia_de_operacao_rejeita_limite_de_faixa_ausente(self):
        """Levanta ValueError se algum limite de tarifa (0, 18, 21 ou 24 h) faltar em t."""
        t_sem_18 = np.array([0.0, 12.0, 21.0, 24.0])
        vazao = np.full(t_sem_18.size, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t_sem_18, vazao, np.array([40.0]), np.array([0.8]), Trapezio())

    def test_dia_de_operacao_aplica_tarifa_ponta_e_soma_faixas(self):
        """Aplica tarifa tripla das 18h às 21h e iguala custo_reais à soma das faixas."""
        t = np.array([0.0, 18.0, 21.0, 24.0])
        vazao = np.full(t.size, 50.0)
        resumo = dia_de_operacao(t, vazao, np.array([40.0]), np.array([0.8]), Trapezio())
        p = float(potencia_eletrica(50.0, 40.0, 0.8))
        self.assertAlmostEqual(resumo.custo_por_faixa[1], p * 3.0 * 1.50)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))

# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

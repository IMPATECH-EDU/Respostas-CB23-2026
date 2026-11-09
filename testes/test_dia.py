"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.integracao import Simpson


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Trapezio


class TestRegressaoIssue11(unittest.TestCase):
    """Issue #11: o trapézio sobre tabela deve usar a largura real de cada intervalo."""

    def test_malha_irregular_funcao_linear(self):
        """Em malha irregular, ∫ (3x + 1) dx de 0 a 2 deve ser 8 (o trapézio é exato para retas)."""
        x = np.array([0.0, 0.25, 0.5, 1.0, 2.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 8.0)

    def test_leitura_perdida_na_vazao_constante(self):
        """Vazão constante com leituras perdidas: o volume deve ser vazão × tempo, sem subestimar."""
        t = np.array([0.0, 0.25, 0.5, 1.0, 1.25, 1.5, 2.0])   # faltam as leituras de 0,75 e 1,75
        q = np.full(t.size, 10.0)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, q), 20.0)


class TestContratoDia(unittest.TestCase):
    """Issue #10: regras do contrato que os testes de aceitação não verificam."""

    def test_ajustar_polinomio_argumentos_invalidos(self):
        """`ajustar_polinomio` levanta ValueError para grau negativo e para x e y de tamanhos diferentes."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_limite_de_faixa_ausente(self):
        """`dia_de_operacao` levanta ValueError se um limite de faixa (aqui 21 h) não está em `t`."""
        t = np.array([h for h in np.arange(0.0, 24.0 + 1e-9, 1.5) if h != 21.0])
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_malha_irregular_e_soma_das_faixas(self):
        """Com leituras perdidas, volume e energia são exatos e o custo é a soma das faixas."""
        t = np.array([0.0, 3.0, 6.0, 12.0, 18.0, 19.0, 21.0, 22.5, 24.0])   # espaçamento irregular
        resumo = dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())
        potencia = 998.0 * 9.81 * 0.050 * 40.0 / (1000.0 * 0.8)
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * 50.0 * 24.0)
        self.assertAlmostEqual(resumo.energia_kwh, potencia * 24.0)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))
        self.assertAlmostEqual(resumo.custo_reais, potencia * 15.0)



if __name__ == "__main__":
    unittest.main()

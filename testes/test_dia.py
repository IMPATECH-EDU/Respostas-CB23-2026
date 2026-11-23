"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonEx(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_parabola_100exato(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioMIrregular(unittest.TestCase):
    """Regressão da issue #11: Trapezio.integrar_tabela deve usar cada passo x[i+1] - x[i]."""

    def test_malha_funcao_linear(self):
        """Trapézio integra exatamente uma reta em malha irregular com passos diferentes."""
        x = np.array([0.0, 0.25, 0.75, 1.0])
        y = 2.0 * x + 1.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 2.0)

    def test_registro_com_falhas_e_integral_constante(self):
        """Vazão constante de 50 L/s em 24 h com leituras perdidas integra 1200 L/s·h."""
        t_completo = np.linspace(0.0, 24.0, 97)
        t_falho = np.delete(t_completo, [10, 25, 40, 60])
        q = np.full_like(t_falho, 50.0)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t_falho, q), 1200.0)

    def test_intervalo_inicio_n_superestima(self):
        """Malha irregular com primeiro passo maior não superestima a integral."""
        x = np.array([0.0, 1.0, 1.25, 1.5])
        y = np.ones_like(x)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 1.5)


class TestContratos(unittest.TestCase):
    """Regras do contrato da issue #10 que os testes de aceitação não verificam."""

    def test_ajustar_dim_e_polinomio_grau_negativo(self):
        """ajustar_polinomio levanta ValueError para grau negativo ou tamanhos incompatíveis."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0], [1.0, 2.0, 3.0], 1)

    def test_dia_de_operacao(self):
        """dia_de_operacao levanta ValueError quando falta um limite de faixa tarifária em t."""
        t_sem_ponta = np.array([0.0, 6.0, 12.0, 20.0, 24.0])  # faltam 18.0 e 21.0
        vazao = np.full_like(t_sem_ponta, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t_sem_ponta, vazao, [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()
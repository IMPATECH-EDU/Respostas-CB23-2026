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


class TestRegressaoIssue11(unittest.TestCase):
    """Issue #11: o trapézio deve respeitar a largura de cada intervalo da tabela."""

    def test_trapezio_malha_nao_uniforme(self):
        """Intervalos de larguras diferentes: a área de y = 1 em [0, 3] é 3."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [1.0, 1.0, 1.0]), 3.0)

    def test_volume_do_dia_com_leituras_perdidas(self):
        """Leituras perdidas não reduzem o volume de um dia com vazão constante."""
        t = np.delete(np.linspace(0.0, 24.0, 97), [10, 40, 80])
        resumo = dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * 50.0 * 24.0)


class TestContratoDia(unittest.TestCase):
    """Regras das docstrings de `elevatoria/dia.py` que a aceitação não verifica."""

    def test_ajuste_com_entrada_invalida(self):
        """Tamanhos diferentes, x que não é 1D e grau negativo levantam ValueError."""
        casos = [([0.0, 1.0, 2.0], [1.0, 2.0], 1),
                 ([[0.0, 1.0], [2.0, 3.0]], [[1.0, 2.0], [3.0, 4.0]], 1),
                 ([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)]
        for x, y, grau in casos:
            with self.subTest(x=x, y=y, grau=grau):
                with self.assertRaises(ValueError):
                    ajustar_polinomio(x, y, grau)

    def test_dia_sem_limite_de_faixa(self):
        """A falta de qualquer limite de faixa (0, 18, 21 ou 24 h) em t levanta ValueError."""
        malha = np.linspace(0.0, 24.0, 97)
        for limite in (0.0, 18.0, 21.0, 24.0):
            with self.subTest(limite=limite):
                t = malha[malha != limite]
                with self.assertRaises(ValueError):
                    dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()

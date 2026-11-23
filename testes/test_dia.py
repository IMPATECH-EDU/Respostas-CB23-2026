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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: integrar_tabela supunha passo uniforme e errava com leituras faltando."""

    def test_malha_nao_uniforme_com_funcao_constante(self):
        """y = 2 em x = [0, 1, 3]: a área é 2 · 3 = 6, apesar do buraco entre 1 e 3."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [2.0, 2.0, 2.0]), 6.0)

    def test_leitura_faltando_no_meio_do_dia(self):
        """Vazão constante de 10 em 0..24 h a cada 0,25 h, sem as leituras das 10 às 12 h: 240."""
        t = np.arange(0.0, 24.0 + 1e-9, 0.25)
        t = t[(t <= 10.0) | (t >= 12.0)]
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.full(t.size, 10.0)), 240.0)


class TestContratoDia(unittest.TestCase):
    """Regras das docstrings da issue #10 que os testes de aceitação não verificam."""

    def test_grau_negativo_levanta_value_error(self):
        """grau < 0 levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_x_e_y_de_tamanhos_diferentes(self):
        """x com 3 pontos e y com 2 levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_limite_de_faixa_ausente_em_t(self):
        """Sem a leitura das 18 h, a faixa de ponta não tem início: ValueError."""
        t = np.array([0.0, 6.0, 12.0, 17.5, 19.0, 21.0, 24.0])
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()

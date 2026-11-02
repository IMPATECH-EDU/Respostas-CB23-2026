"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada
from fornecido.simulador import gerar_demanda


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# ---------------------------------------------------------------------------------------
# Issue #11: testes de regressão do trapézio (escritos antes da correção)
# ---------------------------------------------------------------------------------------
class TestTrapezioComFalhas(unittest.TestCase):
    """Issue #11: o trapézio tem que respeitar a largura de cada intervalo da tabela."""

    def test_reta_em_malha_irregular(self):
        """O trapézio é exato para uma reta, qualquer que seja o espaçamento dos pontos."""
        x = np.array([0.0, 1.0, 3.0])                # intervalos de largura 1 e 2
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2 * x + 1), 12.0)

    def test_apagar_leituras_de_uma_reta(self):
        """Tirar leituras de uma vazão que varia em linha reta não muda o volume."""
        t = np.arange(0.0, 24.0 + 1e-9, 0.25)
        q = 40.0 + 0.5 * t
        manter = np.ones(t.size, dtype=bool)
        manter[[5, 6, 40, 77]] = False               # um buraco de 45 min e dois de 30 min
        completo = Trapezio().integrar_tabela(t, q)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t[manter], q[manter]), completo)

    def test_volume_do_dia_com_falhas(self):
        """O registro com 8 leituras perdidas dá quase o mesmo volume que o registro completo."""
        t, q = vazao_registrada(3484)
        t_completo, q_completo = gerar_demanda(3484)
        com_falhas = Trapezio().integrar_tabela(t, q)
        completo = Trapezio().integrar_tabela(t_completo, q_completo)
        self.assertLess(abs(com_falhas / completo - 1), 0.005)


if __name__ == "__main__":
    unittest.main()

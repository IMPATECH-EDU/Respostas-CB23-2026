"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: integrar_tabela usava a largura do 1º intervalo para todos os trapézios."""

    def test_reta_em_malha_irregular(self):
        """O trapézio é exato para retas, também com passos diferentes: ∫₀³ (3x+1) dx = 16,5."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3.0 * x + 1.0), 16.5)

    def test_constante_com_leitura_perdida(self):
        """Uma constante 1 em [0, 1] integra 1, mesmo faltando a leitura de 0,5."""
        x = np.array([0.0, 0.25, 0.75, 1.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.ones_like(x)), 1.0)

    def test_registro_do_dia_com_vazao_constante(self):
        """Nos instantes reais do registro (com falhas), 50 L/s por 24 h integram 1200 L/s·h."""
        t, _ = vazao_registrada(3472)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.full(t.size, 50.0)), 1200.0)

    def test_primeiro_passo_maior_que_os_outros(self):
        """Se o 1º intervalo for o maior, o resultado não pode crescer: ∫₀² x dx = 2 com x = [0, 1, 1.5, 2]."""
        x = np.array([0.0, 1.0, 1.5, 2.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x), 2.0)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

import math

from elevatoria.operacao import ordem_convergencia
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook


class TestNewton(unittest.TestCase):
    """Issue #9: o Newton deve ter ordem de convergência perto de 2."""

    def test_ordem_colebrook_re_10_000(self):
        """O caso do relato: em Colebrook com Re = 10^4, a ordem do Newton é maior que 1.8."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        ordem = ordem_convergencia(resultado.historico, resultado.raiz)
        self.assertGreater(ordem, 1.8)

    def test_ordem_colebrook_re_100_000(self):
        """Em Colebrook com Re = 10^5, a ordem do Newton também é maior que 1.8."""
        _, resultado = fator_atrito_colebrook(1e5, 0.15e-3 / 0.20, Newton(tol=1e-12))
        ordem = ordem_convergencia(resultado.historico, resultado.raiz)
        self.assertGreater(ordem, 1.8)

    def test_ordem_raiz_de_2(self):
        """Na raiz de x² - 2 em [0, 2], a ordem do Newton é maior que 1.8."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2, 0.0, 2.0)
        ordem = ordem_convergencia(resultado.historico, math.sqrt(2))
        self.assertGreater(ordem, 1.8)

if __name__ == "__main__":
    unittest.main()

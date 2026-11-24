"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioMalhaIrregular(unittest.TestCase):
    """Regressões para integrar tabelas com intervalos de larguras diferentes."""

    def test_malha_irregular_linear(self) -> None:
        """Cada trapézio usa a largura do seu próprio intervalo."""
        x = np.array([0.0, 1.0, 3.0])
        y = 2.0 * x + 1.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 12.0)

    def test_malha_irregular_com_leitura_ausente(self) -> None:
        """A integração continua correta quando um intervalo mede o dobro do usual."""
        x = np.array([0.0, 1.0, 3.0, 4.0])
        y = np.ones_like(x)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 4.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

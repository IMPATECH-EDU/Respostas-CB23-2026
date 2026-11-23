"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao

from elevatoria.integracao import Trapezio

from elevatoria.integracao import Simpson


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestTrapezioIrregular(unittest.TestCase):
    """Regressões da largura dos trapézios em malha irregular."""

    def test_constante_em_malha_irregular(self) -> None:
        """A integral de uma constante usa a duração total da tabela."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0, 1, 4], [2, 2, 2]), 8.0)

    def test_rampa_em_malha_irregular(self) -> None:
        """Integra exatamente uma reta mesmo quando os passos são diferentes."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0, 2, 3], [0, 2, 3]), 4.5)



class TestDiaValidacao(unittest.TestCase):
    """Casos de validação do ajuste e das faixas tarifárias."""

    def test_ajuste_rejeita_grau_negativo(self) -> None:
        """Um polinômio não pode ter grau negativo."""
        with self.assertRaisesRegex(ValueError, "grau"):
            ajustar_polinomio(np.array([0, 1]), np.array([1, 2]), -1)

    def test_dia_rejeita_limite_de_faixa_ausente(self) -> None:
        """O balanço exige uma leitura exatamente às 18 horas."""
        t = np.array([0, 17, 19, 21, 24])
        with self.assertRaisesRegex(ValueError, "limite"):
            dia_de_operacao(t, np.full(t.size, 40), np.array([35]), np.array([0.8]), Trapezio())


if __name__ == "__main__":
    unittest.main()

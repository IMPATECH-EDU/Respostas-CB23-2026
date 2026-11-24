"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.dia import ajustar_polinomio
from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoTrapezioMalhaIrregular(unittest.TestCase):
    """Regressões da issue #11 para dados com falhas de comunicação."""

    def test_vazao_constante_em_intervalos_irregulares(self):
        """A integral de uma vazão constante deve usar toda a duração registrada."""
        self.assertAlmostEqual(
            Trapezio().integrar_tabela([0.0, 1.0, 3.0], [2.0, 2.0, 2.0]),
            6.0,
        )

    def test_vazao_linear_com_intervalo_de_leitura_perdida(self):
        """A área sob uma vazão linear deve considerar cada intervalo entre leituras."""
        self.assertAlmostEqual(
            Trapezio().integrar_tabela([0.0, 1.0, 3.0], [0.0, 1.0, 3.0]),
            4.5,
        )


class TestAjustarPolinomioValidacao(unittest.TestCase):
    """Validações do contrato de ajustar_polinomio."""

    def test_rejeita_vetores_de_dimensoes_diferentes(self):
        """Vetores x e y de tamanhos diferentes devem levantar ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_rejeita_grau_negativo(self):
        """Grau negativo deve levantar ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0], [1.0, 2.0], -1)


if __name__ == "__main__":
    unittest.main()

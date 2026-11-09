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


class TestRegressaoTrapezio(unittest.TestCase):
    """Testes de regressão da issue #11 ANTES da correção."""

    def test_trapezio_malha_nao_uniforme_constante(self):
        """Trapézio deve integrar função constante corretamente mesmo com falhas de comunicação (passo variável)."""
        import numpy as np
        from elevatoria.integracao import Trapezio
        x = np.array([0.0, 1.0, 3.0])  # salto de 2 horas no segundo intervalo
        y = np.array([2.0, 2.0, 2.0])
        # Integral exata de y=2 de 0 a 3 é 6.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 6.0)

    def test_trapezio_malha_irregular_linear(self):
        """Trapézio em malha irregular deve calcular a área exata para polinômio de grau 1."""
        import numpy as np
        from elevatoria.integracao import Trapezio
        x = np.array([0.0, 1.0, 2.0, 5.0])
        y = 2.0 * x + 1.0  # integral de 2x+1 de 0 a 5 = [x^2 + x] = 30.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 30.0)


class TestDiaContrato(unittest.TestCase):
    """Testes de contrato de ajustar_polinomio e dia_de_operacao não cobertos pela aceitação."""

    def test_ajustar_polinomio_grau_negativo(self):
        """ajustar_polinomio com grau < 0 deve levantar ValueError."""
        from elevatoria.dia import ajustar_polinomio
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [0.0, 1.0, 2.0], -1)

    def test_ajustar_polinomio_tamanhos_diferentes(self):
        """ajustar_polinomio com x e y de tamanhos distintos levanta ValueError."""
        from elevatoria.dia import ajustar_polinomio
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [0.0, 1.0], 1)

    def test_dia_de_operacao_falta_limite_faixa(self):
        """dia_de_operacao sem algum limite tarifario em t levanta ValueError."""
        import numpy as np
        from elevatoria.dia import dia_de_operacao
        from elevatoria.integracao import Trapezio
        # malha que omite o ponto 18.0
        t = np.array([0.0, 6.0, 12.0, 20.0, 21.0, 24.0])
        vazao = np.full(t.size, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, vazao, [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()

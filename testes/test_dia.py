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


if __name__ == "__main__":
    unittest.main()

class TestTrapezioRegressao(unittest.TestCase):
    """Testes de regressão da issue #11."""

    def test_integracao_tabela_irregular_linear(self):
        """Regressão #11: o trapézio deve usar larguras diferentes da malha irregular."""
        import numpy as np
        from elevatoria.integracao import Trapezio
        x = np.array([0.0, 1.0, 3.0])
        y = 2.0 * x + 1.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 12.0)

    def test_integracao_tabela_irregular_com_mais_lacunas(self):
        """Regressão #11: a soma dos trapézios locais deve ser correta em todos os intervalos."""
        import numpy as np
        from elevatoria.integracao import Trapezio
        x = np.array([0.0, 0.5, 2.0, 4.0])
        y = np.full_like(x, 3.0)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 12.0)

    def test_ajustar_polinomio_rejeita_vetores_de_tamanhos_diferentes(self):
        """O ajuste deve recusar vetores x e y com comprimentos diferentes."""
        from elevatoria.dia import ajustar_polinomio
        with self.assertRaises(ValueError):
            ajustar_polinomio([0, 1, 2], [1, 2], 1)

    def test_dia_rejeita_registro_sem_limite_tarifario(self):
        """O balanço exige os quatro limites das faixas tarifárias na malha temporal."""
        import numpy as np
        from elevatoria.dia import dia_de_operacao
        from elevatoria.integracao import Trapezio
        t = np.array([0.0, 6.0, 12.0, 18.0, 24.0])  # falta 21 h
        q = np.full(t.size, 10.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, q, [40.0], [0.8], Trapezio())

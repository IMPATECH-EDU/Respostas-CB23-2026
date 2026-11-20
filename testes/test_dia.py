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

class TestTrapezioTabela(unittest.TestCase):
    """Issue #11: integrar_tabela deve usar a largura de cada intervalo (malha não uniforme)."""

    def test_reta_em_malha_irregular(self):
        """A integral de 3x + 1 nos pontos [0, 1, 3] é 16.5 (o trapézio é exato para retas)."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 16.5)

    def test_vazao_constante_com_leitura_perdida(self):
        """Vazão constante de 50 L/s de 0 a 1 h, sem a leitura de 0,75 h: a integral é 50."""
        t = np.array([0.0, 0.25, 0.5, 1.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.full(t.size, 50.0)), 50.0)

    def test_igual_ao_numpy_em_malha_irregular(self):
        """Numa malha irregular qualquer, o resultado é igual ao de np.trapezoid."""
        rng = np.random.default_rng(3537)
        x = np.sort(rng.uniform(0.0, 24.0, 40))
        y = 40.0 + 10.0 * np.sin(x)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), float(np.trapezoid(y, x)))


T = np.arange(0.0, 24.0 + 1e-9, 1.5)    # um dia com leituras a cada 1,5 h

class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: regras do contrato de ajustar_polinomio que os testes de aceitação não verificam."""

    def test_grau_negativo(self):
        """Com grau < 0, levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_entradas_invalidas(self):
        """Com x e y de tamanhos diferentes ou x 2D, levanta ValueError."""
        casos = [([0.0, 1.0, 2.0], [1.0, 2.0]), ([[0.0, 1.0], [2.0, 3.0]], [1.0, 2.0, 3.0, 4.0])]
        for x, y in casos:
            with self.subTest(x=x, y=y), self.assertRaises(ValueError):
                ajustar_polinomio(x, y, 1)

    def test_grau_zero_e_a_media(self):
        """Com grau 0, o único coeficiente é a média de y."""
        y = np.array([2.0, 5.0, 3.0, 6.0])
        coef = ajustar_polinomio([0.0, 1.0, 2.0, 3.0], y, 0)
        self.assertEqual(len(coef), 1)
        self.assertAlmostEqual(coef[0], float(y.mean()))


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: regras do contrato de dia_de_operacao que os testes de aceitação não verificam."""

    def test_falta_limite_de_faixa(self):
        """Sem a leitura das 18 h (início da ponta), levanta ValueError."""
        t = T[T != 18.0]
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_custo_total_e_a_soma_das_faixas(self):
        """O custo total é a soma das faixas, e a ponta custa 3 vezes mais que as 3 h finais."""
        resumo = dia_de_operacao(T, np.full(T.size, 50.0), [40.0], [0.8], Trapezio())
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa))
        self.assertAlmostEqual(resumo.custo_por_faixa[1], 3 * resumo.custo_por_faixa[2])

if __name__ == "__main__":
    unittest.main()

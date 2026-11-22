"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import FAIXAS_TARIFARIAS, potencia_eletrica

#: Um dia de teste com leituras a cada 1,5 h (os limites 0, 18, 21 e 24 h estão na malha).
_T = np.arange(0.0, 24.0 + 1e-9, 1.5)


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# ---------------------------------------------------------------------------------------
# Issue #11: regressão do trapézio em tabela (escritos antes da correção; falham no original)
# ---------------------------------------------------------------------------------------
class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: integrar_tabela deve usar a largura de cada intervalo, não só a primeira."""

    def test_reta_em_malha_irregular(self):
        """O trapézio é exato para uma reta, mesmo com intervalos de larguras diferentes."""
        x = np.array([0.0, 1.0, 3.0, 3.5, 6.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2.0 * x + 1.0), 42.0)

    def test_leitura_perdida_no_registro(self):
        """Vazão de 1 L/s com uma leitura perdida (passos de 15 e 30 min) integra 1 L/s·h."""
        t = np.array([0.0, 0.25, 0.75, 1.0])     # falta a leitura de 0,5 h
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.ones(t.size)), 1.0)

    def test_igual_ao_trapezoid_do_numpy(self):
        """Numa malha irregular aleatória, o resultado coincide com np.trapezoid."""
        rng = np.random.default_rng(11)
        x = np.cumsum(rng.uniform(0.1, 1.0, 40))
        y = np.sin(x) + 0.1 * x
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), float(np.trapezoid(y, x)))


# ---------------------------------------------------------------------------------------
# Issue #10: regras do contrato que os testes de aceitação não verificam
# ---------------------------------------------------------------------------------------
class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: validações e ordem dos coeficientes de ajustar_polinomio."""

    def test_entradas_invalidas(self):
        """Tamanhos diferentes, x 2D ou grau negativo levantam ValueError."""
        casos = {"tamanhos": ([0.0, 1.0, 2.0], [1.0, 2.0], 1),
                 "2D": ([[0.0, 1.0], [2.0, 3.0]], [[1.0, 2.0], [3.0, 4.0]], 1),
                 "grau negativo": ([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)}
        for nome, (x, y, grau) in casos.items():
            with self.subTest(caso=nome), self.assertRaises(ValueError):
                ajustar_polinomio(x, y, grau)

    def test_recupera_cubica_em_ordem_crescente(self):
        """Dados exatos de 1 − 2x + 0,5x³ devolvem [1, −2, 0, 0,5], em ordem crescente."""
        x = np.linspace(-3.0, 3.0, 9)
        coef = ajustar_polinomio(x, 1.0 - 2.0 * x + 0.5 * x ** 3, 3)
        self.assertTrue(np.allclose(coef, [1.0, -2.0, 0.0, 0.5]))

    def test_pontos_repetidos_nao_contam(self):
        """Três pontos, mas só dois valores distintos de x, não bastam para uma parábola."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([1.0, 1.0, 2.0], [3.0, 4.0, 5.0], 2)


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: regras de dia_de_operacao fora dos testes de aceitação."""

    def test_limite_de_faixa_ausente(self):
        """Sem a leitura das 21 h, as faixas não podem ser separadas: ValueError."""
        t = _T[_T != 21.0]
        with self.assertRaisesRegex(ValueError, "21"):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_faixas_somam_a_energia_em_malha_irregular(self):
        """Com o trapézio, as energias das faixas somam a energia do dia, mesmo com falhas."""
        t = np.delete(np.arange(0.0, 24.0 + 1e-9, 0.25), [5, 40, 77, 90])  # 4 leituras perdidas
        vazao = 50.0 + 10.0 * np.sin(np.pi * t / 12.0)
        resumo = dia_de_operacao(t, vazao, [45.0, 0.0, -0.0022], [0.6, 0.002], Trapezio())
        energia_das_faixas = sum(c / preco for c, (_, _, preco)
                                 in zip(resumo.custo_por_faixa, FAIXAS_TARIFARIAS))
        self.assertAlmostEqual(energia_das_faixas, resumo.energia_kwh)

    def test_funciona_com_simpson(self):
        """Com malha uniforme e faixas de número ímpar de pontos, Simpson também serve."""
        vazao = 40.0 + _T
        resumo = dia_de_operacao(_T, vazao, [45.0, 0.0, -0.0022], [0.6, 0.002], Simpson())
        potencia = potencia_eletrica(vazao, 45.0 - 0.0022 * vazao ** 2, 0.6 + 0.002 * vazao)
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * (40.0 * 24.0 + 24.0 ** 2 / 2))
        self.assertAlmostEqual(resumo.energia_kwh, Simpson().integrar_tabela(_T, potencia))


if __name__ == "__main__":
    unittest.main()
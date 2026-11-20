"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada

# Leituras de hora em hora, de 0 h a 24 h: os limites das faixas (0, 18, 21, 24) estão na malha.
HORAS = np.arange(0.0, 25.0, 1.0)


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


class TestContratoAjustarPolinomio(unittest.TestCase):
    """Regras da docstring de ajustar_polinomio que os testes de aceitação não verificam."""

    def test_entradas_invalidas(self):
        """Tamanhos diferentes, vetores 2D ou grau negativo levantam ValueError."""
        casos = [([0.0, 1.0, 2.0], [1.0, 2.0], 1),
                 (np.zeros((2, 2)), np.zeros((2, 2)), 1),
                 ([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)]
        for x, y, grau in casos:
            with self.subTest(grau=grau, n=np.size(x)), self.assertRaises(ValueError):
                ajustar_polinomio(x, y, grau)

    def test_ordem_crescente_e_interpolacao_exata(self):
        """Com grau + 1 pontos, o ajuste passa pelos pontos e os coeficientes vêm em ordem crescente."""
        x = np.array([-1.0, 0.0, 2.0])
        coef = ajustar_polinomio(x, 5.0 - 3.0 * x + 0.5 * x ** 2, 2)   # c0 = 5, c1 = −3, c2 = 0,5
        self.assertTrue(np.allclose(coef, [5.0, -3.0, 0.5]))

    def test_grau_zero_e_a_media(self):
        """O polinômio constante de mínimos quadrados é a média dos y."""
        y = np.array([3.0, 7.0, 4.0, 10.0])
        coef = ajustar_polinomio(np.arange(4.0), y, 0)
        self.assertEqual(len(coef), 1)
        self.assertAlmostEqual(float(coef[0]), float(y.mean()))

    def test_residuo_ortogonal_as_colunas(self):
        """No ótimo, o resíduo é ortogonal a 1, x e x² (condição de mínimos quadrados)."""
        rng = np.random.default_rng(3472)
        x = np.linspace(0.0, 100.0, 15)
        y = 45.0 - 0.0022 * x ** 2 + rng.normal(0.0, 0.2, x.size)
        coef = ajustar_polinomio(x, y, 2)
        residuo = y - np.polynomial.polynomial.polyval(x, coef)
        matriz = np.vander(x, 3, increasing=True)
        self.assertTrue(np.allclose(matriz.T @ residuo, 0.0, atol=1e-6 * np.abs(matriz.T @ y).max()))


class TestContratoDiaDeOperacao(unittest.TestCase):
    """Regras da docstring de dia_de_operacao que os testes de aceitação não verificam."""

    def test_falta_um_limite_de_faixa(self):
        """Sem a leitura das 21 h (limite entre ponta e fora de ponta), levanta ValueError."""
        horas = HORAS[HORAS != 21.0]
        with self.assertRaisesRegex(ValueError, "21"):
            dia_de_operacao(horas, np.full(horas.size, 50.0), [40.0], [0.8], Trapezio())

    def test_custo_e_a_soma_das_faixas(self):
        """O custo total é exatamente a soma de custo_por_faixa, e há uma parcela por faixa."""
        vazao = 45.0 + 15.0 * np.sin(2.0 * np.pi * (HORAS - 12.0) / 24.0)
        resumo = dia_de_operacao(HORAS, vazao, [45.0, 0.0, -0.0022], [0.1, 0.02, -0.0001], Trapezio())
        self.assertEqual(len(resumo.custo_por_faixa), 3)
        self.assertAlmostEqual(resumo.custo_reais, sum(resumo.custo_por_faixa), places=12)

    def test_ponta_nao_vaza_para_as_vizinhas(self):
        """Bombeando só de 18 h a 21 h, a ponta cobra as 3 h a 1,50 R$/kWh e as vizinhas só a rampa de 1 h a 0,50."""
        vazao = np.where((HORAS >= 18.0) & (HORAS <= 21.0), 50.0, 0.0)
        resumo = dia_de_operacao(HORAS, vazao, [40.0], [0.8], Trapezio())
        potencia = 998.0 * 9.81 * 0.050 * 40.0 / (1000.0 * 0.8)
        self.assertTrue(np.allclose(resumo.custo_por_faixa[1], 1.50 * potencia * 3.0))
        # nas faixas vizinhas, só a rampa de 1 h entre a leitura de fronteira e a seguinte
        self.assertAlmostEqual(resumo.custo_por_faixa[0], 0.50 * potencia * 0.5)
        self.assertAlmostEqual(resumo.custo_por_faixa[2], 0.50 * potencia * 0.5)

    def test_usa_o_integrador_recebido(self):
        """Com o Simpson (malha de meia hora: nº ímpar de pontos em cada faixa), um perfil cúbico integra exato."""
        meia_hora = np.arange(0.0, 24.25, 0.5)               # 37, 7 e 7 pontos nas três faixas
        vazao = 40.0 + 0.001 * meia_hora ** 3                # ∫₀²⁴ = 960 + 0,001·24⁴/4
        resumo = dia_de_operacao(meia_hora, vazao, [40.0], [0.8], Simpson())
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * (40.0 * 24.0 + 0.001 * 24.0 ** 4 / 4.0))


if __name__ == "__main__":
    unittest.main()

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

#: Malha uniforme de 15 min, como no registro sem falhas (97 pontos, com 0, 18, 21 e 24 h).
MALHA_15_MIN = np.arange(0.0, 24.0 + 1e-9, 0.25)


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoTrapezioTabela(unittest.TestCase):
    """Issue #11: integrar_tabela do trapézio deve usar a largura de cada intervalo."""

    def test_reta_em_malha_irregular(self):
        """A integral de x de 0 a 3, com pontos 0, 1, 3, dá 4,5 (o trapézio é exato para retas)."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0.0, 1.0, 3.0], [0.0, 1.0, 3.0]), 4.5)

    def test_vazao_constante_no_registro_com_falhas(self):
        """50 L/s constantes no registro real (com falhas) dão 50 · 24 = 1200 L/s·h, sem perder os buracos."""
        t, _ = vazao_registrada(3508)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.full(t.size, 50.0)), 1200.0)

    def test_tirar_um_ponto_de_uma_reta_nao_muda_nada(self):
        """Em y = 2x + 1, tirar o ponto do meio da malha não altera a integral (= 20 em [0, 4])."""
        x = np.linspace(0.0, 4.0, 9)
        sem_um = np.delete(x, 4)
        regra = Trapezio()
        self.assertAlmostEqual(regra.integrar_tabela(x, 2 * x + 1), 20.0)
        self.assertAlmostEqual(regra.integrar_tabela(sem_um, 2 * sem_um + 1), 20.0)




class TestContratoAjustarPolinomio(unittest.TestCase):
    """Issue #10: regras de ajustar_polinomio que os testes de aceitação não verificam."""

    def test_grau_negativo_e_tamanhos_diferentes(self):
        """grau < 0, x e y de tamanhos diferentes e x 2D são ValueError."""
        casos = [([0.0, 1.0], [1.0, 2.0], -1), ([0.0, 1.0, 2.0], [1.0, 2.0], 1),
                 ([[0.0, 1.0], [2.0, 3.0]], [1.0, 2.0], 1)]
        for x, y, grau in casos:
            with self.subTest(grau=grau, n=len(x)), self.assertRaises(ValueError):
                ajustar_polinomio(x, y, grau)

    def test_grau_zero_e_a_media(self):
        """O polinômio constante de mínimos quadrados é a média de y."""
        y = [3.0, 5.0, 10.0, 2.0]
        self.assertTrue(np.allclose(ajustar_polinomio([0.0, 1.0, 2.0, 3.0], y, 0), [np.mean(y)]))

    def test_recupera_cubica_exata(self):
        """Dados sem ruído de 1 - 2x + 0,5x³ devolvem exatamente esses coeficientes."""
        x = np.linspace(-3.0, 3.0, 13)
        coef = ajustar_polinomio(x, 1 - 2 * x + 0.5 * x ** 3, 3)
        self.assertTrue(np.allclose(coef, [1.0, -2.0, 0.0, 0.5], atol=1e-12))

    def test_x_repetidos_nao_determinam_o_polinomio(self):
        """Cinco pontos com só dois x distintos não determinam uma parábola: ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([1.0, 1.0, 1.0, 2.0, 2.0], [1.0, 1.1, 0.9, 2.0, 2.1], 2)


class TestContratoDiaDeOperacao(unittest.TestCase):
    """Issue #10: regras de dia_de_operacao que os testes de aceitação não verificam."""

    def test_falta_limite_de_faixa(self):
        """Sem a leitura das 21 h (fim da ponta), as faixas não podem ser separadas: ValueError."""
        t = MALHA_15_MIN[MALHA_15_MIN != 21.0]
        with self.assertRaisesRegex(ValueError, "21"):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_rendimento_nao_positivo_propaga(self):
        """Uma curva de rendimento que zera numa vazão do registro faz o ValueError da potência subir."""
        vazao = np.full(MALHA_15_MIN.size, 50.0)
        with self.assertRaises(ValueError):
            dia_de_operacao(MALHA_15_MIN, vazao, [40.0], [1.0, -0.02], Trapezio())   # η(50) = 0

    def test_com_simpson_em_malha_uniforme(self):
        """Com Simpson na malha de 15 min, as faixas têm nº ímpar de pontos e o custo soma as faixas."""
        vazao = 45.0 + 15.0 * np.sin(2 * np.pi * (MALHA_15_MIN - 12.0) / 24.0)
        simpson = dia_de_operacao(MALHA_15_MIN, vazao, [45.0, 0.0, -0.0022], [0.0, 0.0214, -0.000153], Simpson())
        trapezio = dia_de_operacao(MALHA_15_MIN, vazao, [45.0, 0.0, -0.0022], [0.0, 0.0214, -0.000153], Trapezio())
        self.assertAlmostEqual(simpson.custo_reais, sum(simpson.custo_por_faixa))
        self.assertAlmostEqual(simpson.volume_m3, 3.6 * 45.0 * 24.0, delta=0.01)   # o seno integra a 0
        self.assertAlmostEqual(simpson.energia_kwh, trapezio.energia_kwh, delta=0.01 * trapezio.energia_kwh)

    def test_energia_e_a_soma_das_faixas_no_trapezio(self):
        """No trapézio, a energia do dia é igual à soma das energias das três faixas (custo / tarifa)."""
        t, vazao = vazao_registrada(3508)
        resumo = dia_de_operacao(t, vazao, [45.0, 0.0, -0.0022], [0.0, 0.0214, -0.000153], Trapezio())
        energias = [c / tarifa for c, tarifa in zip(resumo.custo_por_faixa, (0.50, 1.50, 0.50))]
        self.assertAlmostEqual(resumo.energia_kwh, sum(energias))


if __name__ == "__main__":
    unittest.main()

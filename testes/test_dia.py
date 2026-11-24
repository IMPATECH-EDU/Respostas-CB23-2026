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
from fornecido.simulador import verdade_dia

MATRICULA = 3503
T = np.arange(0.0,24.0 + 1e-9, 1.5)

class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioMalhaIrregularRegressao(unittest.TestCase):
    """Issue #11: Trapezio.integrar_tabela usava a largura do 1º intervalo em todos os outros."""
    def test_reta_em_malha_irregular(self):
        """Em x = 0, 1, 3, 4 (passos 1, 2 e 1) o trapézio integra 2x + 1 exatamente: 20."""
        x = np.array([0.0, 1.0, 3.0, 4.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2 * x + 1), 20.0)

    def test_pontos_perdidos_nao_mudam_a_integral_de_uma_reta(self):
        """Tirar leituras do meio da tabela não muda a integral de uma função linear."""
        x = np.arange(0.0, 24.0 + 1e-9, 0.25)
        y = 40.0 + x
        exato = 40.0 * 24.0 + 24.0 ** 2 / 2
        manter = np.setdiff1d(np.arange(x.size), [5, 6, 30, 31, 60, 77]) # lacunas no registro
        self.assertAlmostEqual(Trapezio().integrar_tabela(x[manter], y[manter]), exato)

    def test_volume_do_dia_com_registro_falho(self):
        """O caso do relato: com 8 leituras perdidas, o volume fica a menos de 1,5% da conferência."""
        t, q = vazao_registrada(MATRICULA)
        volume = 3.6 * Trapezio().integrar_tabela(t, q)
        self.assertLess(abs(volume / verdade_dia()["volume_m3"] - 1), 0.015)

    def test_malha_uniforme_continua_igual(self):
        """Em malha uniforme o resultado não muda: h * (y0/2 + meio + yn/2)."""
        x = np.linspace(0.0, 2.0, 9)
        y = x ** 2
        esperado = 0.25 * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), esperado)

class TestAjustarPolinomioContrato(unittest.TestCase):
    """Issue #10: regras de `ajustar_polinomio` que os testes de aceitação não verificam."""
    def test_x_e_y_de_tamanhos_diferentes(self):
        """x e y com tamanhos diferentes levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_grau_negativo(self):
        """Um grau negativo levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)

    def test_pontos_igual_a_coeficientes_interpola(self):
        """Com len(x) == grau + 1 não há erro: o polinômio passa exatamente pelos pontos."""
        x, y = [0.0, 1.0, 2.0], [1.0, 0.0, 3.0]
        coef = ajustar_polinomio(x, y, 2)
        self.assertTrue(np.allclose(np.polynomial.polynomial.polyval(x, coef), y))

class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Issue #10: regras de `dia_de_operacao` que os testes de aceitação não verificam."""
    def test_limite_de_faixa_ausente(self):
        """Sem a leitura das 18 h na malha, dia_de_operacao levanta ValueError."""
        t = T[T != 18.0]
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_simpson_em_malha_uniforme(self):
        """Com malha uniforme e pontos ímpares por faixa, o Simpson dá o mesmo balanço do trapézio."""
        vazao = np.full(T.size, 50.0)
        com_trapezio = dia_de_operacao(T, vazao, [40.0], [0.8], Trapezio())
        com_simpson = dia_de_operacao(T, vazao, [40.0], [0.8], Simpson())
        self.assertAlmostEqual(com_simpson.volume_m3, com_trapezio.volume_m3)
        self.assertAlmostEqual(com_simpson.energia_kwh, com_trapezio.energia_kwh)
        self.assertAlmostEqual(com_simpson.custo_reais, com_trapezio.custo_reais)

    def test_rendimento_nao_positivo(self):
        """Um rendimento zero levanta ValueError (vem de potencia_eletrica)."""
        with self.assertRaises(ValueError):
            dia_de_operacao(T, np.full(T.size, 50.0), [40.0], [0.0], Trapezio())


if __name__ == "__main__":
    unittest.main()

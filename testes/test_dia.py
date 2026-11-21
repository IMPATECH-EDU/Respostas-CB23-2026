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

class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestTrapezioRegressao(unittest.TestCase):
    """Testes de regressão da issue #11 para `Trapezio.integrar_tabela` em malha irregular."""

    def test_trapezio_malha_irregular_funcao_linear(self):
        """Regressão #11: trapézio em malha não uniforme integra função linear exatamente."""
        x = np.array([0.0, 0.25, 0.5, 1.0, 2.0])
        y = 2.0 * x + 1.0
        # Integral exata de (2x + 1) em [0, 2] = [x^2 + x]_0^2 = 6.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, y), 6.0, places=12)

    def test_trapezio_registro_scada_com_falhas_funcao_constante(self):
        """Regressão #11: vazão constante de 50 L/s nas timestamps irregulares do SCADA dá 1200 L·h."""
        t, _ = vazao_registrada(3544)
        q_constante = np.full_like(t, 50.0)
        # De 0h a 24h com 50 L/s constantes, a integral exata é 50 * 24 = 1200.0
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, q_constante), 1200.0, places=10)


class TestDiaContrato(unittest.TestCase):
    """Testes de casos de borda do contrato de `ajustar_polinomio` e `dia_de_operacao`."""

    def test_ajustar_polinomio_poucos_pontos_ou_grau_negativo(self):
        """Menos pontos que grau + 1 ou grau negativo levanta ValueError."""
        x = np.array([0.0, 1.0, 2.0])
        y = np.array([1.0, 3.0, 5.0])
        with self.assertRaises(ValueError):
            ajustar_polinomio(x, y, grau=3)
        with self.assertRaises(ValueError):
            ajustar_polinomio(x, y, grau=-1)

    def test_dia_de_operacao_limite_faixa_ausente(self):
        """Ausência de algum limite de faixa tarifária (ex.: 18 h) em `t` levanta ValueError."""
        t = np.array([0.0, 6.0, 12.0, 21.0, 24.0])  # falta 18.0
        q = np.full_like(t, 60.0)
        coef_h = np.array([40.0, -0.05])
        coef_eta = np.array([0.75])
        with self.assertRaises(ValueError):
            dia_de_operacao(t, q, coef_h, coef_eta, Trapezio())

if __name__ == "__main__":
    unittest.main()

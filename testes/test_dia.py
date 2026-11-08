"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.integracao import Simpson, Trapezio
from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from fornecido.energia import FAIXAS_TARIFARIAS
import numpy as np


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestAjustarPolinomio(unittest.TestCase):
    """Teste de regressão para a função ajustar_poolinomio."""
    def test_grau_negativo(self):
        """Verifica se a função levanta ValueError quando o grau inserido é menor que 0."""
        with self.assertRaisesRegex(ValueError, r"grau deve ser maior"):
            ajuste = ajustar_polinomio([0.0, 1.0, 2.0, 3.0], [1.0, 3.0, 5.0, 7.0], -1)

class TestDiaDeOperacao(unittest.TestCase):
    """Teste de regressão para a função dia_de_operacao."""
    def test_faixas_tarifarias(self):
        """Verifica se a função levanta ValueError quando inserimos tempos que não cobrem os pontos das tarifas tarifárias."""
        with self.assertRaisesRegex(ValueError, r"O limite"):
            t = np.array([0.0, 1.0, 2.0, 4.0, 5.0, 6.0, 15.0, 16.0, 17.0, 19.0, 21.0, 24.0])
            vazao = np.array([0 for i in range(len(t))])
            dia = dia_de_operacao(t, vazao, [2], [50], Trapezio())

class TestTrapezio(unittest.TestCase):
    """Testes de regressão para integrar_tabela com malhas não uniformes."""

    def test_malha_nao_uniforme(self):
        """Verifica se a integração funciona corretamente para malhas com intervalos desiguais."""
        # Criamos uma malha com passos não uniformes
        x = np.array([0.0, 1.0, 3.0])
        y = np.array([2.0, 2.0, 2.0])

        # Calculamos a integração
        resultado = Trapezio().integrar_tabela(x, y)

        # Verificamos se a integração ocorreu adequadamente
        self.assertAlmostEqual(
            resultado,
            6.0,
            places=5,
            msg="O cálculo ignorou o tamanho variável dos subintervalos.",
        )

    def test_falha_de_comunicacao_scada(self):
        """Verifica se o cálculo do volume é exato quando há lacunas de pontos (falha SCADA)."""
        # Criamos uma malha com passos não uniformes
        x = np.array([0.0, 0.25, 0.75, 1.0])
        y = np.array([10.0, 20.0, 20.0, 10.0])

        # Calculamos a integração
        resultado = Trapezio().integrar_tabela(x, y)

        # Verificamos se a integração ocorreu adequadamente
        self.assertAlmostEqual(
            resultado,
            17.5,
            places=5,
            msg="A falha de comunicação/lacuna de dados distorceu a soma das áreas.",
        )


if __name__ == "__main__":
    unittest.main()

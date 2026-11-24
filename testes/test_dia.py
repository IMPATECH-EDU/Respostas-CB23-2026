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

if __name__ == "__main__":
    unittest.main()

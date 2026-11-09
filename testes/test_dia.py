"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ResumoDia, ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoIssue11(unittest.TestCase):
    """Issue #11: o trapézio sobre tabelas deve respeitar a largura de cada subintervalo."""

    def test_trapezio_malha_irregular_reta(self):
        """Trapézio é exato para uma reta numa malha não uniforme (x = 0, 1, 3)."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2.0 * x + 1.0), 12.0)

    def test_trapezio_malha_irregular_constante(self):
        """A integral de uma constante é valor × (x[-1] - x[0]) mesmo com passos diferentes."""
        x = np.array([0.0, 0.25, 0.75, 1.0, 2.5, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, np.full(x.size, 4.0)), 12.0)

    def test_trapezio_registro_com_falhas(self):
        """No registro real (com falhas), o volume bate com a soma explícita dos trapézios."""
        t, q = vazao_registrada(3529)
        esperado = sum((t[i + 1] - t[i]) * (q[i] + q[i + 1]) / 2.0 for i in range(t.size - 1))
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, q), esperado)

    def test_trapezio_malha_uniforme_continua_correto(self):
        """Em malha uniforme o resultado não muda (sem regressão no caso que já funcionava)."""
        x = np.linspace(0.0, 2.0, 9)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x ** 2), 8.0 / 3.0, places=1)
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 3 * x + 1), 8.0)


class TestContratoAjuste(unittest.TestCase):
    """Regras do contrato de ajustar_polinomio que a aceitação não verifica."""

    def test_grau_negativo_e_tamanhos_invalidos(self):
        """Grau negativo, x e y de tamanhos diferentes ou não 1D levantam ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0, 3.0], -1)
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)
        with self.assertRaises(ValueError):
            ajustar_polinomio([[0.0, 1.0], [2.0, 3.0]], [[1.0, 2.0], [3.0, 4.0]], 1)

    def test_grau_zero_e_a_media(self):
        """O polinômio de grau 0 de mínimos quadrados é a média de y."""
        coef = ajustar_polinomio([0.0, 1.0, 2.0, 3.0], [1.0, 2.0, 6.0, 7.0], 0)
        self.assertTrue(np.allclose(coef, [4.0]))

    def test_interpolacao_com_pontos_justos(self):
        """Com len(x) == grau + 1 o ajuste passa exatamente pelos pontos (parábola exata)."""
        x = np.array([1.0, 2.0, 4.0])
        coef = ajustar_polinomio(x, 3.0 - 2.0 * x + 0.5 * x ** 2, 2)
        self.assertTrue(np.allclose(coef, [3.0, -2.0, 0.5]))


class TestContratoDia(unittest.TestCase):
    """Regras do contrato de dia_de_operacao que a aceitação não verifica."""

    def test_limite_de_faixa_ausente(self):
        """Se a leitura das 18 h não está em t, levanta ValueError."""
        t = np.array([0.0, 6.0, 12.0, 21.0, 24.0])
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_malha_irregular_no_balanco(self):
        """Com leituras faltando (malha irregular) o volume e o custo seguem o tempo real."""
        t = np.array([0.0, 3.0, 4.0, 18.0, 19.0, 21.0, 22.5, 24.0])
        vazao = np.full(t.size, 50.0)
        resumo = dia_de_operacao(t, vazao, [40.0], [0.8], Trapezio())
        potencia = 998.0 * 9.81 * 0.050 * 40.0 / (1000.0 * 0.8)
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * 50.0 * 24.0)
        self.assertAlmostEqual(resumo.custo_reais, potencia * 15.0)

    def test_simpson_recusa_registro_com_falhas(self):
        """Com o integrador Simpson, o registro com falhas é recusado (malha irregular)."""
        t, q = vazao_registrada(3529)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, q, [40.0], [0.8], Simpson())


if __name__ == "__main__":
    unittest.main()
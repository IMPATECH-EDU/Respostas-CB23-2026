"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import FAIXAS_TARIFARIAS


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestTrapezioRegressao(unittest.TestCase):
    """Regressões da issue #11 para integração em malhas irregulares."""

    def test_trapezio_constante_malha_irregular(self) -> None:
        """Uma constante mantém a área total com intervalos de larguras diferentes."""
        x = [0.0, 1.0, 3.0]
        y = [2.0, 2.0, 2.0]
        integral = Trapezio().integrar_tabela(x, y)
        # Área do retângulo: 2 * (3 - 0) = 6.
        self.assertAlmostEqual(integral, 6.0)

    def test_trapezio_reta_malha_irregular(self) -> None:
        """A reta y=x integra exatamente com intervalos de larguras 2, 1 e 3."""
        x = [0.0, 2.0, 3.0, 6.0]
        y = [0.0, 2.0, 3.0, 6.0]
        integral = Trapezio().integrar_tabela(x, y)
        # Integral de x entre 0 e 6: 6**2 / 2 = 18.
        self.assertAlmostEqual(integral, 18.0)


class TestAjustarPolinomioContrato(unittest.TestCase):
    """Casos do contrato de ajuste não cobertos pelos testes de aceitação."""

    def test_grau_zero_retorna_media(self) -> None:
        """O ajuste de grau zero retorna a média dos valores em um ndarray 1D."""
        coef = ajustar_polinomio([0.0, 1.0, 2.0], [2.0, 4.0, 9.0], 0)
        self.assertIsInstance(coef, np.ndarray)
        self.assertEqual(coef.shape, (1,))
        self.assertAlmostEqual(coef[0], 5.0)

    def test_rejeita_grau_negativo(self) -> None:
        """Um grau negativo levanta ValueError."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0], [1.0, 2.0], -1)

    def test_rejeita_vetores_invalidos(self) -> None:
        """Entradas 2D ou com tamanhos diferentes levantam ValueError."""
        casos = [
            ([[0.0, 1.0]], [1.0, 2.0]),
            ([0.0, 1.0], [[1.0, 2.0]]),
            ([0.0, 1.0], [1.0]),
        ]
        for x, y in casos:
            with self.subTest(x=x, y=y):
                with self.assertRaises(ValueError):
                    ajustar_polinomio(x, y, 0)

    def test_aceita_minimo_de_pontos(self) -> None:
        """Um ajuste de grau dois aceita exatamente três pontos."""
        coef = ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 6.0, 17.0], 2)
        self.assertTrue(np.allclose(coef, [1.0, 2.0, 3.0]))


class TestDiaDeOperacaoContrato(unittest.TestCase):
    """Casos do balanço diário não cobertos pelos testes de aceitação."""

    def test_rejeita_limite_tarifario_ausente(self) -> None:
        """A ausência de qualquer limite tarifário levanta ValueError."""
        t = np.array([0.0, 6.0, 12.0, 18.0, 19.0, 21.0, 24.0])
        limites = {limite for inicio, fim, _ in FAIXAS_TARIFARIAS
                   for limite in (inicio, fim)}
        for limite in sorted(limites):
            instantes = t[t != limite]
            with self.subTest(limite=limite):
                with self.assertRaises(ValueError):
                    dia_de_operacao(instantes, np.full(instantes.size, 50.0),
                                    [40.0], [0.8], Trapezio())

    def test_balanco_em_malha_irregular(self) -> None:
        """Vazão e potência lineares têm balanço exato mesmo em malha irregular."""
        t = np.array([0.0, 1.0, 18.0, 19.0, 21.0, 22.0, 24.0])
        resumo = dia_de_operacao(t, 40.0 + t, [40.0], [0.8], Trapezio())
        # P(t) = fator * (40 + t); sua integral é analítica em cada faixa.
        fator = 998.0 * 9.81 * 40.0 / (1e6 * 0.8)
        integral_vazao = 40.0 * 24.0 + 24.0 ** 2 / 2.0
        custos = tuple(tarifa * fator * (40.0 * (fim - inicio)
                                       + (fim ** 2 - inicio ** 2) / 2.0)
                       for inicio, fim, tarifa in FAIXAS_TARIFARIAS)
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * integral_vazao)
        self.assertAlmostEqual(resumo.energia_kwh, fator * integral_vazao)
        self.assertIsInstance(resumo.custo_por_faixa, tuple)
        self.assertTrue(np.allclose(resumo.custo_por_faixa, custos))
        self.assertAlmostEqual(resumo.custo_reais, sum(custos))

    def test_respeita_integrador_simpson(self) -> None:
        """Simpson integra a potência quadrática exatamente no dia e em cada faixa."""
        t = np.arange(0.0, 24.0 + 1e-9, 1.5)
        resumo = dia_de_operacao(t, t, [0.0, 1.0], [1.0], Simpson())
        # Q(t) = H(t) = t e rendimento unitário: P(t) = fator * t².
        fator = 998.0 * 9.81 / 1e6
        custos = tuple(tarifa * fator * (fim ** 3 - inicio ** 3) / 3.0
                       for inicio, fim, tarifa in FAIXAS_TARIFARIAS)
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * 24.0 ** 2 / 2.0)
        self.assertAlmostEqual(resumo.energia_kwh, fator * 24.0 ** 3 / 3.0)
        self.assertTrue(np.allclose(resumo.custo_por_faixa, custos))
        self.assertAlmostEqual(resumo.custo_reais, sum(custos))

    def test_rejeita_rendimento_nao_positivo(self) -> None:
        """Rendimento zero ou negativo propaga o ValueError da potência elétrica."""
        t = np.array([0.0, 18.0, 21.0, 24.0])
        for rendimento in (0.0, -0.2):
            with self.subTest(rendimento=rendimento):
                with self.assertRaises(ValueError):
                    dia_de_operacao(t, np.full(t.size, 50.0), [40.0],
                                    [rendimento], Trapezio())


if __name__ == "__main__":
    unittest.main()

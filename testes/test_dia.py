"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.integracao import Simpson


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)



from elevatoria.integracao import Trapezio


class TestTrapezioRegressao(unittest.TestCase):
    """Regressões da largura de cada intervalo da issue #11."""

    def test_constante_com_lacunas(self) -> None:
        """Uma constante integra corretamente com intervalos de larguras distintas."""
        area = Trapezio().integrar_tabela([0, 0.25, 1.5, 4], [7, 7, 7, 7])
        self.assertAlmostEqual(area, 28.0)

    def test_reta_com_primeiro_intervalo_largo(self) -> None:
        """O trapézio é exato para uma reta mesmo quando o primeiro passo é maior."""
        area = Trapezio().integrar_tabela([0, 3, 4, 4.5], [2, 8, 10, 11])
        self.assertAlmostEqual(area, 29.25)

import numpy as np
from elevatoria.dia import ajustar_polinomio, dia_de_operacao


class TestContratosDia(unittest.TestCase):
    """Contratos de ajuste e integração tarifária além dos casos de aceitação."""

    def test_ajuste_rejeita_dimensao_e_tamanho(self) -> None:
        """O ajuste rejeita vetores de comprimentos diferentes e entradas bidimensionais."""
        for x, y in [([0, 1, 2], [2, 3]), ([[0, 1]], [[2, 3]])]:
            with self.subTest(x=x, y=y), self.assertRaises(ValueError):
                ajustar_polinomio(x, y, 1)

    def test_ajuste_grau_negativo(self) -> None:
        """Um grau negativo não define o polinômio solicitado."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0, 1, 2], [2, 3, 4], -1)

    def test_ajuste_constante_media(self) -> None:
        """O ajuste de grau zero devolve a média dos valores observados."""
        coef = ajustar_polinomio([0, 1, 4, 7], [3, 9, 5, 11], 0)
        self.assertEqual(coef.shape, (1,))
        self.assertAlmostEqual(float(coef[0]), 7.0)

    def test_limites_tarifarios_ausentes(self) -> None:
        """Cada fronteira tarifária precisa ter sua própria leitura na tabela."""
        for limite in (0, 18, 21, 24):
            t = np.array([h for h in [0, 12, 18, 21, 24] if h != limite])
            with self.subTest(limite=limite), self.assertRaisesRegex(ValueError, "limite"):
                dia_de_operacao(t, np.full(t.size, 50.0), [40], [0.8], Trapezio())

    def test_custo_por_faixa_na_malha_irregular(self) -> None:
        """Vazão linear e potência proporcional permitem conferir as faixas analiticamente."""
        t = np.array([0, 2, 13, 18, 19, 21, 24], dtype=float)
        resumo = dia_de_operacao(t, 30 + t, [40], [0.8], Trapezio())
        fator = 998 * 9.81 * 40 / (1_000_000 * 0.8)
        esperado = []
        for inicio, fim, tarifa in [(0, 18, 0.5), (18, 21, 1.5), (21, 24, 0.5)]:
            integral = 30 * (fim - inicio) + (fim**2 - inicio**2) / 2
            esperado.append(tarifa * fator * integral)
        self.assertTrue(np.allclose(resumo.custo_por_faixa, esperado))
        self.assertAlmostEqual(resumo.custo_reais, sum(esperado))
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * (30 * 24 + 24**2 / 2))

    def test_rendimento_invalido_propaga_erro(self) -> None:
        """Rendimento não positivo é rejeitado pela função de potência fornecida."""
        with self.assertRaisesRegex(ValueError, "rendimento"):
            dia_de_operacao([0, 18, 21, 24], [50]*4, [40], [0], Trapezio())


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self) -> None:
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoTrapezio(unittest.TestCase):
    """Expõe o erro de assumir passo constante em dados irregulares."""

    def test_constante_em_malha_irregular(self) -> None:
        """Integra a constante 2 em [0, 3] com larguras 1 e 2."""
        self.assertAlmostEqual(Trapezio().integrar_tabela([0, 1, 3], [2, 2, 2]), 6.0)

    def test_reta_em_malha_irregular(self) -> None:
        """Integra 2x+1 em [0, 6] com larguras 2, 1 e 3."""
        x = np.array([0.0, 2.0, 3.0, 6.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, 2 * x + 1), 42.0)


class TestContratosDia(unittest.TestCase):
    """Cobre validações do ajuste e fronteiras das faixas tarifárias."""

    def test_grau_negativo(self) -> None:
        """Grau negativo levanta ValueError com mensagem explicativa."""
        with self.assertRaisesRegex(ValueError, "grau"):
            ajustar_polinomio([0, 1], [1, 2], -1)

    def test_vetores_incompativeis(self) -> None:
        """Matrizes e vetores de tamanhos diferentes não definem o ajuste."""
        for x, y in (([[0, 1]], [1, 2]), ([0, 1], [[1, 2]]), ([0, 1], [1])):
            with self.subTest(x=x, y=y), self.assertRaises(ValueError):
                ajustar_polinomio(x, y, 1)

    def test_ajuste_constante(self) -> None:
        """O ajuste de grau zero devolve a média das observações."""
        coeficientes = ajustar_polinomio([0, 1, 2], [2, 3, 7], 0)
        self.assertEqual(coeficientes.shape, (1,))
        self.assertAlmostEqual(float(coeficientes[0]), 4.0)

    def test_falta_limite_tarifario(self) -> None:
        """Cada limite 0, 18, 21 e 24 deve estar presente na tabela."""
        completo = np.array([0, 6, 12, 18, 20, 21, 23, 24], dtype=float)
        for limite in (0, 18, 21, 24):
            t = completo[completo != limite]
            with self.subTest(limite=limite), self.assertRaisesRegex(ValueError, "limite|faixa"):
                dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())

    def test_balanco_irregular_por_faixa(self) -> None:
        """Vazão linear em malha irregular preserva volume e custos analíticos."""
        t = np.array([0, 1, 5, 18, 19, 21, 24], dtype=float)
        q = 40 + t
        resumo = dia_de_operacao(t, q, [40.0], [0.8], Trapezio())
        # Potência = fator * (40+t); a primitiva da vazão é 40t+t²/2.
        fator = 998.0 * 9.81 * 40.0 / (1_000_000 * 0.8)
        integrais = [882.0, 178.5, 187.5]
        custos = fator * np.array(integrais) * [0.5, 1.5, 0.5]
        self.assertAlmostEqual(resumo.volume_m3, 3.6 * 1248.0)
        self.assertAlmostEqual(resumo.energia_kwh, fator * 1248.0)
        self.assertIsInstance(resumo.custo_por_faixa, tuple)
        self.assertTrue(np.allclose(resumo.custo_por_faixa, custos))
        self.assertAlmostEqual(resumo.custo_reais, float(custos.sum()))

    def test_propaga_rendimento_invalido(self) -> None:
        """Rendimento nulo propaga o ValueError da equipe de energia."""
        with self.assertRaisesRegex(ValueError, "rendimento"):
            dia_de_operacao([0, 18, 21, 24], [50] * 4, [40], [0], Trapezio())


if __name__ == "__main__":
    unittest.main()

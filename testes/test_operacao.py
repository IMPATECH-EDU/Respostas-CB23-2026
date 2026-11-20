"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook

RUGOSIDADE_RELATIVA = 0.15e-3 / 0.20


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton usava a derivada do ponto inicial em todas as iterações."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Em Re = 10⁴ o Newton resolve Colebrook em no máximo 6 iterações (antes levava 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_dois_converge_quadraticamente(self):
        """Em x² − 2 a partir de 1, o erro de cada passo é da ordem do quadrado do anterior."""
        resultado = Newton(tol=1e-12, df=lambda x: 2.0 * x).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertLessEqual(resultado.iteracoes, 6)
        erros = [abs(x - math.sqrt(2.0)) for x in resultado.historico[:4]]   # antes do arredondamento
        for anterior, seguinte in zip(erros, erros[1:]):
            self.assertLess(seguinte, anterior ** 2)       # e_{k+1} ≈ e_k² / (2√2) < e_k²

    def test_derivada_reavaliada_em_cada_aproximacao(self):
        """Com df fornecida, ela é chamada em cada aproximação, e não só no ponto inicial."""
        pontos = []

        def derivada(x: float) -> float:
            pontos.append(x)
            return 3.0 * x * x

        resultado = Newton(tol=1e-12, df=derivada).encontrar(lambda x: x ** 3 - 8.0, 1.0, 4.0)
        self.assertAlmostEqual(resultado.raiz, 2.0, places=10)
        self.assertEqual(len(set(pontos)), resultado.iteracoes)


if __name__ == "__main__":
    unittest.main()

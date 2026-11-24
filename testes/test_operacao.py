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


class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton calculava a derivada uma vez só."""

    def test_colebrook_re_1e4_em_poucas_iteracoes(self):
        """Re = 1e4 em Colebrook converge em até 6 iterações (antes: 10)."""
        _, resultado = fator_atrito_colebrook(1e4, RUGOSIDADE_RELATIVA, Newton(tol=1e-12))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_raiz_de_dois_em_poucas_iteracoes(self):
        """Em x² - 2, chega a 1e-12 em até 8 iterações (antes: 32)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 8)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=12)

    def test_derivada_e_avaliada_a_cada_iteracao(self):
        """`df` é chamada uma vez por iteração."""
        chamadas = []

        def df(x: float) -> float:
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertEqual(len(chamadas), resultado.iteracoes)
        self.assertGreater(len(chamadas), 1)

    def test_erro_cai_mais_rapido_que_linear(self):
        """Cada erro entre 1e-14 e 1e-2 é menor que o anterior elevado a 1,5."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        erros = [abs(x - math.sqrt(2.0)) for x in resultado.historico]
        pares = [(e, seguinte) for e, seguinte in zip(erros, erros[1:])
                 if e < 1e-2 and seguinte > 1e-14]
        self.assertGreaterEqual(len(pares), 2)
        for e, seguinte in pares:
            with self.subTest(erro=e):
                self.assertLess(seguinte, e ** 1.5)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# ---------------------------------------------------------------------------------------
# Issue #9: regressão do Newton (escritos antes da correção; falham no código original)
# ---------------------------------------------------------------------------------------
class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton precisa recalcular a derivada a cada iteração."""

    def test_raiz_de_dois_em_poucas_iteracoes(self):
        """x² − 2 a partir de x0 = 1 converge em até 6 iterações (com o defeito, 32)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertTrue(math.isclose(resultado.raiz, math.sqrt(2.0)))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_exata_tambem_e_reavaliada(self):
        """Com df fornecida, o Newton chama df em cada novo ponto, e não só no primeiro."""
        pontos = []

        def df(x: float) -> float:
            pontos.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertGreaterEqual(len(pontos), resultado.iteracoes)
        self.assertEqual(len(set(pontos)), len(pontos))

    def test_colebrook_do_relato(self):
        """O caso do relato: Colebrook com Re = 1e4 em até 6 iterações (com o defeito, 10)."""
        f, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertAlmostEqual(f, 0.03202, delta=5e-5)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_erro_cai_quadraticamente(self):
        """Perto da raiz, cada erro é no máximo da ordem do quadrado do anterior."""
        resultado = Newton(tol=1e-15).encontrar(lambda x: x * x - 2.0, 1.0, 2.0)
        erros = [abs(x - math.sqrt(2.0)) for x in resultado.historico]
        e_antes, e_depois = erros[1], erros[2]
        self.assertLess(e_depois, e_antes ** 2)


if __name__ == "__main__":
    unittest.main()
"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao, Newton
from elevatoria.operacao import ordem_convergencia

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TesteNRegressao(unittest.TestCase):
    """Regressão da issue #9: o Newton deve recalcular a derivada a cada iteração."""

    def test_converge_em_poucas_iteracoes(self):
        """Newton para x^3 - 2 em [0, 4] converge em até 8 iterações (com o defeito, 43)."""
        resultado = Newton().encontrar(lambda x: x**3 - 2.0, 0.0, 4.0)
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 8)
        self.assertAlmostEqual(resultado.raiz, 2.0 ** (1.0 / 3.0), places=8)

    def test_erro_cai_mais_que_linearmente(self):
        """Na convergência quadrática, a razão entre erros consecutivos encolhe a cada passo."""
        resultado = Newton().encontrar(lambda x: x * x - 4.0, 0.0, 10.0)
        erros = [abs(x - 2.0) for x in resultado.historico]
        self.assertLess(erros[3] / erros[2], 0.1)

    def test_derivada_e_calculada_a_cada_iteracao(self):
        """A derivada fornecida é chamada uma vez por iteração, e não só no ponto inicial."""
        chamadas = []

        def df(x):
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(df=df).encontrar(lambda x: x * x - 2.0, 1.0, 2.0)
        self.assertEqual(len(chamadas), resultado.iteracoes)

class TestOrdemConvergencia(unittest.TestCase):
    """Regras do contrato de ordem_convergencia que os testes de aceitação não verificam."""

    def test_ignora_erros_no_nivel_do_arredondamento(self):
        """Erros abaixo do piso (aqui, o erro zero final) não entram na estimativa."""
        p = ordem_convergencia([1.1, 1.01, 1.0001, 1.00000001, 1.0], 1.0)
        self.assertAlmostEqual(p, 2.0, places=3)

    def test_menos_de_tres_erros_acima_do_piso(self):
        """Com menos de 3 erros acima do piso, a função levanta ValueError."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1.1, 1.01, 1.0], 1.0)

if __name__ == "__main__":
    unittest.main()

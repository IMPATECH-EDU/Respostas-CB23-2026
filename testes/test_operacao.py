"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9."""

    def test_newton_recalcula_derivada_a_cada_iteracao(self):
        """Regressão #9: a derivada não pode ser congelada no primeiro chute."""
        from elevatoria.raizes import Newton
        chamadas = []
        def derivada(x):
            chamadas.append(x)
            return 2.0 * x
        resultado = Newton(tol=1e-12, df=derivada).encontrar(lambda x: x*x - 2.0, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertGreater(len(chamadas), 1)
        self.assertAlmostEqual(resultado.raiz, 2.0 ** 0.5, places=11)

    def test_newton_converge_quadraticamente_em_raiz_simples(self):
        """Regressão #9: com derivada atualizada, Newton chega à raiz em poucas iterações."""
        from elevatoria.raizes import Newton
        resultado = Newton(tol=1e-12).encontrar(lambda x: x*x - 2.0, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 7)

    def test_ordem_convergencia_descarta_erros_abaixo_do_piso(self):
        """Erros no nível do arredondamento não entram na estimativa da ordem."""
        from elevatoria.operacao import ordem_convergencia
        historico = [1.1, 1.01, 1.0001, 1.0 + 1e-8, 1.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 1.0), 2.0, delta=0.05)

    def test_ordem_convergencia_rejeita_historico_insuficiente(self):
        """A estimativa exige pelo menos três erros acima do piso."""
        from elevatoria.operacao import ordem_convergencia
        with self.assertRaises(ValueError):
            ordem_convergencia([1.0, 1.0 + 1e-16], 1.0)

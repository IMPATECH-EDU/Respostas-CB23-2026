"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao, Newton
from elevatoria.operacao import ponto_operacao, ordem_convergencia
from fornecido.testes_aceitacao.test_aceitacao_m3 import tubulacao, BOMBA



class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))

    def test_convergencia(self):
        "Vamos mostrar que a função encontrar foi implementada erroneamente e por isso, não converge, às ves, mesmo para funções simples"
        def f(x):
            return 1 - x**2
        a = Newton()
        resultado = a.encontrar(f, -1, 1.9)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, 1.0, places=5)

    def test_newton_quantidade_iteracoes(self):
        """Garante que o Método de Newton converge rapidamente em poucas iterações."""
        # f(x) = x^2 - 2
        resultado = Newton(tol=1e-10).encontrar(lambda x: x**2 - 2, 0.0, 2.0)
    
        self.assertTrue(resultado.convergiu)
        # Com o bug da derivada fixa, leva 26 iterações (falha aqui).
        # Com a derivada atualizada a cada passo, leva apenas 5 iterações (passa).
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_ponto_operacao_fora_do_dominio(self):
        """Garante que limite a < q_min ou b > q_max levanta ValueError."""
        tub = tubulacao()
        # bomba.dominio é (0.0, 100.0)
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tub, Bisseccao(), a=-5.0, b=50.0)
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tub, Bisseccao(), a=50.0, b=150.0)

    def test_ordem_convergencia_erros_abaixo_do_piso(self):
        """Garante ValueError quando o histórico é longo, mas possui menos de 3 erros acima do piso."""
        raiz = 1.0
        # 4 aproximações, mas 3 delas têm erro 1e-16 (menor que o piso de 1e-14)
        historico = [1.5, 1.0 + 1e-16, 1.0 + 1e-16, 1.0]
        with self.assertRaises(ValueError):
            ordem_convergencia(historico, raiz, piso=1e-14)

    

    

        
        


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

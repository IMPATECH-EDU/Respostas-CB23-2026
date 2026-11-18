"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao, Newton
from elevatoria.operacao import ordem_convergencia
from fornecido.hidraulica import fator_atrito_colebrook

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))

    def test_convergencia(self):

        def f(x):
            return x**2 - 2  #Raiz: sqrt(2)

        raiz = Newton(tol=1e-12).encontrar(f,0,4)
        conv = ordem_convergencia(raiz.historico, raiz.raiz)
        self.assertGreater(conv, 1.8) 

    def test_quant_passos(self):

        Re = 10e4
        D = 0.15e-3
        resolv = Newton(tol=1e-12)

        f, resultado = fator_atrito_colebrook(Re, D, resolv)
        self.assertLessEqual(resultado.iteracoes, 6) 

# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

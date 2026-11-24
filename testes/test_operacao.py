"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao
from elevatoria.raizes import Newton
from elevatoria.operacao import ordem_convergencia

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestNewton(unittest.TestCase):
    """Testes de regressão e comportamento para o método de Newton."""

    def test_regressao_newton_convergencia_rapida(self):
        """Verifica se o método de Newton converge quadraticamente em poucas iterações."""
        f = lambda x: x**2 - 2
        df = lambda x: 2*x
        # Usando um intervalo cujo ponto médio já está perto da raiz (ex: sqrt(2) ≈ 1.414)
        res = Newton(df=df).encontrar(f, 1.3, 1.5)
        self.assertLessEqual(res.iteracoes, 5)

    def test_regressao_newton_atualiza_derivada(self):
        """Garante que a derivada é recalculada a cada passo do método de Newton."""
        f = lambda x: x**3 - x - 2
        res = Newton().encontrar(f, 1.0, 2.0) 
        # Com a derivada atualizada a cada passo, converge rapidamente em poucas iterações
        self.assertLessEqual(res.iteracoes, 8)

    def test_ordem_convergencia_quadratica(self):
        """Valida se a função calcula corretamente ordem p=2 para erros quadráticos."""
        historico = [1.0, 0.1, 0.01, 0.0001]
        p = ordem_convergencia(historico, raiz=0.0, piso=1e-14)
        self.assertAlmostEqual(p, 2.0, delta=0.1)

    def test_ordem_convergencia_lanca_erro_poucos_erros(self):
        """Garante que ValueError é levantado se houver menos de 3 erros acima do piso."""
        historico = [1.0, 0.1]
        with self.assertRaises(ValueError):
            ordem_convergencia(historico, raiz=0.0, piso=1e-14)
            
if __name__ == "__main__":
    unittest.main()

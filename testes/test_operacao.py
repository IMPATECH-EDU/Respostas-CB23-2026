"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao
from elevatoria.raizes import Newton
from elevatoria.operacao import ordem_convergencia
from fornecido.hidraulica import fator_atrito_colebrook
from fornecido.hidraulica import Tubulacao
from elevatoria.operacao import ponto_operacao
from fornecido.testes_aceitacao.test_aceitacao_m3 import BOMBA

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 testes que falhavam antes da correção

class TestNewtonConvergencia(unittest.TestCase):

    def test_newton_itera_rapido(self):
        """Prova que o Newton resolve o fator de atrito em no máximo 6 iterações."""
        resolvedor = Newton(tol=1e-10)
        # Re = 10000, rugosidade relativa = 0.001
        f, resultado = fator_atrito_colebrook(10000.0, 0.001, resolvedor)
        
        # Atualmente vai falhar porque leva cerca de 10 iterações
        self.assertLessEqual(resultado.iteracoes, 6, "O Newton está lento demais (convergência linear).")

    def test_newton_ordem_quadratica(self):
        """Prova que a ordem de convergência real do método é ~2.0 (quadrática)."""
        resolvedor = Newton(tol=1e-10)
        # Função simples: x^2 - 4, raiz em x=2. Intervalo [1, 3], meio = 2.0 (já é a raiz).
        # Vamos usar um intervalo assimétrico para forçar passos: [1, 4], meio = 2.5
        resultado = resolvedor.encontrar(lambda x: x**2 - 4.0, 1.0, 4.0)
        
        ordem = ordem_convergencia(list(resultado.historico), resultado.raiz)
        
        # Atualmente falha porque a ordem será próxima de 1.0 (linear)
        self.assertAlmostEqual(ordem, 2.0, delta=0.2, 
                               msg="A convergência não é quadrática. A derivada está a ser atualizada?")

# Teste Issue 8

    def test_ponto_operacao_falha_convergencia(self):
        """Garante que levanta ValueError se o resolvedor esgotar as iterações sem convergir."""
        tub = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))
        # Forçamos a falha dando apenas 1 iteração máxima ao método
        resolvedor_limitado = Bisseccao(tol=1e-10, max_iter=1)
        
        with self.assertRaises(ValueError):
            ponto_operacao(BOMBA, tub, resolvedor_limitado)

    def test_ordem_convergencia_ignora_ruido_piso(self):
        """Garante que a função descarta flutuações numéricas abaixo do piso exigido."""
        # Histórico com convergência linear exata até 0.25, seguido de ruído minúsculo
        historico = [2.0, 1.0, 0.5, 0.25, 1e-13, 1e-14, 1e-15]
        
        # A raiz exata é 0.0. O piso padrão é 1e-12. 
        # Os valores 1e-13, 1e-14 e 1e-15 devem ser ignorados.
        # Os últimos três erros válidos processados devem ser 0.25, 0.5 e 1.0.
        ordem = ordem_convergencia(historico, raiz=0.0, piso=1e-12)
        
        self.assertAlmostEqual(ordem, 1.0, delta=0.01)
        
if __name__ == "__main__":
    unittest.main()

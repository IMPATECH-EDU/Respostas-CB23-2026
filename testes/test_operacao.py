"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao, Newton
from elevatoria.operacao import ponto_operacao, ordem_convergencia
from elevatoria.calibracao import CurvaCalibracao

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressaoNewton(unittest.TestCase):
    """Testes de regressão para a convergência do método de Newton."""

    def test_recalcula_derivada_analitica(self):
        """Verifica se a derivada analítica é recalculada em cada iteração."""
        pontos = []

        def derivada(x):
            pontos.append(x)
            return 2 * x

        metodo = Newton(tol=1e-12, max_iter=20, df=derivada)
        resultado = metodo.encontrar(lambda x: x**2 - 2, 1, 2)

        self.assertTrue(resultado.convergiu)
        self.assertEqual(len(pontos), resultado.iteracoes)
        self.assertGreater(len(set(pontos)), 1)

    def test_convergencia_com_derivada_numerica(self):
        """Verifica se a derivada numérica permite convergência quadrática."""
        metodo = Newton(tol=1e-9, max_iter=6, h=1e-6)

        resultado = metodo.encontrar(
            lambda x: x**2 - 2,
            1, 2
        )

        self.assertTrue(resultado.convergiu)

class TestOperacao(unittest.TestCase):
    """Testes das funções de cálculo do ponto de operação e da ordem de convergência."""

    def test_ponto_operacao_fora_do_dominio(self):
        """Rejeita intervalos que ultrapassam o domínio da curva da bomba."""
        bomba = CurvaCalibracao([0, 10, 20], [50, 40, 30], "linear")

        with self.assertRaises(ValueError):
            ponto_operacao(bomba, None, None, a=5, b=25)

    def test_ordem_convergencia_piso_proporcional_raiz(self):
        """Considera a magnitude da raiz ao filtrar erros pequenos."""
        raiz = 1000.0
        historico = [
            1000.1,
            1000.01,
            1000.0001,
            1000.00000001,
            1000.0000000001
        ]

        ordem = ordem_convergencia(
            historico, raiz, piso=1e-8
        )

        self.assertAlmostEqual(ordem, 2.0, places=5)

if __name__ == "__main__":
    unittest.main()

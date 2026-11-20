"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from elevatoria.calibracao import CurvaCalibracao
from fornecido.hidraulica import Tubulacao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))

# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9: convergência do método de Newton."""

    def test_newton_convergencia_quadratica(self):
        """Confirma que o método de Newton atinge ordem de convergência próxima de 2."""
        f = lambda x: x**2 - 2.0
        newton = Newton(tol=1e-12)
        res = newton.encontrar(f, 1.0, 2.0)
        ordem = ordem_convergencia(res.historico, res.raiz)
        self.assertGreater(ordem, 1.8)

    def test_newton_poucas_iteracoes(self):
        """Garante que a convergência quadrática reduz o número de iterações em relação à bissecção."""
        f = lambda x: x**2 - 2.0
        res_newton = Newton(tol=1e-12).encontrar(f, 1.0, 2.0)
        res_bissec = Bisseccao(tol=1e-12).encontrar(f, 1.0, 2.0)
        self.assertLess(res_newton.iteracoes, res_bissec.iteracoes / 2)

class TestPontoOperacao(unittest.TestCase):
    """Verifica o levantamento de erros em casos anormais do modulo operacao"""
    def test_ponto_operacao_a_maior(self):
        """Garante que, quando 'a' for maior que 'b' em 'ponto_operacao()', levantará erro"""
        with self.assertRaises(ValueError):
            funcao = ponto_operacao(
        CurvaCalibracao([-0.05, -0.2, 45.0], [0.0, 20.0, 10.0]),
        Tubulacao(15.0, 0.15, 0.15, 0.15, Bisseccao()),
        Newton(),
        2.0,
        1.0
        )

    def test_ordem_convergencia_menor_3(self):
        """Garante que, ao chamar 'ordem_convergencia()' com len(erros) < 3, levantará erro"""
        with self.assertRaises(ValueError):
            funcao = f = lambda x: x**2 - 2.0
            newton = Newton(tol=1e-12)
            res = newton.encontrar(f, 1.0, 2.0)
            ordem = ordem_convergencia([0.1], res.raiz)

if __name__ == "__main__":
    unittest.main()

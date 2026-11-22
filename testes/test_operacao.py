"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import Tubulacao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestTangenteDeNewton(unittest.TestCase):
    """Regressões para a inclinação usada em cada aproximação de Newton."""

    def test_segunda_tangente(self) -> None:
        """A segunda tangente de x²−2 tem inclinação 3, pois o novo ponto é 1,5."""
        metodo = Newton(df=lambda x: 2 * x)
        resultado = metodo.encontrar(lambda x: x*x - 2, 1.0, 3.0)
        self.assertAlmostEqual(resultado.historico[1], 1.5)
        self.assertAlmostEqual(resultado.historico[2], 17 / 12)

    def test_seis_passos_com_derivada_numerica(self) -> None:
        """Com a diferença central atualizada, seis passos bastam para chegar a √3."""
        metodo = Newton(tol=1e-10, max_iter=6)
        resultado = metodo.encontrar(lambda x: x*x - 3, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, 3**0.5, places=10)


class TestLimitesDaOperacao(unittest.TestCase):
    """Limites do ensaio, convergência do resolvedor e escala dos erros."""

    def setUp(self) -> None:
        """Cria uma curva decrescente e a tubulação com raiz dentro do ensaio."""
        self.bomba = CurvaCalibracao([10, 55, 100], [50, 40, 20], "linear")
        self.tubo = Tubulacao(0.20, 850.0, 0.00015, 18.0, Bisseccao())

    def test_passo_insuficiente(self) -> None:
        """Uma iteração de bissecção não autoriza reportar um ponto de operação."""
        with self.assertRaisesRegex(ValueError, "convergiu"):
            ponto_operacao(self.bomba, self.tubo, Bisseccao(max_iter=1))

    def test_extremo_fora_do_ensaio(self) -> None:
        """O limite inferior abaixo de 10 L/s ultrapassa o domínio da curva."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(self.bomba, self.tubo, Bisseccao(), a=9, b=80)

    def test_piso_relativo_entre_aproximacoes(self) -> None:
        """Com raiz 1000, o piso relativo 0,001 descarta inclusive o erro de uma unidade."""
        historico = [1016, 1001, 1008, 1000.5, 1004, 1000.125]
        self.assertAlmostEqual(ordem_convergencia(historico, 1000, piso=0.001), 1.0)


if __name__ == "__main__":
    unittest.main()

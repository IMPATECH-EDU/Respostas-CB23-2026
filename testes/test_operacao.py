"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from fornecido.hidraulica import Tubulacao

from elevatoria.raizes import Newton

from elevatoria.raizes import Bisseccao


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestNewton(unittest.TestCase):
    """Regressões da atualização da derivada."""

    def test_passo_quadratico_com_derivada_analitica(self) -> None:
        """O segundo passo usa a derivada no ponto recém-calculado."""
        resultado = Newton(df=lambda x: 2*x, max_iter=2).encontrar(
            lambda x: x*x - 2, 1.0, 3.0)
        self.assertAlmostEqual(resultado.historico[2], 17/12)

    def test_converge_com_poucas_iteracoes(self) -> None:
        """O Newton numérico converge em seis passos para a raiz de x² - 2."""
        resultado = Newton(max_iter=6).encontrar(lambda x: x*x - 2, 1.0, 3.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, 2**0.5)



class TestOperacaoValidacao(unittest.TestCase):
    """Casos de domínio e de arredondamento na estimativa de ordem."""

    def test_rejeita_intervalo_fora_da_bomba(self) -> None:
        """O intervalo pedido deve caber por inteiro na curva da bomba."""
        metodo = Bisseccao()
        bomba = CurvaCalibracao([10, 50, 100], [40, 32, 18])
        tubo = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, metodo)
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(bomba, tubo, metodo, a=9.0)

    def test_ordem_ignora_erros_abaixo_do_piso(self) -> None:
        """A estimativa usa as últimas três diferenças úteis mesmo com um zero."""
        historico = [1.0, 0.5, 0.25, 0.125, 0.0, 1e-15]
        self.assertAlmostEqual(ordem_convergencia(historico, 0.0), 1.0)


if __name__ == "__main__":
    unittest.main()

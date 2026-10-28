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



import math
from elevatoria.raizes import Newton


class TestNewtonRegressao(unittest.TestCase):
    """Regressões da atualização da derivada da issue #9."""

    def test_derivada_analitica_atualizada(self) -> None:
        """Newton analítico alcança sqrt(2) dentro de seis iterações."""
        resultado = Newton(tol=1e-12, max_iter=6, df=lambda x: 2*x).encontrar(
            lambda x: x*x - 2, 0.0, 2.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=12)

    def test_derivada_numerica_atualizada(self) -> None:
        """Newton numérico converge para a raiz cúbica dentro de seis iterações."""
        resultado = Newton(tol=1e-10, max_iter=6).encontrar(
            lambda x: x**3 - 7, 1.0, 4.0)
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, 7 ** (1/3), places=9)

from unittest.mock import Mock
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import ResultadoRaiz


class TestContratosOperacao(unittest.TestCase):
    """Intervalos, falha do resolvedor e seleção dos erros de convergência."""

    def test_intervalo_invertido_ou_vazio(self) -> None:
        """Limites iguais ou invertidos são rejeitados antes de chamar o resolvedor."""
        bomba = CurvaCalibracao([0, 50, 100], [50, 40, 20])
        resolvedor = Mock()
        for a, b in [(50, 50), (80, 20)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(bomba, Mock(), resolvedor, a, b)
        resolvedor.encontrar.assert_not_called()

    def test_intervalo_fora_do_dominio(self) -> None:
        """Nenhuma extremidade do intervalo pode ultrapassar o domínio da bomba."""
        bomba = CurvaCalibracao([0, 50, 100], [50, 40, 20])
        for a, b in [(-1, 80), (20, 101)]:
            with self.subTest(a=a, b=b), self.assertRaisesRegex(ValueError, "domínio"):
                ponto_operacao(bomba, Mock(), Mock(), a, b)

    def test_resolvedor_nao_converge(self) -> None:
        """Uma aproximação retornada sem convergência não vira ponto de operação."""
        bomba = CurvaCalibracao([0, 50, 100], [50, 40, 20])
        resolvedor = Mock()
        resolvedor.encontrar.return_value = ResultadoRaiz(50.0, 1, False, (50.0,))
        with self.assertRaisesRegex(ValueError, "não convergiu"):
            ponto_operacao(bomba, Mock(), resolvedor)

    def test_preserva_resultado_e_funcao(self) -> None:
        """A composição entrega bomba menos sistema e preserva o resultado do método."""
        bomba = CurvaCalibracao([0, 50, 100], [50, 40, 20])
        tubulacao = Mock()
        tubulacao.altura_sistema.return_value = 40.0
        resolvedor = Mock()
        resposta = ResultadoRaiz(50.0, 3, True, (55.0, 51.0, 50.0))
        resolvedor.encontrar.return_value = resposta
        ponto = ponto_operacao(bomba, tubulacao, resolvedor, 20, 80)
        funcao, a, b = resolvedor.encontrar.call_args.args
        self.assertAlmostEqual(funcao(50), 0.0)
        self.assertEqual((a, b), (20, 80))
        self.assertIs(ponto.resultado, resposta)
        self.assertAlmostEqual(ponto.altura, 40.0)

    def test_piso_escalado_pela_raiz(self) -> None:
        """O piso relativo filtra erros pequenos antes de selecionar os três últimos."""
        self.assertAlmostEqual(ordem_convergencia([1100, 1010, 1001, 1000.01],
                                                  1000, piso=1e-4), 1.0)

    def test_faltam_erros_apos_filtro(self) -> None:
        """Três aproximações não bastam se uma delas cai abaixo do piso relativo."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1100, 1010, 1000.01], 1000, piso=1e-4)


if __name__ == "__main__":
    unittest.main()

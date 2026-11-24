"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestRegressaoNewton(unittest.TestCase):
    """Verifica o progresso do Newton com derivadas analítica e numérica."""

    def test_segundo_passo_da_raiz_de_dois(self) -> None:
        """A tangente em 1,5 leva a 17/12 na segunda iteração."""
        resultado = Newton(df=lambda x: 2 * x).encontrar(lambda x: x*x - 2, 0, 2)
        self.assertAlmostEqual(resultado.historico[2], 17 / 12)

    def test_colebrook_em_cinco_iteracoes(self) -> None:
        """A derivada numérica atualizada resolve Colebrook em até cinco passos."""
        _, resultado = fator_atrito_colebrook(1e4, 0.00075, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 5)


class TestContratoOperacao(unittest.TestCase):
    """Casos de fronteira da estimativa da ordem e do ponto de operação."""

    def test_ordem_com_erros_em_escalas_extremas(self) -> None:
        """A ordem continua definida quando o quociente direto subflui."""
        ordem = ordem_convergencia([1e300, 1e-100, 1e-200], 0.0, piso=0.0)
        self.assertAlmostEqual(ordem, 0.25)

    def test_piso_relativo_exclui_igualdade(self) -> None:
        """O erro igual ao piso escalado pela raiz fica fora da estimativa."""
        historico = [144, 132, 104, 102]
        ordem = ordem_convergencia(historico, 100, piso=0.02)
        self.assertAlmostEqual(ordem, math.log(4 / 32) / math.log(32 / 44))

    def test_rejeita_resultado_sem_convergencia(self) -> None:
        """Uma aproximação obtida ao esgotar as iterações não é aceita."""
        bomba = CurvaCalibracao([0, 50, 100], [50, 40, 10], "linear")
        tubo = Tubulacao(0.2, 850, 0.00015, 18, Bisseccao())
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tubo, Bisseccao(max_iter=1))

    def test_intervalo_fora_do_dominio(self) -> None:
        """O intervalo inteiro precisa pertencer ao domínio antes de chamar Newton."""
        bomba = CurvaCalibracao([0, 50, 100], [50, 40, 10], "linear")
        tubo = Tubulacao(0.2, 850, 0.00015, 18, Bisseccao())
        with self.assertRaises(ValueError):
            ponto_operacao(bomba, tubo, Newton(), a=10, b=101)


if __name__ == "__main__":
    unittest.main()

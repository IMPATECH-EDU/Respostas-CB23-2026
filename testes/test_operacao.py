"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestNewtonRegressao(unittest.TestCase):
    """Dois testes de regressão para a issue #9."""

    def test_colebrook_re_1e4_em_ate_6_iteracoes(self):
        """Colebrook com Re = 1e4 e derivada numérica converge em até 6 iterações."""
        _, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_reavaliada_a_cada_iteracao(self):
        """Em x² - 2, partindo de 1, as iterações seguem a fórmula com f'(x_k) atual."""
        resultado = Newton(df=lambda x: 2.0 * x).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        for obtido, esperado in zip(resultado.historico, [1.0, 1.5, 17 / 12, 577 / 408]):
            self.assertAlmostEqual(obtido, esperado)


class TestContratoOperacao(unittest.TestCase):
    """Regras das docstrings de `elevatoria/operacao.py` que a aceitação não verifica."""

    def test_ponto_operacao_recusa_entradas_invalidas(self):
        """a >= b, [a, b] fora do domínio da bomba e não convergência levantam ValueError."""
        vazoes = [10.0 * k for k in range(11)]
        bomba = CurvaCalibracao(vazoes, [50.0 - 0.004 * q ** 2 for q in vazoes], "spline")
        tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))
        # Newton parte do ponto médio: só a validação de ponto_operacao barra os dois primeiros.
        casos = {"a >= b": (Newton(), 100.0, 10.0),
                 "fora do domínio": (Newton(), 10.0, 150.0),
                 "não convergiu": (Newton(max_iter=1), 10.0, 100.0)}
        for nome, (resolvedor, a, b) in casos.items():
            with self.subTest(nome), self.assertRaises(ValueError):
                ponto_operacao(bomba, tubulacao, resolvedor, a, b)

    def test_ordem_convergencia_piso_relativo_a_raiz(self):
        """O piso escala com |raiz|, mas nunca fica abaixo do valor absoluto de `piso`."""
        erros = [1e-2, 1e-3, 1e-4]
        # O último erro está abaixo do piso e deve ser ignorado, sobrando os erros lineares.
        for raiz, ultimo_erro in ((-1e6, 1e-9), (0.0, 1e-15)):
            with self.subTest(raiz=raiz):
                historico = [raiz + e for e in erros + [ultimo_erro]]
                self.assertAlmostEqual(ordem_convergencia(historico, raiz), 1.0, delta=0.01)


if __name__ == "__main__":
    unittest.main()

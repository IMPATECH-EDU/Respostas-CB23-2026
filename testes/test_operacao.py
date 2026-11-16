"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.operacao import ordem_convergencia
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestNewtonRegressao(unittest.TestCase):
    """Regressões da derivada congelada descrita na issue #9."""

    def test_aproximacoes_usam_derivada_no_ponto_atual(self) -> None:
        """Cada passo de Newton para x² − 2 usa a derivada da aproximação atual."""
        def f(x: float) -> float:
            return x * x - 2.0

        def f_prime(x: float) -> float:
            return 2.0 * x

        resultado = Newton(df=f_prime).encontrar(f, 1.0, 2.0)

        self.assertGreaterEqual(len(resultado.historico), 3)
        for atual, seguinte in zip(resultado.historico, resultado.historico[1:]):
            esperado = atual - (atual * atual - 2.0) / (2.0 * atual)
            self.assertAlmostEqual(seguinte, esperado, places=12)

    def test_colebrook_converge_em_ate_cinco_iteracoes(self) -> None:
        """Colebrook em Re = 10⁴ converge em até cinco passos com derivada numérica."""
        fator, resultado = fator_atrito_colebrook(1e4, 1e-4, Newton(tol=1e-10))
        referencia, _ = fator_atrito_colebrook(1e4, 1e-4, Bisseccao(tol=1e-12))
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(fator, referencia, places=10)
        self.assertLessEqual(resultado.iteracoes, 5)


class TestOrdemConvergencia(unittest.TestCase):
    """Casos de filtragem dos erros ausentes nos testes de aceitação."""

    def test_erro_igual_ao_piso_nao_conta(self) -> None:
        """Erro exatamente no piso é descartado, restando menos de três erros."""
        with self.assertRaises(ValueError):
            ordem_convergencia([8.0, 4.0, 2.0], raiz=0.0, piso=2.0)

    def test_piso_escalado_pelo_modulo_da_raiz(self) -> None:
        """Para raiz de módulo maior que um, o piso é multiplicado por esse módulo."""
        # O limiar é (1/16) * 16 = 1: só os erros 8, 4 e 2 contam.
        # Os erros 1/4 e 1/8 seriam incluídos se o piso não fosse escalado.
        historico = [24.0, 20.0, 18.0, 16.25, 16.125]
        ordem = ordem_convergencia(historico, raiz=16.0, piso=0.0625)
        self.assertAlmostEqual(ordem, 1.0, places=12)


if __name__ == "__main__":
    unittest.main()

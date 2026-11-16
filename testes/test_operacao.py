"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

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


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.raizes import Bisseccao
from elevatoria.operacao import ordem_convergencia


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestOrdemConvergenciaContrato(unittest.TestCase):
    def test_ignora_erros_abaixo_do_piso_relativo(self):
        """Descarta erros menores que o piso ajustado à magnitude da raiz."""
        historico = [1016.0, 1008.0, 1004.0, 1000.5]

        ordem = ordem_convergencia(historico, raiz=1000.0, piso=0.001)

        self.assertAlmostEqual(ordem, 1.0)

    def test_usa_os_tres_ultimos_erros_validos(self):
        """Estima a ordem usando os três últimos erros acima do piso."""
        historico = [0.8, 0.5, 0.25, 0.0625, 0.00390625]

        ordem = ordem_convergencia(historico, raiz=0.0)

        self.assertAlmostEqual(ordem, 2.0)

if __name__ == "__main__":
    unittest.main()

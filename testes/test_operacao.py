"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

# Importações para os testes
import numpy as np
from elevatoria.raizes import Bisseccao
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.raizes import MetodoRaiz, ResultadoRaiz
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from fornecido.hidraulica import Tubulacao


# Esse código foi tirado do test_aceitacao_m3.py por simplicidade
VAZOES = np.arange(0.0, 101.0, 10.0)
BOMBA = CurvaCalibracao(VAZOES, 50.0 - 0.004 * VAZOES ** 2, "spline")   # H = 50 - 0,004 Q²

def tubulacao() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestPontoOperacao(unittest.TestCase):
    """Teste da função ponto_operacao."""

    def test_intervalos_crescentes(self):
        """Verifica se a função retorna erro quando os intervalos não estão em ordem cresccente."""
        # Podemos usar o asserRaisesRegex, que verifica a resposta também, e assim diferenciamos os erros do 
        # PontoOperacao e do resolvedor em si.
        with self.assertRaisesRegex(ValueError, r"não é uma entrada válida"):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10), a=60.0, b=50.0)

    def test_intervalos_definidos(self):
        """Verifica se a função levanta erro quando os intervalos não estão contidos no domínio da bomba."""
        with self.assertRaisesRegex(ValueError, r"não está contido no domínio da bomba"):
            ponto_operacao(BOMBA, tubulacao(), Bisseccao(tol=1e-10), a = 120.0, b = 200.0)



if __name__ == "__main__":
    unittest.main()

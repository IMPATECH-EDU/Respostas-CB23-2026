"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

import numpy as np

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


class TestNewtonRegressao(unittest.TestCase):
    """Regressões da issue #9: derivada do método de Newton."""

    def test_newton_recalcula_derivada_da_raiz_quadratica(self):
        """Newton deve recalcular a derivada e convergir quadraticamente."""
        resultado = Newton(tol=1e-10, max_iter=10, df=lambda x: 2.0 * x).encontrar(
            lambda x: x * x - 2.0, 0.0, 2.0
        )
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=9)
        self.assertLessEqual(resultado.iteracoes, 5)

    def test_newton_avalia_derivada_em_cada_aproximacao(self):
        """A derivada fornecida deve ser avaliada em cada aproximação."""
        contador = [0]

        def derivada(x):
            contador[0] +=1
            return 2.0 * x

        resultado = Newton(tol=1e-10, max_iter=10, df=derivada).encontrar(
            lambda x: x * x - 2.0, 0.0, 2.0
        )
        self.assertTrue(resultado.convergiu)
        self.assertGreaterEqual(contador[0], 4)


class TestPontoOperacaoContrato(unittest.TestCase):
    """Regras do contrato não cobertas pelos testes de aceitação."""

    def setUp(self):
        vazoes = np.arange(0.0, 101.0, 10.0)
        self.bomba = CurvaCalibracao(
            vazoes, 50.0 - 0.004 * vazoes ** 2, "spline"
        )
        self.tubulacao = Tubulacao(
            0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12)
        )

    def test_intervalo_com_extremo_negativo_fica_fora_do_dominio(self):
        """O limite negativo do intervalo deve ser rejeitado pelo domínio da bomba."""
        with self.assertRaises(ValueError):
            ponto_operacao(
                self.bomba,
                self.tubulacao,
                Bisseccao(tol=1e-10),
                a=-1.0,
                b=50.0,
            )

    def test_piso_grande_deixa_menos_de_tres_erros_validos(self):
        """O piso personalizado deve descartar erros pequenos e exigir três erros válidos."""
        with self.assertRaises(ValueError):
            ordem_convergencia(
                [1.5, 1.1, 1.01, 1.001, 1.0],
                1.0,
                piso=0.1,
            )


if __name__ == "__main__":
    unittest.main()

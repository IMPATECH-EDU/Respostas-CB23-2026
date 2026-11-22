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
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook

#: Bomba de teste, H = 50 − 0,004·Q², ensaiada de 0 a 100 L/s.
_VAZOES = np.arange(0.0, 101.0, 10.0)
_BOMBA = CurvaCalibracao(_VAZOES, 50.0 - 0.004 * _VAZOES ** 2, "spline")


def _adutora() -> Tubulacao:
    """A adutora da estação, com a bissecção resolvendo Colebrook."""
    return Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# ---------------------------------------------------------------------------------------
# Issue #9: regressão do Newton (escritos antes da correção; falham no código original)
# ---------------------------------------------------------------------------------------
class TestRegressaoNewton(unittest.TestCase):
    """Issue #9: o Newton precisa recalcular a derivada a cada iteração."""

    def test_raiz_de_dois_em_poucas_iteracoes(self):
        """x² − 2 a partir de x0 = 1 converge em até 6 iterações (com o defeito, 32)."""
        resultado = Newton(tol=1e-12).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertTrue(math.isclose(resultado.raiz, math.sqrt(2.0)))
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_derivada_exata_tambem_e_reavaliada(self):
        """Com df fornecida, o Newton chama df em cada novo ponto, e não só no primeiro."""
        pontos = []

        def df(x: float) -> float:
            pontos.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-12, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 2.0)
        self.assertGreaterEqual(len(pontos), resultado.iteracoes)
        self.assertEqual(len(set(pontos)), len(pontos))

    def test_colebrook_do_relato(self):
        """O caso do relato: Colebrook com Re = 1e4 em até 6 iterações (com o defeito, 10)."""
        f, resultado = fator_atrito_colebrook(1e4, 0.15e-3 / 0.20, Newton(tol=1e-12))
        self.assertAlmostEqual(f, 0.03202, delta=5e-5)
        self.assertLessEqual(resultado.iteracoes, 6)

    def test_erro_cai_quadraticamente(self):
        """Perto da raiz, cada erro é no máximo da ordem do quadrado do anterior."""
        resultado = Newton(tol=1e-15).encontrar(lambda x: x * x - 2.0, 1.0, 2.0)
        erros = [abs(x - math.sqrt(2.0)) for x in resultado.historico]
        e_antes, e_depois = erros[1], erros[2]
        self.assertLess(e_depois, e_antes ** 2)


# ---------------------------------------------------------------------------------------
# Issue #8: regras do contrato que os testes de aceitação não verificam
# ---------------------------------------------------------------------------------------
class TestPontoOperacaoContrato(unittest.TestCase):
    """Issue #8: validações de ponto_operacao."""

    def test_intervalo_invertido(self):
        """a >= b levanta ValueError antes de chamar o resolvedor."""
        for a, b in [(60.0, 40.0), (50.0, 50.0)]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(_BOMBA, _adutora(), Bisseccao(), a=a, b=b)

    def test_intervalo_fora_do_dominio_da_bomba(self):
        """[a, b] que sai do domínio da bomba (0 a 100 L/s) levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            ponto_operacao(_BOMBA, _adutora(), Bisseccao(), a=10.0, b=120.0)

    def test_resolvedor_que_nao_converge(self):
        """Se o resolvedor para em max_iter sem convergir, ponto_operacao levanta ValueError."""
        with self.assertRaisesRegex(ValueError, "convergiu"):
            ponto_operacao(_BOMBA, _adutora(), Bisseccao(tol=1e-10, max_iter=3))


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Issue #8: o piso de ordem_convergencia é relativo ao tamanho da raiz."""

    def test_piso_escala_com_a_raiz(self):
        """Com raiz = 1000, um erro de ~1e-12 fica abaixo do piso (1e-11) e é ignorado."""
        raiz = 1000.0
        historico = [raiz + 1e-1, raiz + 1e-2, raiz + 1e-4, raiz + 1e-12, raiz]
        self.assertAlmostEqual(ordem_convergencia(historico, raiz), 2.0, delta=0.01)

    def test_erros_iguais_nao_tem_ordem(self):
        """Uma sequência parada (erros iguais) levanta ValueError, sem dividir por zero."""
        with self.assertRaises(ValueError):
            ordem_convergencia([2.0, 2.0, 2.0], 1.0)


if __name__ == "__main__":
    unittest.main()
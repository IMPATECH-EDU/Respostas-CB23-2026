"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import math

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self) -> None:
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #9 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoNewton(unittest.TestCase):
    """Confere a velocidade de convergência com derivada analítica e numérica."""

    def test_quadratica_com_derivada_analitica(self) -> None:
        """Newton encontra a raiz de x² - 2 em até seis iterações."""
        resultado = Newton(tol=1e-12, max_iter=6, df=lambda x: 2 * x).encontrar(
            lambda x: x * x - 2, 0.0, 2.0
        )
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2), places=11)

    def test_colebrook_com_derivada_numerica(self) -> None:
        """Colebrook em Re=1e4 converge em até seis iterações com diferença central."""
        fator, resultado = fator_atrito_colebrook(
            1e4, 0.15e-3 / 0.20, Newton(tol=1e-12, max_iter=6)
        )
        self.assertTrue(resultado.convergiu)
        self.assertAlmostEqual(fator, 0.03202, delta=5e-5)


class TestContratosOperacao(unittest.TestCase):
    """Cobre os limites do domínio, a não convergência e o piso dos erros."""

    def setUp(self) -> None:
        """Prepara a bomba e a tubulação com uma interseção no domínio."""
        self.bomba = CurvaCalibracao([0, 50, 100], [50, 40, 10], "spline")
        self.tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

    def test_intervalo_invertido_ou_vazio(self) -> None:
        """Intervalos invertidos e de largura zero levantam ValueError."""
        for a, b in ((50.0, 40.0), (50.0, 50.0)):
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(self.bomba, self.tubulacao, Newton(), a, b)

    def test_intervalo_fora_do_dominio(self) -> None:
        """Recusa cada extremo fora do domínio antes de chamar Newton."""
        for a, b in ((-1.0, 100.0), (10.0, 101.0)):
            with self.subTest(a=a, b=b), self.assertRaisesRegex(ValueError, "domínio"):
                ponto_operacao(self.bomba, self.tubulacao, Newton(), a, b)

    def test_resolvedor_sem_convergencia(self) -> None:
        """Um resultado sem convergência não pode virar ponto de operação."""
        with self.assertRaisesRegex(ValueError, "converg"):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(max_iter=1))

    def test_piso_relativo_e_igualdade(self) -> None:
        """O piso usa o módulo da raiz e exclui erros iguais ao limite."""
        for raiz in (1000.0, -1000.0):
            historico = [raiz + erro for erro in (16, 8, 4, 1, 0.5, 0)]
            with self.subTest(raiz=raiz):
                self.assertAlmostEqual(ordem_convergencia(historico, raiz, piso=0.001), 1.0)

    def test_poucos_erros_apos_filtrar(self) -> None:
        """Um histórico longo ainda é inválido se só dois erros superam o piso."""
        with self.assertRaises(ValueError):
            ordem_convergencia([1016, 1008, 1001, 1000.5, 1000], 1000.0, piso=0.001)


if __name__ == "__main__":
    unittest.main()

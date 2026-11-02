"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

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


class TestPontoOperacaoContrato(unittest.TestCase):
    """Validações do ponto de operação ausentes nos testes de aceitação."""

    def setUp(self) -> None:
        """Prepara uma curva de bomba e uma adutora com resolvedor de Colebrook."""
        self.bomba = CurvaCalibracao([0.0, 50.0, 100.0], [50.0, 40.0, 10.0])
        self.tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Bisseccao(tol=1e-12))

    def test_rejeita_intervalo_nao_crescente(self) -> None:
        """Intervalos com extremos iguais ou invertidos levantam ValueError."""
        for a, b in ((50.0, 50.0), (80.0, 40.0)):
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(self.bomba, self.tubulacao, Newton(), a=a, b=b)

    def test_rejeita_intervalo_fora_do_dominio(self) -> None:
        """Cada extremidade do intervalo deve pertencer ao domínio da bomba."""
        for a, b in ((-1.0, 90.0), (10.0, 101.0)):
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                ponto_operacao(self.bomba, self.tubulacao, Newton(), a=a, b=b)

    def test_rejeita_resultado_sem_convergencia(self) -> None:
        """Atingir max_iter sem convergir impede devolver um ponto de operação."""
        with self.assertRaises(ValueError):
            ponto_operacao(self.bomba, self.tubulacao, Bisseccao(max_iter=1))


class TestOrdemConvergenciaContrato(unittest.TestCase):
    """Filtragem dos erros conforme o piso absoluto e a escala da raiz."""

    def test_descarta_erro_igual_ao_piso(self) -> None:
        """Erro exatamente no piso personalizado não conta entre os três válidos."""
        with self.assertRaises(ValueError):
            ordem_convergencia([0.5, 0.25, 0.125], 0.0, piso=0.125)

    def test_piso_considera_modulo_da_raiz(self) -> None:
        """Raízes grandes de ambos os sinais ampliam o piso pelo seu módulo."""
        for raiz in (1024.0, -1024.0):
            with self.subTest(raiz=raiz):
                historico = [raiz + erro for erro in (16.0, -8.0, 4.0, -2.0, 1.0, 0.0625, 0.0)]
                self.assertAlmostEqual(ordem_convergencia(historico, raiz, piso=1e-3), 1.0)

    def test_filtra_antes_de_escolher_ultimos_tres(self) -> None:
        """Erros pequenos intercalados são removidos sem reordenar os válidos."""
        historico = [0.5, 0.01, -0.25, 0.125, 0.0]
        self.assertAlmostEqual(ordem_convergencia(historico, 0.0, piso=0.02), 1.0)

    def test_rejeita_poucos_erros_apos_filtragem(self) -> None:
        """Um histórico longo também falha se menos de três erros superam o piso."""
        with self.assertRaises(ValueError):
            ordem_convergencia([0.5, 0.01, 0.005, 0.0], 0.0, piso=0.02)


if __name__ == "__main__":
    unittest.main()

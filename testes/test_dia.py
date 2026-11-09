"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.integracao import Simpson, Trapezio
from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from fornecido.energia import vazao_registrada
from fornecido.simulador import verdade_dia


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11.

class TestRegressaoIssue11(unittest.TestCase):
    """Testes de regressão para integração em malha irregular."""

    def test_trapezio_usa_largura_de_cada_intervalo(self):
        """Integra cada trecho com seu próprio espaçamento."""
        resultado = Trapezio().integrar_tabela([0.0, 1.0, 3.0], [0.0, 2.0, 2.0])
        self.assertAlmostEqual(resultado, 5.0)

    def test_volume_do_registro_com_falhas(self):
        """Mantém o volume do dia dentro da tolerância apesar das leituras perdidas."""
        t, vazao = vazao_registrada(123456)
        volume = 3.6 * Trapezio().integrar_tabela(t, vazao)
        referencia = verdade_dia()["volume_m3"]
        self.assertLess(abs(volume / referencia - 1.0), 0.015)


class TestContratosIssue10(unittest.TestCase):
    """Testes de contrato de ajustar_polinomio e dia_de_operacao."""

    def test_ajustar_polinomio_rejeita_vetores_de_tamanhos_diferentes(self):
        """Rejeita x e y com comprimentos diferentes."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 3.0], 1)

    def test_dia_de_operacao_rejeita_limite_de_faixa_ausente(self):
        """Rejeita um dia cuja malha não contém todos os limites tarifários."""
        t = [hora for hora in range(25) if hora != 18]
        vazao = [50.0] * len(t)
        with self.assertRaises(ValueError):
            dia_de_operacao(t, vazao, [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()

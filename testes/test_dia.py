"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


class TestTrapezioIrregular(unittest.TestCase):
    """Regressões de integração de registros com leituras perdidas."""

    def test_constante_com_lacuna(self) -> None:
        """Uma leitura ausente não encurta a duração de uma vazão constante."""
        resultado = Trapezio().integrar_tabela([0, 1, 3], [4, 4, 4])
        self.assertAlmostEqual(resultado, 12.0)

    def test_reta_com_primeiro_intervalo_maior(self) -> None:
        """A integral de y = x em [0, 4] vale oito mesmo com passos 3 e 1."""
        resultado = Trapezio().integrar_tabela([0, 3, 4], [0, 3, 4])
        self.assertAlmostEqual(resultado, 8.0)


class TestContratoDia(unittest.TestCase):
    """Casos de fronteira do ajuste e da integração por faixas."""

    def test_grau_zero(self) -> None:
        """O ajuste constante devolve um único coeficiente igual à média."""
        coef = ajustar_polinomio([0, 1, 2], [1, 2, 9], 0)
        self.assertEqual(coef.shape, (1,))
        self.assertAlmostEqual(coef[0], 4.0)

    def test_rejeita_matriz(self) -> None:
        """Uma tabela bidimensional de respostas não é um vetor de medições."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0, 1], [[1], [3]], 1)

    def test_limite_de_tarifa_ausente(self) -> None:
        """Cada fronteira tarifária precisa ter uma leitura registrada."""
        limites = np.array([0., 9., 18., 20., 21., 23., 24.])
        for hora in (0, 18, 21, 24):
            with self.subTest(hora=hora):
                t = limites[limites != hora]
                with self.assertRaises(ValueError):
                    dia_de_operacao(t, np.full(t.size, 50.), [40.], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()

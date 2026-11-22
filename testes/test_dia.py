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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestLarguraDosTrapezios(unittest.TestCase):
    """Regressões de integração na presença de leituras perdidas."""

    def test_constante_com_lacuna(self) -> None:
        """A área de uma constante conta também as horas da lacuna."""
        area = Trapezio().integrar_tabela([0, 1, 4], [2, 2, 2])
        self.assertAlmostEqual(area, 8.0)

    def test_reta_com_primeiro_passo_igual_ao_medio(self) -> None:
        """As larguras 2, 1 e 3 devem integrar 2t até 6 mesmo com média igual a 2."""
        area = Trapezio().integrar_tabela([0, 2, 3, 6], [0, 4, 6, 12])
        self.assertAlmostEqual(area, 36.0)


class TestEnsaioETarifas(unittest.TestCase):
    """Valida o ajuste e os limites das faixas tarifárias."""

    def test_grau_zero_da_a_media(self) -> None:
        """O melhor polinômio constante para 2, 9 e 4 vale 5."""
        coef = ajustar_polinomio([0, 1, 3], [2, 9, 4], 0)
        self.assertEqual(coef.shape, (1,))
        self.assertAlmostEqual(coef[0], 5.0)

    def test_coluna_nao_e_vetor(self) -> None:
        """Ter o mesmo número de elementos não torna uma matriz coluna um vetor 1D."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0, 1, 2], [[2], [9], [4]], 1)

    def test_leitura_em_cada_troca_de_tarifa(self) -> None:
        """Exige explicitamente as medições nos quatro limites das faixas."""
        limites = np.array([0, 18, 21, 24])
        for ausente in limites:
            t = limites[limites != ausente]
            with self.subTest(ausente=ausente), self.assertRaisesRegex(ValueError, "limite"):
                dia_de_operacao(t, np.full(t.size, 40.0), [30.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 4 (veja a seção 5 do ENUNCIADO_MARCO4.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

import numpy as np

from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from fornecido.energia import vazao_registrada
from marco1 import MATRICULA


class TestSimpsonExemplo(unittest.TestCase):
    """Exemplo do formato. `Simpson` é código existente da base."""

    def test_exato_para_parabola(self):
        """Simpson integra x² exatamente, mesmo com n = 2."""
        self.assertAlmostEqual(Simpson().integrar(lambda x: x ** 2, 0.0, 3.0, 2), 9.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #11 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestTrapezioRegressao(unittest.TestCase):
    """Regressão da issue #11: `Trapezio.integrar_tabela` precisa aceitar malha não uniforme."""

    def test_reta_em_malha_irregular(self):
        """O trapézio integra y = x exatamente em [0, 3], com passos 1 e 2 (área 4,5)."""
        x = np.array([0.0, 1.0, 3.0])
        self.assertAlmostEqual(Trapezio().integrar_tabela(x, x), 4.5)

    def test_constante_com_leitura_perdida(self):
        """Vazão constante de 2 com uma leitura perdida integra 2 × 1 h, e não menos."""
        t = np.array([0.0, 0.25, 0.75, 1.0])    # falta a leitura de 0,5 h
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, np.full(t.size, 2.0)), 2.0)

    def test_registro_do_dia_com_falhas(self):
        """No registro real do dia, com 8 leituras perdidas, o resultado bate com np.trapezoid."""
        t, q = vazao_registrada(MATRICULA)
        self.assertAlmostEqual(Trapezio().integrar_tabela(t, q), np.trapezoid(q, t))


class TestContratoDia(unittest.TestCase):
    """Regras do contrato de `ajustar_polinomio` e `dia_de_operacao` sem teste de aceitação."""

    def test_ajuste_com_tamanhos_diferentes(self):
        """x e y de tamanhos diferentes levantam ValueError (e não o TypeError do polyfit)."""
        with self.assertRaises(ValueError):
            ajustar_polinomio([0.0, 1.0, 2.0], [1.0, 2.0], 1)

    def test_limite_de_faixa_ausente(self):
        """Sem a leitura das 18 h, que separa duas faixas tarifárias, levanta ValueError."""
        t = np.array([0.0, 6.0, 12.0, 17.0, 19.0, 21.0, 24.0])
        with self.assertRaises(ValueError):
            dia_de_operacao(t, np.full(t.size, 50.0), [40.0], [0.8], Trapezio())


if __name__ == "__main__":
    unittest.main()

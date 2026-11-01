"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag

import numpy as np
from elevatoria.serie import SerieTemporal

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestRegressao(unittest.TestCase):
    """Testamos a função media_movel de SerieTemopral com o tamanho da serie resultante e o primeiro elemento calculado."""
    def test_primeiro_ponto(self):
        # Criamos a série
        arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        nova_serie = SerieTemporal.de_lista(arr)

        # Calculamos a média móvel
        janela = 2
        media = nova_serie.media_movel(janela)

        # 1. Teste de tamanho: 10 - 2 + 1 = 9 elementos
        self.assertEqual(len(media), len(arr) - janela + 1, "A média móvel devolveu um tamanho incorreto")

        # 2. Teste do primeiro elemento: (1 + 2) / 2 = 1.5
        self.assertEqual(media[0], 1.5,  "A média movel ignora o primeiro valor")


if __name__ == "__main__":
    unittest.main()

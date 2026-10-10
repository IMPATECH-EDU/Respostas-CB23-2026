"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np
from elevatoria.dados import por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestRegressionIssue4(unittest.TestCase):
    """Testes de regressão da issue #4 (média móvel)."""
    def test_media_movel_tamanho_correto(self):
        dados = np.arange(600, dtype=float)
        s = SerieTemporal.de_lista(dados)
        mm = s.media_movel(30)
        self.assertEqual(len(mm), 571)  # 600 - 30 + 1 = 571

    def test_media_movel_janela_um(self):
        """Média móvel com janela 1 deve retornar a própria série com mesmo tamanho."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        mm = s.media_movel(1)
        self.assertEqual(len(mm), 4)

if __name__ == "__main__":
    unittest.main()

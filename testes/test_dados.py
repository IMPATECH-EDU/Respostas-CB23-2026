"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag
from elevatoria.serie import SerieTemporal

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

# Testes - Média movel (Issue 4)

class TestMediaMovel(unittest.TestCase):
    def test_media_movel_simples(self):
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        resultado = s.media_movel(3)
        print("Resultado:", resultado)
        print("Tamanho:", len(resultado))
        
        # O resultado esperado para janelas de tamanho 3 na série [1, 2, 3, 4, 5] é [2.0, 3.0, 4.0] (tamanho 3)
        self.assertEqual(len(resultado), 3)




    def test2_media_movel_simples(self):
        x = SerieTemporal.de_lista([3.0, 5.0])
        resultado = x.media_movel(1)
        print("Resultado:", resultado)
        print("Tamanho:", len(resultado))
        # O resultado esperado para k = 1, é "ValueError"
        with self.assertRaises(ValueError):
            x.media_movel(0)

if __name__ == "__main__":
    unittest.main()

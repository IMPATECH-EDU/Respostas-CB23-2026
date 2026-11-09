"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np

from elevatoria.dados import por_tag, ler_log
from elevatoria.serie import SerieTemporal     

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestLerLog(unittest.TestCase):
    """Regras de contrato de ler_log"""

    def test_data_impossivel(self):
        """Dia 32 está no padrão, mas o strptime falha: a linha é inválida."""
        linha = "2026-10-32 08:00:00 INFO PT101 contagens=1"
        registros, invalidas = ler_log(linha + "\n")
        self.assertEqual((registros, invalidas), ([], [linha]))

    def test_resto_sem_par(self):
        """Linha sem chave=valor é considerada inválida."""
        linha = "2026-10-05 09:00:00 INFO PT101 sem_par_aqui"
        registros, invalidas = ler_log(linha + "\n")
        self.assertEqual((registros, invalidas), ([], [linha]))

    def test_linhas_vazias(self):
        """Linhas vazias são ignoradas."""
        texto = "\n   \n2026-10-05 10:00:00 INFO PT101 contagens=1\n\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])
    
class TestMediaMovelRegressao(unittest.TestCase):
    """Testes de regressão da issue #4 (média móvel)."""

    def test_quantidade_de_medias(self):
        """Série de 5 pontos com janela 2 deve devolver 4 valores (n-janela+1) de média móvel."""
        serie = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        self.assertEqual(len(serie.media_movel(2)), 4) #deve ser 4 termos: [1.5, 2.5, 3.5, 4.5]  

    def test_media_movel_janela_1(self):
        """Média móvel com janela 1 deve devolver a própria série."""
        serie = SerieTemporal.de_lista([10, 20, 30])
        self.assertTrue(np.allclose(serie.media_movel(1), [10, 20, 30]))

    def test_media_movel_valores(self):
        """Série de 5 pontos dada por [1,2,3,4,5] deve devolver [1.5, 2.5, 3.5, 4.5] em janela 2."""
        serie = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        self.assertTrue(np.allclose(serie.media_movel(2), [1.5, 2.5, 3.5, 4.5]))

class TestReamostrar(unittest.TestCase):
    """Testes de reamostragem."""

    def test_reamostrar_descarta_restante(self):
        """Descarta pontos que não completam um bloco."""
        serie = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        self.assertTrue(np.allclose(serie.reamostrar(5), [3.0])) # (1+2+3+4+5)/5=3.0

    def test_reamostrar_nao_modifica_serie(self):
        """A reamostragem não deve modificar a série original."""
        serie = SerieTemporal.de_lista([1, 2, 3, 4])
        serie.reamostrar(2)
        self.assertTrue(np.array_equal(serie, [1, 2, 3, 4])) 

if __name__ == "__main__":
    unittest.main()

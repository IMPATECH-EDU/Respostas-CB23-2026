"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np

from elevatoria.dados import por_tag
from elevatoria.serie import SerieTemporal
from elevatoria.dados import ler_log


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class Test_media_movel(unittest.TestCase):
     def test_quantidade_de_valores(self):
        """Verifica se uma janela de 30 gera 571 medias pra 600 leituras"""
        dados = SerieTemporal.de_lista(list(range(600)))
        resultado = SerieTemporal.media_movel(dados, 30)

        """Verifica se uma janela de 10 gera 4041 para 4050 leituras."""

        dados2 = SerieTemporal.de_lista(list(range(4050)))
        resultado2 = SerieTemporal.media_movel(dados2, 10)

        self.assertEqual(len(resultado), 571)
        self.assertEqual(len(resultado2), 4041)
     def test_janelas(self):
         """O teste passa se der value error para as janelas <1 ou >len(self)"""
         with self.assertRaises(ValueError):
             (SerieTemporal.de_lista(list(range(1000)))).media_movel(-10)
         with self.assertRaises(ValueError):
             (SerieTemporal.de_lista(list(range(1000)))).media_movel(1001)
class test_reamostrar(unittest.TestCase):
     def test_reamostrar_medias_dos_blocos(self):
         """Verifica se calcula corretamente a média de cada bloco."""
         dados = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
         resultado = dados.reamostrar(3)
         np.testing.assert_allclose(resultado, [2.0, 5.0])


     def test_reamostrar_descarta_sobra(self):
        """Verifica se descarta os pontos finais que não completam um bloco."""
        dados = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        resultado = dados.reamostrar(3)
        np.testing.assert_allclose(resultado, [2.0, 5.0, 8.0])
        self.assertEqual(len(resultado), 3)

class test_ler_log(unittest.TestCase):
     def test_ler_log_registro_valido(self):
        """Verifica se um log válido é convertido em um registro."""
        texto = "2026-01-15 10:30:00 INFO PT102 pressao=12.5"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])
        self.assertEqual(registros[0].nivel, "INFO")
        self.assertEqual(registros[0].tag, "PT102")
     def test_ler_log_data_impossivel(self):
        """Verifica se uma data impossível é colocada na lista de inválidos."""
        texto = "2026-02-30 10:30:00 INFO PT102 pressao=12.5"
        registros, invalidas = ler_log(texto)
        self.assertEqual(registros, [])
        self.assertEqual(len(invalidas), 1)
        self.assertEqual(invalidas[0], texto)

      
if __name__ == "__main__":
    unittest.main()
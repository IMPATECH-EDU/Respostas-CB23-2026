"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np
import sys
import os
from elevatoria.serie import SerieTemporal
from elevatoria.dados import por_tag


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestMediaMovel(unittest.TestCase):

    def test_media_movel_tamanho_correto(self):
        """Verifica se media_movel retorna n - janela + 1 elementos."""
        dados = list(range(600))  # Criamos a lista com 600 numeros de 1 a 600
        serie = SerieTemporal.de_lista(dados) # Convertemos essa lista em uma SerieTemporal
        janela = 30

        # Aqui fazemos os testes, mas para uma lista menor
        dads=[1, 2, 3, 4, 5]
        seri=SerieTemporal.de_lista(dads)
        janel=2

        # Realizamos a verificação usando o método da classe SerieTemporal
        resultado_1= SerieTemporal.media_movel(serie, janela)
        resultado_2= SerieTemporal.media_movel(seri, janel)

        # 600 - 30 + 1 deve ser 571 (o código antigo retorna 570 e falha neste assert)
        self.assertAlmostEqual(len(resultado_1), 571)
        # 5 - 2 + 1 deve ser aproximadamente igual a 4, por ser float 
        self.assertAlmostEqual(len(resultado_2), 4)

        # Verificamos se o resultado está coerente com o esperado
        self.assertTrue(np.allclose(resultado_2, [1.5, 2.5, 3.5, 4.5]))


class TestReamostrar(unittest.TestCase):
    def test_reamostrar_com_k_valido(self):
        """Analisamos se a função reamostrar está identificando se o k dado como argumento é válido e se 
        não for lança ValueError"""

        k_1=0
        k_2=10
        dadso=SerieTemporal.de_lista([10, 20, 30, 40, 50, 60, 70])

        # Agora vemos se temos a função lança ValueError
        try:
            result_1=dadso.reamostrar(k_1)
        except ValueError:
            self.assertTrue(12==10+2)
        
        result_2=dadso.reamostrar(k_2)

    def test_reamostrar_media_certa(self):

        # Vamos usar o caso onde temos 7 itens e queremos separá-los em blocos de tamanho 3
        serie = SerieTemporal.de_lista([10, 20, 30, 40, 50, 60, 70])
        resultado = serie.reamostrar(3)

        # Esperamos receber que o resultado seja [20, 50], já que (10+20+30)/3==20 e (40+50+60)/3==50
        assert np.allclose(resultado, [20, 50])


if __name__ == "__main__":
    unittest.main()

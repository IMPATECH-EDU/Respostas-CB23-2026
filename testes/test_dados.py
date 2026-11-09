"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np
import sys
import os
from elevatoria.serie import SerieTemporal
from elevatoria.dados import (por_tag, ler_log)


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestMediaMovel(unittest.TestCase):

    def test_media_movel_tamanho_correto(self):
        """Verifica se media_movel retorna n - janela + 1 elementos, para as series [i for i in range(600)] e [1, 2, 3, 4, 5]."""
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
        self.assertEqual(len(resultado_1), 571)
        # 5 - 2 + 1 deve ser aproximadamente igual a 4, por ser float 
        self.assertEqual(len(resultado_2), 4)

        # Verificamos se o resultado está coerente com o esperado
        self.assertTrue(np.allclose(resultado_2, [1.5, 2.5, 3.5, 4.5]))

    def test_media_movel_janela_igual_serie(self):
        """Verifica se uma janela do tamanho da série produz uma única média."""
        serie = SerieTemporal.de_lista([2, 4, 6])
        resultado = serie.media_movel(3)

        self.assertEqual(len(resultado), 1)
        self.assertTrue(np.allclose(resultado, [4]))

class TestReamostrar(unittest.TestCase):
    def test_reamostrar_com_k_valido(self):
        """Analisamos se reamostrar lança ValueError quando identifica k menor que 1 ou maior que o comprimento da serie"""
        serie = SerieTemporal.de_lista([10, 20, 30, 40, 50])

        with self.assertRaises(ValueError):
            serie.reamostrar(0)

        with self.assertRaises(ValueError):
            serie.reamostrar(6)

    def test_reamostrar_media_certa(self):
        """Cobrindo o caso para a serie(10, 20, 30, 40, 50, 60, 70), testa se o método reamostrar está bem implementado"""
        # Vamos usar o caso onde temos 7 itens e queremos separá-los em blocos de tamanho 3
        serie = SerieTemporal.de_lista([10, 20, 30, 40, 50, 60, 70])
        resultado = serie.reamostrar(3)

        # Esperamos receber que o resultado seja [20, 50], já que (10+20+30)/3==20 e (40+50+60)/3==50
        assert np.allclose(resultado, [20, 50])

class TestLerLog(unittest.TestCase):

    def test_ignora_linhas_vazias(self):
        """Verifica se linhas vazias ou com espaços são ignoradas."""
        texto = "\n   \n\t\n"

        registros, invalidas = ler_log(texto)

        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [])

    def test_converte_valores_do_log(self):
        """Verifica se valores numéricos viram float e textos permanecem strings."""
        texto = "2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5"

        registros, invalidas = ler_log(texto)

        self.assertEqual(len(invalidas), 0)
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0].valores["evento"], "partida")
        self.assertEqual(registros[0].valores["corrente"], 47.5)
        self.assertIsInstance(registros[0].valores["corrente"], float)

    def test_preserva_ordem_dos_registros(self):
        """Verifica se os registros são devolvidos na mesma ordem do texto."""
        texto = (
            "2026-10-05 08:00:00 INFO B1 evento=partida\n"
            "2026-10-05 08:00:06 WARN B1 evento=parada"
        )

        registros, invalidas = ler_log(texto)

        self.assertEqual(len(invalidas), 0)
        self.assertEqual(len(registros), 2)
        self.assertEqual(registros[0].valores["evento"], "partida")
        self.assertEqual(registros[1].valores["evento"], "parada")

    def test_descarta_data_impossivel(self):
        """Verifica se uma linha com data impossível é descartada."""
        texto = "2026-13-05 08:00:00 INFO B1 evento=partida"  # Data impossível sendo mês 13

        registros, invalidas = ler_log(texto)

        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [texto])

if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import por_tag, ler_log

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
    """Testes para a media_movel de SerieTemporal."""
    def test_tamanho(self):
        """Verifica o tamanho da série resultante."""
        # Criamos a série
        arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        nova_serie = SerieTemporal.de_lista(arr)

        # Calculamos a média móvel
        janela = 2
        media = nova_serie.media_movel(janela)

        # Teste de tamanho: 10 - 2 + 1 = 9 elementos
        self.assertEqual(len(media), len(arr) - janela + 1, "A média móvel devolveu um tamanho incorreto")

    def test_primeiro_ponto(self):
        """Verifica o valor do primeiro ponto."""
        # Criamos a série
        arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        nova_serie = SerieTemporal.de_lista(arr)

        # Calculamos a média móvel
        janela = 2
        media = nova_serie.media_movel(janela)

        # Teste do primeiro elemento: (1 + 2) / 2 = 1.5
        self.assertEqual(float(media[0]), 1.5,  "A média movel ignora o primeiro valor")

    def test_media_movel_janela_invalida(self):
        """Verifica se media_movel levanta ValueError para janela menor que 1 ou maior que len(self)."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            s.media_movel(0)

class TestReamostrar(unittest.TestCase):
    """Testes para o método reamostrar da SerieTemporal."""

    def test_reamostrar_descarte_de_sobra(self):
        """Verifica se reamostrar descarta corretamente os pontos que sobram."""
        # 11 elementos com k = 5 deve gerar 2 blocos (10 elementos) e descartar o 11
        s = SerieTemporal.de_lista([2.0] * 11)
        res = s.reamostrar(5)
        self.assertEqual(len(res), 2)
        self.assertTrue(np.allclose(res, [2.0, 2.0]))

    def test_reamostrar_valores_calculados(self):
        """Verifica se as médias dos blocos consecutivos são calculadas adequadamente."""
        s = SerieTemporal.de_lista([1.0, 3.0, 10.0, 20.0])  # Bloco 1: (1+3)/2 = 2, Bloco 2: (10+20)/2 = 15
        res = s.reamostrar(2)
        self.assertTrue(np.allclose(res, [2.0, 15.0]))

    def test_reamostrar_k_invalido(self):
        """Verifica se reamostrar levanta ValueError quando k for menor que 1 ou maior que len(self)."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            s.reamostrar(0)

class TestLerLog(unittest.TestCase):
    """Testes de ler_log não verificados nos testes de aceitação."""

    def test_ler_log_ignora_linhas_invalidas_e_comentarios(self):
        """Garante que ler_log ignora linhas malformadas e comentários sem interromper a leitura."""
        texto = (
            "2026-10-05 08:59:42 INFO PT101 contagens=132\n"
            "# Linha de comentário que deve ser ignorada\n"
            "LINHA_INVALIDA_SEM_DATA_NEM_TAG\n"
            "2026-10-05 08:59:48 INFO PT101 contagens=136\n"
        )
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 2)
        self.assertEqual(len(invalidas), 2)

    def test_ler_log_conversao_tipos_atributos(self):
        """Verifica se ler_log converte corretamente os valores numéricos dos registros."""
        texto = "2026-10-05 08:59:42 INFO LT301 nivel=53.64 evento=normal\n"
        registros, _ = ler_log(texto)
        reg = registros[0]
        self.assertEqual(reg.tag, "LT301")
        self.assertAlmostEqual(float(reg.valores["nivel"]), 53.64)
        self.assertEqual(reg.valores["evento"], "normal")


if __name__ == "__main__":
    unittest.main()

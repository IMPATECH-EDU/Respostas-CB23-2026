"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np
from elevatoria.dados import (por_tag, ler_log, valida_tag, contagem_por_tag,
                              criar_conversores, medir_memoria, serie)
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestMarco1Proprio(unittest.TestCase):
    def test_regressao_media_movel_janela_1(self):
        """A janela unitária deve devolver todos os pontos, inclusive o primeiro."""
        s = SerieTemporal.de_lista([2, 4, 8])
        resultado = s.media_movel(1)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(np.allclose(resultado, [2, 4, 8]))

    def test_regressao_media_movel_janela_completa(self):
        """Uma janela do tamanho da série deve produzir exatamente uma média."""
        s = SerieTemporal.de_lista([2, 4, 6, 8])
        resultado = s.media_movel(4)
        self.assertEqual(len(resultado), 1)
        self.assertTrue(np.allclose(resultado, [5]))

    def test_reamostrar_descarta_sobra(self):
        """Pontos finais que não completam um bloco devem ser descartados."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 100])
        self.assertTrue(np.allclose(s.reamostrar(3), [2, 5]))

    def test_reamostrar_bloco_unitario(self):
        """Com k igual a um, a reamostragem preserva todos os valores."""
        s = SerieTemporal.de_lista([3, 7, 9])
        self.assertTrue(np.allclose(s.reamostrar(1), [3, 7, 9]))

    def test_ler_log_ignora_linhas_em_branco(self):
        """Linhas vazias e com espaços não entram na lista de inválidas."""
        registros, invalidas = ler_log("\n   \n2026-10-05 08:00:00 INFO B1 evento=partida\n")
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_ler_log_data_impossivel(self):
        """Uma data impossível deve ser descartada e preservada como inválida."""
        linha = "2026-13-05 08:00:00 INFO B1 evento=partida"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_ler_log_sem_par_chave_valor(self):
        """Uma linha estruturalmente válida sem chave=valor é inválida."""
        linha = "2026-10-05 08:00:00 INFO B1 partida"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_tag_aceita_limites(self):
        """Uma letra e um dígito formam a menor tag permitida."""
        self.assertTrue(valida_tag("A1"))

    def test_conversores_fatores_independentes(self):
        """Cada lambda mantém o fator associado à sua própria tag."""
        f = criar_conversores({"A1": 2.0, "B2": 0.5})
        self.assertAlmostEqual(f["A1"](3), 6)
        self.assertAlmostEqual(f["B2"](3), 1.5)

    def test_contagem_tags_vazia(self):
        """A contagem de uma coleção vazia deve ser um dicionário vazio."""
        self.assertEqual(contagem_por_tag([]), {})

    def test_memoria_rejeita_float(self):
        """A medição de memória deve rejeitar arrays com dtype não inteiro."""
        from elevatoria.dados import medir_memoria
        with self.assertRaises(ValueError):
            medir_memoria(np.array([1.0, 2.0]))

    def test_serie_sem_chave(self):
        """Uma série sem registros que contenham a chave deve ser vazia."""
        registros, _ = ler_log("2026-10-05 08:00:00 INFO B1 evento=partida")
        self.assertEqual(len(serie(registros, "B1", "contagens")), 0)


if __name__ == "__main__":
    unittest.main()

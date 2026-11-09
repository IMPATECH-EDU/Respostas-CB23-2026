"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np
from elevatoria import dados
from elevatoria.dados import por_tag
from elevatoria.serie import SerieTemporal 


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestLerLog(unittest.TestCase):
    """Regras do contrato de ler_log."""

    def test_mes_impossivel_e_invalido(self):
        """Linha com mês 13 vai para as inválidas."""
        texto = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = dados.ler_log(texto)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [texto])

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Linha cujo resto não tem nenhum chave=valor vai para as inválidas."""
        texto = "2026-10-05 08:00:00 INFO PT101 semvalor"
        registros, invalidas = dados.ler_log(texto)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [texto])

    def test_linhas_vazias_sao_ignoradas(self):
        """Linhas vazias ou só com espaços não contam como inválidas."""
        valida = "2026-10-05 08:00:00 INFO PT101 contagens=131"
        registros, invalidas = dados.ler_log(f"\n   \n{valida}\n\n")
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_texto_vazio(self):
        """Texto vazio devolve duas listas vazias."""
        self.assertEqual(dados.ler_log(""), ([], []))

    def test_conversao_dos_valores(self):
        """Números viram float e o restante continua str."""
        texto = "2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5"
        registros, _ = dados.ler_log(texto)
        self.assertEqual(registros[0].valores, {"evento": "partida", "corrente": 47.5})


class TestMemoriaETempo(unittest.TestCase):
    """Issue #3: memória e tempo."""

    def test_medir_memoria_rejeita_float(self):
        """medir_memoria levanta ValueError para ndarray de floats."""
        with self.assertRaises(ValueError):
            dados.medir_memoria(np.array([1.0, 2.0]))

    def test_medir_memoria_rejeita_2d(self):
        """medir_memoria levanta ValueError para ndarray 2D."""
        with self.assertRaises(ValueError):
            dados.medir_memoria(np.zeros((2, 2), dtype=int))

    def test_medir_memoria_bytes_do_ndarray(self):
        """uint16 ocupa 2 bytes por elemento e float64 ocupa 8."""
        r = dados.medir_memoria(np.arange(100))
        self.assertEqual(r["uint16"], 200)
        self.assertEqual(r["float64"], 800)
        self.assertEqual(r["array('H')"], 200)

    def test_converters_concordam(self):
        """As quatro conversões dão os mesmos valores."""
        c = np.array([0, 1000, 4095])
        lista = c.tolist()
        ref = dados.converter_laco(lista)
        self.assertTrue(np.allclose(dados.converter_compreensao(lista), ref))
        self.assertTrue(np.allclose(dados.converter_map(lista), ref))
        self.assertTrue(np.allclose(dados.converter_vetorizado(c), ref))

    def test_vetorizado_nao_estoura_uint16(self):
        """converter_vetorizado com uint16 não sofre overflow (4095 -> 600 kPa)."""
        c = np.array([4095], dtype=np.uint16)
        self.assertAlmostEqual(float(dados.converter_vetorizado(c)[0]), 600.0)

    def test_medir_tempos_chaves_e_positivos(self):
        """medir_tempos devolve as 4 chaves esperadas com tempos positivos."""
        t = dados.medir_tempos(np.arange(1000), k=2)
        self.assertEqual(set(t), {"laço", "compreensão", "map+lambda", "vetorizado"})
        self.assertTrue(all(v > 0 for v in t.values()))


class TestMediaMovel(unittest.TestCase):
    """Issue #4: regressão do bug de media_movel (um valor a menos)."""

    def test_media_movel_quantidade_de_valores(self):
        """media_movel de janela 3 em 6 pontos devolve n - janela + 1 = 4 valores."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        self.assertEqual(len(s.media_movel(3)), 4)

    def test_media_movel_valores(self):
        """media_movel começa na primeira janela e cobre todas as janelas."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        self.assertTrue(np.allclose(s.media_movel(3), [2, 3, 4, 5]))

    def test_media_movel_janela_igual_ao_tamanho(self):
        """media_movel com janela == len(serie) devolve um único valor, a média geral."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        r = s.media_movel(6)
        self.assertEqual(len(r), 1)
        self.assertAlmostEqual(float(r[0]), 3.5)

    def test_media_movel_janela_1_devolve_a_propria_serie(self):
        """media_movel com janela 1 devolve os mesmos n valores da série."""
        s = SerieTemporal.de_lista([4, 8, 15])
        self.assertTrue(np.allclose(s.media_movel(1), [4, 8, 15]))

    def test_media_movel_devolve_serie_temporal(self):
        """media_movel mantém o tipo de retorno SerieTemporal."""
        s = SerieTemporal.de_lista([1, 2, 3, 4])
        self.assertIsInstance(s.media_movel(2), SerieTemporal)


class TestReamostrar(unittest.TestCase):
    """Issue #5: médias por bloco."""

    def test_reamostrar_com_sobra_no_fim(self):
        """reamostrar descarta os pontos finais que não completam um bloco."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7])
        self.assertTrue(np.allclose(s.reamostrar(3), [2, 5]))

    def test_reamostrar_sem_sobra(self):
        """reamostrar com k que divide len(serie) usa todos os pontos."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6])
        self.assertTrue(np.allclose(s.reamostrar(2), [1.5, 3.5, 5.5]))

    def test_reamostrar_k_invalido(self):
        """reamostrar levanta ValueError para k < 1 e para k > len(serie)."""
        s = SerieTemporal.de_lista([1, 2, 3])
        with self.assertRaises(ValueError):
            s.reamostrar(0)
        with self.assertRaises(ValueError):
            s.reamostrar(4)

    def test_reamostrar_nao_modifica_self(self):
        """reamostrar não altera a série original."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        copia = s.copy()
        s.reamostrar(2)
        self.assertTrue(np.array_equal(s, copia))


if __name__ == "__main__":
    unittest.main()


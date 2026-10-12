"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np
from elevatoria.dados import ler_log, contagem_por_tag, criar_conversores, medir_tempos, medir_memoria, converter_vetorizado, converter_map, converter_laco, converter_compreensao

from elevatoria.dados import por_tag, SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])

    def test_ler_log_descarta_data_impossivel(self):
        """Verifica se linhas com mes 13 sao enviadas para a lista de invalidas."""
        texto = "2026-13-05 08:00:00 INFO PT101 contagens=100\n"
        corretas, incorretas = ler_log(texto)
        self.assertEqual(len(corretas), 0)
        self.assertEqual(len(incorretas), 1)

    def test_ler_log_descarta_linha_com_resto_sem_par_chave_valor(self):
        """Garante que linhas cujo grupo resto nao possui nenhum par chave=valor sao enviadas para invalidas."""
        # A linha casa na regex LINHA, mas 'texto_sem_igual' nao forma nenhum par chave=valor
        log_invalido = "2026-10-05 08:00:00 INFO PT101 texto_sem_igual\n"
        corretas, incorretas = ler_log(log_invalido)
        
        self.assertEqual(len(corretas), 0)
        self.assertEqual(len(incorretas), 1)
        self.assertEqual(incorretas, ["2026-10-05 08:00:00 INFO PT101 texto_sem_igual"])

    def test_ler_log_texto_vazio_e_linhas_em_branco(self):
        """Verifica se texto vazio ou composto apenas por espacos e quebras de linha devolve listas vazias."""
        log_espacos = "\n   \n\t\n  \n"
        corretas, incorretas = ler_log(log_espacos)
        
        self.assertEqual(corretas, [])
        self.assertEqual(incorretas, [])


    def test_contagem_por_tag_lista_vazia_retorna_dicionario_vazio(self):
        """Verifica se contagem_por_tag devolve um dicionario vazio ao receber uma lista vazia de registros."""
        resultado = contagem_por_tag([])
        self.assertEqual(resultado, {})

    
    def test_criar_conversores_cada_tag_usa_seu_fator_independente(self):
        """Garante que cada conversor aplica o fator correto da sua propria tag sem sofrer de late binding."""
        escalas = {"PT101": 0.1465, "PT102": 0.1465, "FT201": 0.1}
        conversores = criar_conversores(escalas)
        
        # Testa se PT101 e FT201 usam fatores diferentes
        self.assertAlmostEqual(conversores["PT101"](100), 14.65)
        self.assertAlmostEqual(conversores["FT201"](100), 10.0)

    def test_criar_conversores_dicionario_vazio_retorna_vazio(self):
        """Verifica se criar_conversores com dicionario de escalas vazio retorna um dicionario vazio."""
        self.assertEqual(criar_conversores({}), {})

    def test_memoria_chaves(self):
        """Verifica se medir_memoria devolve exatamente as chaves exigidas."""
        resultado = medir_memoria(np.array([0, 100, 4095]))
        esperadas = {
            "list", "array('H')", "uint16", "int32",
            "int64", "float32", "float64",
        }
        self.assertEqual(set(resultado), esperadas)

   
    def test_memoria_rejeita_lista(self):
        """Verifica se uma lista Python é rejeitada por medir_memoria."""
        with self.assertRaises(ValueError):
            medir_memoria([1, 2, 3])

    def test_memoria_rejeita_multidimensional(self):
        """Verifica se medir_memoria rejeita arrays com mais de uma dimensão."""
        with self.assertRaises(ValueError):
            medir_memoria(np.array([[1, 2], [3, 4]]))

    def test_memoria_rejeita_float(self):
        """Verifica se medir_memoria rejeita arrays com dtype de ponto flutuante."""
        with self.assertRaises(ValueError):
            medir_memoria(np.array([1.0, 2.0]))

    def test_conversoes_equivalentes(self):
        """Verifica se as quatro conversões produzem resultados equivalentes."""
        contagens = [0, 100, 2047, 4095]
        vetor = np.array(contagens)

        resultados = [
            converter_laco(contagens),
            converter_compreensao(contagens),
            converter_map(contagens),
            converter_vetorizado(vetor),
        ]

        for resultado in resultados[1:]:
            self.assertTrue(np.allclose(resultados[0], resultado))

    def test_medir_tempos_chaves(self):
        """Verifica se medir_tempos devolve exatamente as quatro chaves exigidas."""
        resultado = medir_tempos(np.array([0, 100, 4095]), k=2)
        esperadas = {"laço", "compreensão", "map+lambda", "vetorizado"}
        self.assertEqual(set(resultado), esperadas)



    """Testes de regressão da média móvel."""

    def test_media_movel_quantidade_correta(self):
            """Verifica que uma janela de 2 pontos produz n - 1 médias."""
            serie = SerieTemporal.de_lista([1, 2, 3, 4])
            resultado = serie.media_movel(2)

            self.assertEqual(len(resultado), 3)
            self.assertTrue(np.allclose(resultado, [1.5, 2.5, 3.5]))

    def test_media_movel_janela_um(self):
            """Verifica que uma janela de tamanho 1 preserva os valores."""
            serie = SerieTemporal.de_lista([2, 4, 6])
            resultado = serie.media_movel(1)

            self.assertTrue(np.allclose(resultado, [2, 4, 6]))

    def test_media_movel_janela_igual_tamanho(self):
            """Verifica que uma janela igual à série produz uma única média."""
            serie = SerieTemporal.de_lista([2, 4, 6, 8])
            resultado = serie.media_movel(4)

            self.assertEqual(len(resultado), 1)
            self.assertTrue(np.allclose(resultado, [5.0]))

    def test_media_movel_retorna_serie_temporal(self):
            """Verifica que o resultado mantém o tipo SerieTemporal."""
            serie = SerieTemporal.de_lista([1, 2, 3])
            resultado = serie.media_movel(2)

            self.assertIsInstance(resultado, SerieTemporal)

    def test_reamostrar_descarta_sobras(self):
        """Verifica que os pontos finais que não completam um bloco são descartados."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 7, 8])

        resultado = s.reamostrar(3)

        self.assertTrue(np.allclose(resultado, [2.0, 5.0]))


    def test_reamostrar_retorna_serie_temporal(self):
        """Verifica que o resultado de reamostrar mantém o tipo SerieTemporal."""
        s = SerieTemporal.de_lista([1, 2, 3, 4])

        resultado = s.reamostrar(2)

        self.assertIsInstance(resultado, SerieTemporal)


    def test_reamostrar_nao_modifica_original(self):
        """Verifica que reamostrar não altera os valores da série original."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5])
        original = s.copy()

        s.reamostrar(2)

        self.assertTrue(np.array_equal(s, original))


    def test_reamostrar_rejeita_k_invalido(self):
        """Verifica que reamostrar rejeita k menor que 1 ou maior que o tamanho da série."""
        s = SerieTemporal.de_lista([1, 2, 3, 4])

        for k in [0, -1, 5]:
            with self.subTest(k=k), self.assertRaises(ValueError):
                s.reamostrar(k)


    def test_reamostrar_casos_limite(self):
        """Verifica que blocos de tamanho 1 e do tamanho da série produzem médias corretas."""
        s = SerieTemporal.de_lista([2, 4, 6])

        self.assertTrue(np.allclose(s.reamostrar(1), [2, 4, 6]))
        self.assertTrue(np.allclose(s.reamostrar(3), [4]))

    



# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

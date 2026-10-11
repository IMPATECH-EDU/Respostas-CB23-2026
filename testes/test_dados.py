"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np
from elevatoria.dados import ler_log, contagem_por_tag, criar_conversores, medir_tempos, medir_memoria, converter_vetorizado, converter_map, converter_laco, converter_compreensao

from elevatoria.dados import por_tag


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

    



# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

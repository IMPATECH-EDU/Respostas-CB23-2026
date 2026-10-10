"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
from elevatoria.dados import ler_log, contagem_por_tag, criar_conversores

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



# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

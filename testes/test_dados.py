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

class TestMediaMovelRegressao(unittest.TestCase):
    """na issue 4, media_movel estava devolvendo um valor a menos."""

    def test_tamanho_600_janela_30(self):
        """como relatado, deveria dar 571 valores"""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)),571)

    def test_janela_igual_ao_tamanho(self):
        """a janela do tamanho da série precisar dar o valor da média do tubo"""
        s = SerieTemporal.de_lista([2.0,4.0,6.0,8.0])
        r = s.media_movel(4)
        self.assertEqual(len(r),1)
        self.assertAlmostEqual(float(r[0]),5.0)

    def test_janela_um_devolve_a_propria_serie(self):
        """a janela 1 devolve a mesma série, porque não 'suaviza' nada"""
        s = SerieTemporal.de_lista([3.0,1.0,4.0,1.0,5.0])
        self.assertTrue(np.allclose(s.media_movel(1),s))
        
class TestReamostrar(unittest.TestCase):
    "na issue 5, para fazer as medias por bloco"

    def test_sobra_no_fim_eh_descartada(self):
        """com 7 pontos e k = 3, o último ponto deve ser descartado"""
        r = SerieTemporal.de_lista([1,2,3,4,5,6,7]).reamostrar(3)
        self.assertEqual(len(r),2)
        self.assertTrue(np.allclose(r,[2.0,5.0]))

class TestLerLogContrato(unittest.TestCase):
    """na issue 1, regras de ler_log que os testes de aceitacao nao verificam"""

    def test_linhas_vazias_nao_sao_invalidas(self):
        """só ignoradas, não invalidadas"""
        registros, invalidas = dados.ler_log(f"\n \n{"2026-10-05 08:00:00 INFO PT102 contagens=1623"}\n\n")
        self.assertEqual(len(registros),1)
        self.assertEqual(invalidas,[])

    def test_data_impossivel_e_invalida(self):
        """mês 13 (★!) vai ser lido, mas deve ser inválido"""
        linha = "2026-13-05 08:00:00 INFO PT102 contagens=1623"
        registros, invalidas = dados.ler_log(linha)

        self.assertEqual(registros,[])
        self.assertEqual(invalidas, [linha])

    def test_resto_sem_par_chave_valor_eh_invalido(self):
        """se uma linha não tem nenhum chave=valor no resto, tem que ser inválida"""
        linha = "2026-10-05 08:00:00 INFO PT102 sem_par_heheheeee"
        registros, invalidas = dados.ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_ordem_original_dos_registros(self):
        """as linhas devem sair na ordem em que aparecem no texto"""
        texto = ("2026-10-05 08:00:06 INFO PT102 contagens=2\n""2026-10-05 08:00:00 INFO PT102 contagens=1\n")
        registros, _ = dados.ler_log(texto)
        self.assertEqual([r.valores["contagens"] for r in registros], [2.0, 1.0])

class TestTagESerie(unittest.TestCase):
    """na issue 1, para testar valida_tag e serie"""

    def test_valida_tag_nao_aceita_quebra_de_linha(self):
        """o fullmatch não deixa passar uma tag seguida de uma quebra de linha"""
        self.assertFalse(dados.valida_tag("PT101\n"))

    def test_serie_de_tag_inexistente_eh_vazia(self):
        """tag que não existe no log dá uma série vazia"""
        registros, _ = dados.ler_log("2026-10-05 08:00:00 INFO PT102 contagens=1623")
        self.assertEqual(len(dados.serie(registros, "XX9", "contagens")),0)

class TestConversoresBorda(unittest.TestCase):
    """na issue 2, o 'late binding'."""

    def test_cada_convertedor_usa_o_fator_da_sua_tag(self):
        """com três tags, nenhum conversor usa o fator da última tag do dicionáio"""
        conv = dados.criar_conversores({"A1": 2.0, "B2": 3.0, "C3": 5.0})
        self.assertAlmostEqual(conv["A1"](10.0),20.0)
        self.assertAlmostEqual(conv["B2"](10.0),30.0)
        self.assertAlmostEqual(conv["C3"](10.0),50.0)

class TestMemoriaEConversaoBorda(unittest.TestCase):
    """na issue 3, para testar medir_memoria e converter_vetorizado"""

    def test_memoria_nao_aceita_array_de_float(self):
        """medir_memoria só aceita 'ndarray' de inteiros, ou seja, float deve levantar ValueError"""
        with self.assertRaises(ValueError): dados.medir_memoria(np.array([1.0,2.0,3.0]))

    def test_vetorizado_nao_estoura_uint16(self):
        """a conversão vetorizada de um uint16 não pode dar overflow"""
        r = dados.converter_vetorizado(np.array([4095],dtype=np.uint16))
        self.assertAlmostEqual(float(r[0]),600.0)
        
# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()


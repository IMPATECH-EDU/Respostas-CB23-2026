import unittest
import numpy as np

from elevatoria.dados import por_tag, valida_tag, ler_log, criar_conversores
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestRegressaoIssue4(unittest.TestCase):
    """Testes de regressão para a issue #4 (média móvel)."""

    def test_regressao_media_movel_tamanho(self):
        """Verifica se o tamanho retornado pela média móvel é N - janela + 1."""
        s = SerieTemporal.de_lista(list(range(10)))
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 8)  # 10 - 3 + 1 = 8

    def test_regressao_media_movel_valores(self):
        """Verifica os valores exatos calculados pela média móvel."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        mm = s.media_movel(3)
        np.testing.assert_allclose(mm, [2.0, 3.0, 4.0])


class TestValidaTag(unittest.TestCase):
    """Testes para a função valida_tag."""

    def test_valida_tag_sucesso(self):
        """Garante que tags no formato correto (ex: PT101, B1) são aceites."""
        self.assertTrue(valida_tag("PT101"))
        self.assertTrue(valida_tag("B1"))

    def test_valida_tag_rejeita_invalidas(self):
        """Garante que tags minúsculas ou com excesso de dígitos são rejeitadas."""
        self.assertFalse(valida_tag("pt101"))
        self.assertFalse(valida_tag("PT1010"))


class TestLerLog(unittest.TestCase):
    """Testes para o parsing e validação na função ler_log."""

    def test_ler_log_data_invalida(self):
        """Verifica se linhas com datas impossíveis (ex: mês 13) vão para a lista de inválidas."""
        texto = "2026-13-05 08:00:00 INFO PT101 contagens=100\n"
        regs, invs = ler_log(texto)
        self.assertEqual(len(regs), 0)
        self.assertEqual(len(invs), 1)

    def test_ler_log_sem_pares_chave_valor(self):
        """Verifica se linhas sem pares chave=valor são descartadas como inválidas."""
        texto = "2026-10-05 08:00:00 INFO PT101\n"
        regs, invs = ler_log(texto)
        self.assertEqual(len(regs), 0)
        self.assertEqual(len(invs), 1)


class TestCriarConversores(unittest.TestCase):
    """Testes para a issue #2 (late binding em lambdas)."""

    def test_conversores_fator_independente(self):
        """Garante que cada lambda mantém o seu próprio fator de conversão (early binding)."""
        escalas = {"PT101": 2.0, "FT201": 0.5}
        conversores = criar_conversores(escalas)
        
        # Testa se a conversão do PT101 usa fator 2.0 e não o último fator 0.5
        self.assertAlmostEqual(conversores["PT101"](10.0), 20.0)
        self.assertAlmostEqual(conversores["FT201"](10.0), 5.0)


class TestReamostrar(unittest.TestCase):
    """Testes para a issue #5 (reamostragem em blocos)."""

    def test_reamostrar_descarte_sobra(self):
        """Verifica se a reamostragem ignora os elementos sobressalentes do fim."""
        s = SerieTemporal.de_lista([1.0, 3.0, 2.0, 4.0, 10.0])
        r = s.reamostrar(2)
        self.assertEqual(len(r), 2)
        np.testing.assert_allclose(r, [2.0, 3.0])

    def test_reamostrar_bloco_invalido_lança_exceção(self):
        """Verifica se tamanhos de bloco inválidos (< 1 ou > len(s)) lançam ValueError."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            s.reamostrar(0)
        with self.assertRaises(ValueError):
            s.reamostrar(5)


if __name__ == "__main__":
    unittest.main()
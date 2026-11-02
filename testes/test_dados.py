"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md)."""
import unittest
import numpy as np

from elevatoria.dados import (
    por_tag,
    ler_log,
    valida_tag,
    medir_memoria,
)
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestIssue4Regressao(unittest.TestCase):
    """Testes de regressão para a Issue #4 (bug da média móvel)."""

    def test_media_movel_tamanho_correto(self):
        """Média móvel de janela 30 em 600 elementos deve retornar exatamente 571 elementos."""
        s = SerieTemporal.de_lista(list(range(600)))
        mm = s.media_movel(30)
        self.assertEqual(len(mm), 571)

    def test_media_movel_valores_exatos(self):
        """Média móvel de janela 3 para [1, 2, 3, 4, 5] deve ser [2.0, 3.0, 4.0]."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        mm = s.media_movel(3)
        np.testing.assert_allclose(mm, [2.0, 3.0, 4.0])


class TestReamostrar(unittest.TestCase):
    """Testes do método reamostrar (Issue #5)."""

    def test_reamostrar_descarte_sobra(self):
        """Reamostrar série de tamanho 7 com k=3 devolve 2 blocos descartando o último ponto."""
        s = SerieTemporal.de_lista([1, 2, 3, 4, 5, 6, 100])
        r = s.reamostrar(3)
        self.assertEqual(len(r), 2)
        np.testing.assert_allclose(r, [2.0, 5.0])

    def test_reamostrar_valores_exatos(self):
        """Reamostrar blocos de 2 elementos calcula médias de cada par consecutivo."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        r = s.reamostrar(2)
        np.testing.assert_allclose(r, [15.0, 35.0])


class TestLerLogContrato(unittest.TestCase):
    """Testes de contrato da função ler_log e valida_tag (Issue #1)."""

    def test_ler_log_data_invalida(self):
        """Linha com data/hora inexistente (mês 13) deve ser descartada em invalidas."""
        texto = "2026-13-05 08:00:00 INFO PT101 contagens=100"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

    def test_ler_log_sem_chave_valor(self):
        """Linha sem pares chave=valor no resto deve ser considerada inválida."""
        texto = "2026-10-05 08:00:00 INFO PT101 apenas_texto"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 0)
        self.assertEqual(len(invalidas), 1)

    def test_ler_log_linha_vazia_ignorada(self):
        """Linhas vazias não devem contar como inválidas nem gerar registros."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=100\n\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(len(invalidas), 0)

    def test_valida_tag_espacos_sobrando(self):
        """Tag com espaços no final deve ser rejeitada por valida_tag."""
        self.assertFalse(valida_tag("PT101 "))

    def test_medir_memoria_tipo_invalido(self):
        """medir_memoria deve levantar ValueError se receber um array de float."""
        arr_float = np.array([1.0, 2.0, 3.0])
        with self.assertRaises(ValueError):
            medir_memoria(arr_float)


if __name__ == "__main__":
    unittest.main()
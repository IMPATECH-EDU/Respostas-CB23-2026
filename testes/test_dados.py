"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import criar_conversores, ler_log, medir_memoria, por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestLerLogContrato(unittest.TestCase):
    """Cobertura das regras de contrato de ler_log fora dos testes de aceitacao."""

    def test_ignora_linhas_vazias_e_espacos(self):
        """Linhas vazias ou so com espacos sao ignoradas sem contar como invalidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=130\n\t \n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_rejeita_data_ou_hora_impossivel(self):
        """Data ou hora impossivel (como mes 13) vai para invalidas sem modificacao."""
        linha_ruim = "2026-13-05 08:00:00 INFO PT101 contagens=130"
        registros, invalidas = ler_log(linha_ruim + "\n")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha_ruim])

    def test_rejeita_resto_sem_pares_chave_valor(self):
        """Linha sem nenhum par chave=valor no resto e descartada como invalida."""
        linha_sem_par = "2026-10-05 08:00:00 WARN B1 comunicacao_instavel"
        registros, invalidas = ler_log(linha_sem_par)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha_sem_par])


class TestConversoresContrato(unittest.TestCase):
    """Testes adicionais de criar_conversores para entrada vazia e isolamento de lambdas."""

    def test_conversores_dicionario_vazio_e_multiplos_fatores(self):
        """Dicionario vazio devolve vazio e fatores distintos nao sofrem late binding."""
        self.assertEqual(criar_conversores({}), {})
        conv = criar_conversores({"PT101": 0.15, "PT102": 0.30, "FT201": 0.10})
        self.assertAlmostEqual(conv["PT101"](100.0), 15.0)
        self.assertAlmostEqual(conv["PT102"](100.0), 30.0)
        self.assertAlmostEqual(conv["FT201"](100.0), 10.0)


class TestMemoriaETempoContrato(unittest.TestCase):
    """Validacoes extras de entrada para medir_memoria."""

    def test_medir_memoria_rejeita_float_e_lista(self):
        """Entradas que nao sejam ndarray 1D de inteiros levantam ValueError."""
        with self.assertRaises(ValueError):
            medir_memoria(np.array([1.0, 2.0, 3.0]))
        with self.assertRaises(ValueError):
            medir_memoria([1, 2, 3])  # type: ignore[arg-type]


class TestMediaMovelRegressao(unittest.TestCase):
    """Testes de regressao da issue #4 escritos antes da correcao de media_movel."""

    def test_media_movel_tamanho_e_primeira_janela(self):
        """Media movel de janela 2 inclui o primeiro bloco e devolve n - janela + 1 valores."""
        s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])
        res = s.media_movel(2)
        self.assertEqual(len(res), 4)
        self.assertTrue(np.allclose(res, [2.5, 6.5, 12.5, 20.5]))

    def test_media_movel_janela_igual_ao_comprimento(self):
        """Media movel com janela igual ao tamanho da serie devolve 1 valor com a media global."""
        s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])
        res = s.media_movel(len(s))
        self.assertEqual(len(res), 1)
        self.assertTrue(np.allclose(res, [11.0]))

    def test_media_movel_janela_unitaria(self):
        """Media movel com janela 1 preserva todos os elementos sem modificar a serie original."""
        s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])
        res = s.media_movel(1)
        self.assertEqual(len(res), 5)
        self.assertTrue(np.allclose(res, [1.0, 4.0, 9.0, 16.0, 25.0]))


class TestReamostrarExtra(unittest.TestCase):
    """Cobertura adicional para reamostrar, incluindo descarte da sobra final."""

    def test_reamostrar_descarta_sobra_no_fim(self):
        """Reamostrar descarta os pontos finais incompletos sem modificar a serie original."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 100.0])
        res = s.reamostrar(3)
        self.assertIsInstance(res, SerieTemporal)
        self.assertEqual(len(res), 2)
        self.assertTrue(np.allclose(res, [2.0, 5.0]))
        self.assertEqual(len(s), 7)

    def test_reamostrar_bloco_unico_e_tipo(self):
        """Reamostrar com k igual ao comprimento devolve SerieTemporal de tamanho 1."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0, 8.0, 10.0])
        res = s.reamostrar(len(s))
        self.assertIsInstance(res, SerieTemporal)
        self.assertEqual(len(res), 1)
        self.assertAlmostEqual(float(res[0]), 6.0)


if __name__ == "__main__":
    unittest.main()

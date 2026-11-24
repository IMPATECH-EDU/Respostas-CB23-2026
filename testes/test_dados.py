"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
import numpy as np


from elevatoria.dados import por_tag, medir_memoria, ler_log
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        print("rodando")
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TesteMediaMovel(unittest.TestCase):
    """"Issue #4"""

    def test_Base(self):
        dados = np.random.default_rng(1).integers(0, 4096, 600)
        self.assertEqual(len(SerieTemporal.media_movel(dados, 30)), 571)

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


class TestRegressaoMediaMovel(unittest.TestCase):
    """Issue #4: testes de regressão para `SerieTemporal.media_movel`."""

    def test_media_movel_tamanho_600_janela_30(self):
        """Série de 600 pontos com janela 30 devolve 571 médias, e não 570."""
        dados = SerieTemporal.de_lista(np.arange(600, dtype=float))
        self.assertEqual(len(dados.media_movel(30)), 571)

    def test_media_movel_valores_e_janela_1(self):
        """Calcula corretamente a primeira janela (incluindo índice 0) e janela 1."""
        s = SerieTemporal.de_lista([1.0, 4.0, 9.0, 16.0, 25.0])
        self.assertTrue(np.allclose(s.media_movel(2), [2.5, 6.5, 12.5, 20.5]))
        self.assertTrue(np.allclose(s.media_movel(1), [1.0, 4.0, 9.0, 16.0, 25.0]))


class TestReamostrar(unittest.TestCase):
    """Issue #5: testes de `SerieTemporal.reamostrar`."""

    def test_reamostrar_descarta_sobra_no_fim(self):
        """Pontos finais que não completam um bloco de k elementos são descartados."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 100.0])
        r = s.reamostrar(3)
        self.assertIsInstance(r, SerieTemporal)
        self.assertTrue(np.allclose(r, [2.0, 5.0]))

    def test_reamostrar_k_1_e_k_igual_tamanho(self):
        """Reamostrar com k=1 preserva a série e k=len(s) devolve a média global."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        self.assertTrue(np.allclose(s.reamostrar(1), [10.0, 20.0, 30.0, 40.0]))
        self.assertTrue(np.allclose(s.reamostrar(4), [25.0]))


class TestContratoDados(unittest.TestCase):
    """Issues #1 e #3: regras de contrato não cobertas pela aceitação."""

    def test_ler_log_ignora_linhas_vazias_e_espacos(self):
        """Linhas em branco ou apenas com espaços são ignoradas sem contar como inválidas."""
        texto = "\n   \n2026-10-05 08:00:00 INFO PT101 contagens=120\n\t  \n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_ler_log_rejeita_data_ou_hora_impossivel(self):
        """Datas inexistentes (ex.: 30 de fevereiro, mês 13) e horas >= 24 são inválidas."""
        texto = (
            "2026-13-05 08:00:00 INFO PT101 contagens=100\n"
            "2026-02-30 08:00:00 INFO PT101 contagens=100\n"
            "2026-10-05 25:00:00 INFO PT101 contagens=100\n"
        )
        registros, invalidas = ler_log(texto)
        self.assertEqual(registros, [])
        self.assertEqual(len(invalidas), 3)

    def test_ler_log_rejeita_resto_sem_chave_valor(self):
        """Linha sem nenhum par chave=valor no resto é descartada como inválida."""
        texto = "2026-10-05 08:00:00 INFO B1 mensagem_sem_igualdade\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [texto.strip()])

    def test_medir_memoria_rejeita_float_ou_lista(self):
        """medir_memoria levanta ValueError se receber ndarray de float ou lista Python."""
        with self.assertRaises(ValueError):
            medir_memoria(np.array([1.0, 2.0, 3.0]))
        with self.assertRaises(ValueError):
            medir_memoria([1, 2, 3])  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

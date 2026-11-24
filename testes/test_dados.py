"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import por_tag


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

class TestDadosExtras(unittest.TestCase):
    """Casos adicionais dos contratos do Marco 1."""

    def test_media_movel_tem_n_menos_janela_mais_um_resultados(self):
        """Regressão #4: a janela deve incluir também o último bloco possível."""
        from elevatoria.serie import SerieTemporal
        s = SerieTemporal.de_lista([1, 2, 3, 4])
        resultado = s.media_movel(2)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(np.allclose(resultado, [1.5, 2.5, 3.5]))

    def test_media_movel_com_janela_igual_ao_tamanho(self):
        """Regressão #4: uma janela do tamanho da série produz uma média."""
        from elevatoria.serie import SerieTemporal
        s = SerieTemporal.de_lista([2, 4, 6])
        resultado = s.media_movel(3)
        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(float(resultado[0]), 4.0)

    def test_reamostrar_descarta_sobra_final(self):
        """Médias por bloco descartam os pontos que não completam um bloco."""
        from elevatoria.serie import SerieTemporal
        resultado = SerieTemporal.de_lista([1, 2, 3, 4, 5]).reamostrar(2)
        self.assertTrue(np.allclose(resultado, [1.5, 3.5]))

    def test_reamostrar_janela_unitaria_copia_valores(self):
        """Blocos de tamanho um preservam cada observação."""
        from elevatoria.serie import SerieTemporal
        resultado = SerieTemporal.de_lista([3, 5, 7]).reamostrar(1)
        self.assertTrue(np.allclose(resultado, [3, 5, 7]))

    def test_ler_log_conta_data_impossivel_como_invalida(self):
        """Uma data que não existe é descartada e devolvida entre as linhas inválidas."""
        from elevatoria.dados import ler_log
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=100"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_ler_log_ignora_linha_em_branco(self):
        """Linhas vazias ou só com espaços não são registros nem inválidas."""
        from elevatoria.dados import ler_log
        registros, invalidas = ler_log("  \n\t\n")
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [])

    def test_ler_log_rejeita_resto_sem_par_chave_valor(self):
        """Uma linha estruturalmente válida sem chave=valor é inválida."""
        from elevatoria.dados import ler_log
        linha = "2026-10-05 08:00:00 INFO PT101 somente_texto"
        registros, invalidas = ler_log(linha)
        self.assertEqual(registros, [])
        self.assertEqual(invalidas, [linha])

    def test_medir_memoria_rejeita_array_float(self):
        """A medição de memória exige um ndarray unidimensional de inteiros."""
        from elevatoria.dados import medir_memoria
        with self.assertRaises(ValueError):
            medir_memoria(np.array([1.0, 2.0]))



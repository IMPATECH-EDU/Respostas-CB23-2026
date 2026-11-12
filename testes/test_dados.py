"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
from elevatoria.dados import ler_log, por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestLerLogRegras(unittest.TestCase):
    def test_rejeita_data_impossivel_e_preserva_espacos(self):
        """Devolve a linha com data impossível e seus espaços finais."""
        linha = "2026-13-05 08:00:00 INFO PT101 contagens=131  "

        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_rejeita_linha_sem_par_chave_valor(self):
        """Descarta a linha cujo conteúdo não tem nenhum par chave=valor."""
        linha = "2026-10-05 08:00:00 INFO PT101 leitura_incompleta"

        self.assertEqual(ler_log(linha), ([], [linha]))


class TestMediaMovelRegressao(unittest.TestCase):
    def test_inclui_a_primeira_janela(self):
        """Inclui a média dos dois primeiros pontos como primeiro resultado."""
        s = SerieTemporal.de_lista([2.0, 4.0, 8.0])

        resultado = s.media_movel(2)

        self.assertAlmostEqual(resultado[0], 3.0)
        self.assertEqual(len(resultado), 2)
        self.assertAlmostEqual(resultado[1], 6.0)

    def test_janela_do_tamanho_da_serie(self):
        """Uma janela do tamanho da série devolve uma única média."""
        s = SerieTemporal.de_lista([2.0, 4.0, 6.0])

        resultado = s.media_movel(3)

        self.assertEqual(len(resultado), 1)
        self.assertAlmostEqual(resultado[0], 4.0)

        



if __name__ == "__main__":
    unittest.main()

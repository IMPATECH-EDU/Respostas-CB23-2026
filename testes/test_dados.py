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


class TestMediaMovelRegressao(unittest.TestCase):
    """Issue #4: media_movel devolvia um valor a menos."""

    def test_tamanho(self) -> None:
        """O resultado tem n - janela + 1 valores."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        self.assertEqual(len(s.media_movel(2)), 3)

    def test_primeira_janela(self) -> None:
        """O primeiro valor é a média da primeira janela."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(float(s.media_movel(2)[0]), 1.5)


class TestReamostrarProprio(unittest.TestCase):
    """Issue #5: reamostrar."""

    def test_sobra_descartada(self) -> None:
        """Os pontos que não completam um bloco no fim são descartados."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertEqual(len(s.reamostrar(2)), 2)

    def test_k_igual_ao_tamanho(self) -> None:
        """Com k == len(self), sai um único valor: a média da série."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0])
        self.assertAlmostEqual(float(s.reamostrar(3)[0]), 2.0)


class TestLerLogContrato(unittest.TestCase):
    """Issue #1: regras de ler_log que os testes de aceitação não verificam."""

    def test_data_impossivel_e_invalida(self) -> None:
        """Uma linha com mês 13 vai para as inválidas."""
        linha = "2026-13-05 08:00:00 INFO PT102 contagens=1789"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_sem_pares_e_invalida(self) -> None:
        """Uma linha sem nenhum par chave=valor vai para as inválidas."""
        linha = "2026-10-05 08:00:00 INFO PT102 sem_pares"
        self.assertEqual(ler_log(linha), ([], [linha]))

    def test_linha_so_com_espacos_ignorada(self) -> None:
        """Linhas só com espaços não contam como inválidas."""
        self.assertEqual(ler_log("   \n"), ([], []))

    def test_hora_impossivel_e_invalida(self) -> None:
        """Uma linha com hora 25 vai para as inválidas."""
        linha = "2026-10-05 25:00:00 INFO PT102 contagens=1789"
        self.assertEqual(ler_log(linha), ([], [linha]))


if __name__ == "__main__":
    unittest.main()

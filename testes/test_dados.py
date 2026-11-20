"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

import numpy as np

from elevatoria.dados import ler_log, por_tag
from elevatoria.serie import SerieTemporal


class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""

    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoMediaMovel(unittest.TestCase):
    """Issue #4: media_movel devolvia n - janela valores em vez de n - janela + 1."""

    def test_quantidade_de_valores(self):
        """600 pontos com janela 30 dão 571 médias, como diz a docstring."""
        s = SerieTemporal.de_lista(np.arange(600.0))
        self.assertEqual(len(s.media_movel(30)), 571)

    def test_janela_igual_ao_tamanho(self):
        """Com janela == len(s), sai um único valor: a média da série inteira."""
        s = SerieTemporal.de_lista([2.0, 4.0, 9.0])
        mm = s.media_movel(3)
        self.assertEqual(len(mm), 1)
        self.assertAlmostEqual(float(mm[0]), 5.0)

    def test_primeira_media_usa_os_primeiros_pontos(self):
        """O valor 0 é a média de s[0:janela], incluindo o primeiro ponto."""
        s = SerieTemporal.de_lista([10.0, 20.0, 30.0, 40.0])
        mm = s.media_movel(2)
        self.assertEqual(len(mm), 3)
        self.assertTrue(np.allclose(mm, [15.0, 25.0, 35.0]))

    def test_janela_um_devolve_a_propria_serie(self):
        """Janela 1 é a identidade: mesmos valores, mesmo tamanho."""
        s = SerieTemporal.de_lista([3.0, -1.0, 7.5])
        mm = s.media_movel(1)
        self.assertEqual(len(mm), len(s))
        self.assertTrue(np.allclose(mm, s))


class TestContratoLerLog(unittest.TestCase):
    """Regras da docstring de ler_log que os testes de aceitação não exercitam."""

    BOA = "2026-10-05 08:00:00 INFO PT101 contagens=131"

    def test_linhas_em_branco_nao_sao_invalidas(self):
        """Linhas vazias ou só com espaços/tabs são puladas e não entram em `invalidas`."""
        texto = f"\n   \n{self.BOA}\n\t\n"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [])

    def test_data_ou_hora_impossivel_e_invalida(self):
        """Casar com LINHA não basta: mês 13 ou hora 25 tornam a linha inválida."""
        mes_13 = "2026-13-05 08:00:00 INFO PT101 contagens=131"
        hora_25 = "2026-10-05 25:00:00 INFO PT101 contagens=131"
        registros, invalidas = ler_log("\n".join([mes_13, self.BOA, hora_25]))
        self.assertEqual(len(registros), 1)
        self.assertEqual(invalidas, [mes_13, hora_25])

    def test_resto_sem_par_chave_valor_e_invalido(self):
        """Uma linha bem formada, mas sem nenhum `chave=valor` no resto, é descartada."""
        sem_par = "2026-10-05 08:00:00 WARN B1 bomba desligada"
        registros, invalidas = ler_log(sem_par + "\n" + self.BOA)
        self.assertEqual([r.tag for r in registros], ["PT101"])
        self.assertEqual(invalidas, [sem_par])

    def test_invalida_preservada_exatamente(self):
        """A linha descartada volta exatamente como estava, com espaços internos e finais."""
        suja = "  ### falha   de comunicacao ###   "
        _, invalidas = ler_log(suja)
        self.assertEqual(invalidas, [suja])


if __name__ == "__main__":
    unittest.main()

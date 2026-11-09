"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest
 
import numpy as np
 
from elevatoria.dados import criar_conversores, ler_log, por_tag, valida_tag
from elevatoria.serie import SerieTemporal

class TestPorTagExemplo(unittest.TestCase):
    """Exemplo do formato. `por_tag` é código existente da base."""
 
    def test_lista_vazia(self):
        """Sem registros, por_tag devolve uma lista vazia."""
        self.assertEqual(por_tag([], "PT101"), [])
 
 
# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #4 (escreva-os ANTES de corrigir o defeito e confirme que falham).
 
 
class TestMediaMovelRegressao(unittest.TestCase):
    """Regressão da issue #4: `media_movel` devia devolver n - janela + 1 valores."""
 
    def test_media_movel_tamanho_correto(self):
        """Com 600 pontos e janela 30, a média móvel tem 571 valores."""
        s = SerieTemporal.de_lista(np.arange(600, dtype=float))
        self.assertEqual(len(s.media_movel(30)), 571)
 
    def test_media_movel_valores_corretos(self):
        """A média móvel de janela 2 em [1..5] é [1.5, 2.5, 3.5, 4.5], sem deslocamento."""
        s = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0])
        np.testing.assert_allclose(s.media_movel(2), [1.5, 2.5, 3.5, 4.5])


 
class TestReamostrar(unittest.TestCase):
    """Issue #5: `reamostrar` devolve as médias de blocos consecutivos de `k` pontos."""

    def test_reamostrar_divisivel(self):
        """Com 6 pontos e k=2, há 3 blocos completos e o tipo é SerieTemporal."""
        r = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]).reamostrar(2)
        self.assertIsInstance(r, SerieTemporal)
        np.testing.assert_allclose(r, [1.5, 3.5, 5.5])

    def test_reamostrar_sobra_no_fim(self):
        """Com 7 pontos e k=3, o ponto que sobra no fim é descartado, como diz a docstring."""
        r = SerieTemporal.de_lista([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]).reamostrar(3)
        self.assertEqual(len(r), 2)
        np.testing.assert_allclose(r, [2.0, 5.0])


class TestLerLog(unittest.TestCase):
    """Issue #1: `ler_log` separa registros válidos das linhas fora do padrão."""

    def test_ler_log_linha_corrompida(self):
        """Uma linha fora do padrão é devolvida em `invalidas`; linhas em branco são ignoradas."""
        corrompida = "2026-03-14 08:00:10 ?? PT101 pressao=3.2"
        texto = "\n".join([
            "2026-03-14 08:00:00 INFO PT101 pressao=3.2",
            corrompida,
            "",
            "2026-03-14 08:00:20 WARN PT102 pressao=3.4",
        ])
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(registros), 2)
        self.assertEqual(invalidas, [corrompida])

    def test_ler_log_tipos_valores(self):
        """Valores numéricos viram float (inclusive os inteiros) e os demais ficam str."""
        texto = "2026-03-14 08:00:00 INFO PT101 pressao=3.5 contagens=1789 estado=ok"
        registros, invalidas = ler_log(texto)
        self.assertEqual(len(invalidas), 0)
        valores = registros[0].valores
        self.assertIsInstance(valores["pressao"], float)
        self.assertIsInstance(valores["contagens"], float)
        self.assertIsInstance(valores["estado"], str)
        self.assertAlmostEqual(valores["pressao"], 3.5)
        self.assertAlmostEqual(valores["contagens"], 1789.0)
        self.assertEqual(valores["estado"], "ok")


class TestValidaTag(unittest.TestCase):
    """Issue #1: `valida_tag` valida a string inteira."""

    def test_valida_tag_padrao(self):
        """Aceita tags como PT101 e B1; rejeita sufixo, prefixo, espaço e minúsculas."""
        for tag in ["PT101", "FT201", "B1"]:
            with self.subTest(tag=tag):
                self.assertTrue(valida_tag(tag))
        for tag in ["PT1010", "101PT", "PT101 ", "pt101", "PT", ""]:
            with self.subTest(tag=tag):
                self.assertFalse(valida_tag(tag))


class TestCriarConversores(unittest.TestCase):
    """Issue #2: `criar_conversores` devolve uma função independente por tag."""

    def test_criar_conversores_late_binding(self):
        """Cada conversor usa o fator da sua própria tag, e não o da última do dicionário."""
        conv = criar_conversores({"PT101": 2.0, "PT102": 10.0, "PT103": 0.5})
        self.assertAlmostEqual(conv["PT101"](3.0), 6.0)
        self.assertAlmostEqual(conv["PT102"](3.0), 30.0)
        self.assertAlmostEqual(conv["PT103"](3.0), 1.5)


if __name__ == "__main__":
    unittest.main()

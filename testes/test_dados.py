"""Seus testes do Marco 1 (veja a seção 6 do ENUNCIADO_MARCO1.md).

Regras: pelo menos 8 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
import unittest

from elevatoria.dados import ler_log, por_tag


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


if __name__ == "__main__":
    unittest.main()

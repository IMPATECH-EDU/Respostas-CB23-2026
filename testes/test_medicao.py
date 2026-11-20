"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import random
import unittest
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

# Curva que não altera as contagens, no domínio do A/D de 12 bits.
NEUTRA = CurvaCalibracao([0.0, 1000.0, 4095.0], [0.0, 1000.0, 4095.0], "linear")
INICIO = datetime(2026, 10, 5, 8, 0, 0)


def _leitura(i: int, tag: str, contagem: float) -> Registro:
    """Registro INFO da `tag` no instante i·6 s, com a contagem dada."""
    return Registro(INICIO + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(contagem)})


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o AcumuladorKahan somava igual ao ingênuo, sem compensar nada."""

    def test_pulsos_de_um_decimo(self):
        """10⁵ pulsos de 0,1 L dão exatamente 10000.0, onde a soma ingênua já erra."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        pulsos = [0.1] * 100_000
        kahan.adicionar_todos(pulsos)
        ingenuo.adicionar_todos(pulsos)
        self.assertNotEqual(ingenuo.total, 10_000.0)   # o problema existe
        self.assertEqual(kahan.total, 10_000.0)        # e o Kahan o resolve (igualdade exata)

    def test_parcelas_menores_que_meio_ulp(self):
        """Parcelas que somem sozinhas ao lado de 1.0 se acumulam na correção e aparecem no total."""
        kahan = AcumuladorKahan()
        kahan.adicionar(1.0)
        kahan.adicionar_todos([1e-16] * 1000)          # cada 1e-16 é menor que meio ulp de 1.0
        self.assertTrue(math.isclose(kahan.total, 1.0 + 1e-13, rel_tol=1e-15))

    def test_concorda_com_fsum(self):
        """Em valores aleatórios de magnitudes variadas, o Kahan fica a ~1 ulp da soma exata (math.fsum)."""
        gerador = random.Random(3472)
        valores = [gerador.uniform(0.0, 1.0) * 10.0 ** gerador.randint(-8, 3) for _ in range(20_000)]
        kahan = AcumuladorKahan()
        kahan.adicionar_todos(valores)
        exato = math.fsum(valores)
        self.assertLessEqual(abs(kahan.total - exato), 2 * math.ulp(exato))


class TestContratoMedir(unittest.TestCase):
    """Regras da docstring de medir que os testes de aceitação não verificam."""

    def setUp(self):
        self.base = [200, 202, 199, 201, 198, 200, 203, 197, 201, 199]

    def test_u_sistematica_negativa(self):
        """u_sistematica < 0 é entrada inválida e levanta ValueError."""
        regs = [_leitura(i, "PT101", c) for i, c in enumerate(self.base)]
        with self.assertRaises(ValueError):
            medir(regs, "PT101", NEUTRA, u_sistematica=-0.1)

    def test_mad_zero(self):
        """Com mais da metade das leituras iguais, a MAD é zero e medir recusa com ValueError."""
        regs = [_leitura(i, "PT101", c) for i, c in enumerate([500] * 7 + [501, 502])]
        with self.assertRaises(ValueError):
            medir(regs, "PT101", NEUTRA)

    def test_erro_da_curva_chega_a_quem_chamou(self):
        """Contagem fora do domínio da curva: o ValueError da CurvaCalibracao não é engolido."""
        curta = CurvaCalibracao([0.0, 100.0, 300.0], [0.0, 100.0, 300.0], "linear")
        regs = [_leitura(i, "PT101", c) for i, c in enumerate(self.base + [350])]
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(regs, "PT101", curta)

    def test_indices_na_serie_da_tag_em_ordem(self):
        """Os índices de espurias contam só leituras da tag (ignoram outras tags e alarmes) e vêm em ordem."""
        contagens = list(self.base)
        contagens[2] += 900
        contagens[7] -= 150
        regs = []
        for i, c in enumerate(contagens):
            regs.append(_leitura(i, "PT101", 50))                          # outra tag, intercalada
            regs.append(_leitura(i, "PT102", c))
            if i == 1:                                                     # alarme sem "contagens"
                regs.append(Registro(INICIO, "ALARME", "PT102", {"evento": "pressao_alta"}))
        m = medir(regs, "PT102", NEUTRA)
        self.assertEqual(m.espurias, [2, 7])
        self.assertEqual(m.n_validas, len(contagens) - 2)

    def test_limiar_controla_o_descarte(self):
        """Um limiar maior que o |z| da leitura afastada a mantém entre as válidas."""
        regs = [_leitura(i, "PT101", c) for i, c in enumerate(self.base + [230])]
        self.assertEqual(medir(regs, "PT101", NEUTRA).espurias, [10])       # limiar padrão 6
        self.assertEqual(medir(regs, "PT101", NEUTRA, limiar=50.0).espurias, [])


if __name__ == "__main__":
    unittest.main()

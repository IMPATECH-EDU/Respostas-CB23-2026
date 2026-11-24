"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest
from datetime import datetime, timedelta
from decimal import Decimal

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import altura_manometrica, medir

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def leituras(tag: str, contagens: list, inicio: int = 0) -> list:
    """Cria registros de `contagens` da `tag`, um a cada 6 s."""
    t0 = datetime(2026, 10, 5, 8, 0, 0) + timedelta(seconds=inicio)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Issue #7: o Kahan não compensava o arredondamento."""

    def test_um_milhao_de_parcelas_de_um_decimo(self):
        """1 milhão de parcelas de 0,1 somam 100000 com erro abaixo de 1e-9 (antes: 1,3e-6)."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)
        self.assertLess(abs(Decimal(acumulador.total) - Decimal(100_000)), Decimal("1e-9"))

    def test_kahan_bem_melhor_que_o_ingenuo(self):
        """O erro do Kahan é pelo menos 1000 vezes menor que o do ingênuo."""
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        for _ in range(200_000):
            ingenuo.adicionar(0.1)
            kahan.adicionar(0.1)
        exato = Decimal(20_000)
        erro_ingenuo = abs(Decimal(ingenuo.total) - exato)
        erro_kahan = abs(Decimal(kahan.total) - exato)
        self.assertGreater(erro_ingenuo, 0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)

    def test_parcelas_menores_que_meio_ulp_nao_se_perdem(self):
        """Dez parcelas de 1e-16 somadas a 1,0 não somem: o total chega perto de 1 + 1e-15."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar(1.0)
        for _ in range(10):
            acumulador.adicionar(1e-16)
        self.assertGreater(acumulador.total, 1.0)
        self.assertAlmostEqual(acumulador.total, 1.0 + 1e-15, delta=3e-16)

    def test_bate_com_fsum(self):
        """Com parcelas de ordens de grandeza diferentes, fica a 1e-12 de math.fsum."""
        parcelas = [10.0 ** (k % 7 - 3) * (1 + 0.01 * k) for k in range(5000)]
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos(parcelas)
        self.assertLess(abs(acumulador.total - math.fsum(parcelas)), 1e-12)


class TestContratoMedir(unittest.TestCase):
    """Issue #6: regras de medir que a aceitação não cobre."""

    BASE = [3000, 3001, 2999, 3000, 3002, 2998, 3000, 3001]

    def test_incerteza_sistematica_negativa(self):
        """Incerteza sistemática negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(leituras("PT101", self.BASE), "PT101", IDENTIDADE, u_sistematica=-0.1)

    def test_mad_nula_levanta_erro(self):
        """Leituras iguais dão MAD zero e levantam ValueError."""
        with self.assertRaises(ValueError):
            medir(leituras("PT101", [3000] * 8), "PT101", IDENTIDADE)

    def test_indices_contam_so_as_leituras_da_tag(self):
        """Os índices das espúrias contam só as leituras da tag, sem alarmes nem outras tags."""
        regs = leituras("PT102", self.BASE[:4] + [3500] + self.BASE[4:])
        alarme = Registro(datetime(2026, 10, 5, 8, 0, 1), "ALARME", "PT102", {"evento": "pressao_alta"})
        outra = leituras("PT101", [100] * 5)
        medicao = medir(outra + [alarme] + regs, "PT102", IDENTIDADE)
        self.assertEqual(medicao.espurias, [4])
        self.assertEqual(medicao.n_validas, len(self.BASE))

    def test_espuria_para_baixo_tambem_e_descartada(self):
        """O critério usa |z|, então leitura muito abaixo da mediana também é espúria."""
        medicao = medir(leituras("PT102", self.BASE + [100]), "PT102", IDENTIDADE)
        self.assertEqual(medicao.espurias, [8])
        self.assertAlmostEqual(medicao.medida.valor, sum(self.BASE) / len(self.BASE))

    def test_limiar_alto_nao_descarta_nada(self):
        """Com limiar enorme, a leitura de 3500 fica e `espurias` sai vazia."""
        medicao = medir(leituras("PT102", self.BASE + [3500]), "PT102", IDENTIDADE, limiar=1e6)
        self.assertEqual((medicao.espurias, medicao.n_validas), ([], 9))

    def test_limiar_nao_positivo(self):
        """Limiar zero ou negativo levanta ValueError."""
        for limiar in (0.0, -1.0):
            with self.subTest(limiar=limiar), self.assertRaises(ValueError):
                medir(leituras("PT101", self.BASE), "PT101", IDENTIDADE, limiar=limiar)

    def test_sobram_menos_de_duas_validas(self):
        """Se sobra só uma leitura válida, levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(leituras("PT101", [10, 11, 12]), "PT101", IDENTIDADE, limiar=0.1)

    def test_contagem_fora_do_dominio_chega_ao_chamador(self):
        """Contagem acima de 4095 faz a curva levantar ValueError, e medir não esconde."""
        with self.assertRaises(ValueError):
            medir(leituras("PT101", self.BASE + [5000]), "PT101", IDENTIDADE)

    def test_incerteza_total_nunca_fica_abaixo_da_sistematica(self):
        """A incerteza é hypot(erro padrão, sistemática), logo fica acima da sistemática."""
        medicao = medir(leituras("PT101", self.BASE * 50), "PT101", IDENTIDADE, u_sistematica=2.0)
        self.assertGreater(medicao.medida.incerteza, 2.0)
        self.assertAlmostEqual(medicao.medida.incerteza, 2.0, delta=0.05)


class TestAlturaManometricaContrato(unittest.TestCase):
    """Issue #6: altura_manometrica."""

    def test_sem_a_tag_de_succao_levanta_erro(self):
        """Sem registros de PT101, levanta ValueError."""
        with self.assertRaises(ValueError):
            altura_manometrica(leituras("PT102", [3000, 3001, 2999, 3000]), IDENTIDADE)

    def test_incerteza_cresce_com_a_sistematica(self):
        """Incerteza sistemática maior nos transmissores aumenta a incerteza da altura."""
        regs = leituras("PT101", [100, 101, 99, 100]) + leituras("PT102", [1100, 1101, 1099, 1100])
        pequena = altura_manometrica(regs, IDENTIDADE, u_sistematica=0.5)
        grande = altura_manometrica(regs, IDENTIDADE, u_sistematica=3.0)
        self.assertAlmostEqual(pequena.valor, grande.valor)
        self.assertGreater(grande.incerteza, pequena.incerteza)


if __name__ == "__main__":
    unittest.main()

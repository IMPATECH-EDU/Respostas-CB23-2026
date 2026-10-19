"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# ---------------------------------------------------------------------------------------
# Issue #7: testes de regressão do AcumuladorKahan (escritos antes da correção)
# ---------------------------------------------------------------------------------------
class TestKahanRegressao(unittest.TestCase):
    """Issue #7: a soma de Kahan tem que compensar o arredondamento."""

    def test_dez_decimos_dao_exatamente_um(self):
        """Dez parcelas de 0.1: a soma ingênua dá 0.9999999999999999 e a de Kahan, 1.0."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 10)
        # aqui a igualdade exata é o ponto: é isso que separa Kahan da soma ingênua
        self.assertEqual(kahan.total, 1.0)

    def test_parcelas_menores_que_meio_ulp(self):
        """1.0 seguido de 10000 parcelas de 1e-16: a ingênua perde todas, Kahan não perde."""
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        for acumulador in (ingenuo, kahan):
            acumulador.adicionar(1.0)
            acumulador.adicionar_todos([1e-16] * 10_000)
        self.assertEqual(ingenuo.total, 1.0)          # cada 1.0 + 1e-16 arredonda para 1.0
        self.assertAlmostEqual(kahan.total, 1.0 + 1e-12, delta=1e-15)

    def test_um_milhao_de_pulsos(self):
        """O caso do relato: 1 000 000 de parcelas de 0,1 L somam exatamente 100000.0 L."""
        kahan = AcumuladorKahan()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
        self.assertEqual(kahan.total, 100000.0)


# ---------------------------------------------------------------------------------------
# Issue #6: regras do contrato de medir que os testes de aceitação não verificam
# ---------------------------------------------------------------------------------------
IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
T0 = datetime(2026, 10, 5, 8, 0, 0)


def leituras(tag: str, contagens: list, inicio: int = 0) -> list:
    """Registros de leitura da `tag`, um a cada 6 s a partir de `inicio`."""
    return [Registro(T0 + timedelta(seconds=6 * (inicio + i)), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestMedirContrato(unittest.TestCase):
    """Issue #6: casos do contrato de medir."""

    def test_incerteza_sistematica_negativa(self):
        """u_sistematica < 0 levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(leituras("PT101", [10, 11, 9, 10]), "PT101", IDENTIDADE, u_sistematica=-0.5)

    def test_mad_zero(self):
        """Leituras todas iguais têm MAD zero: o z robusto não existe e sai ValueError."""
        with self.assertRaises(ValueError):
            medir(leituras("PT101", [1000] * 8), "PT101", IDENTIDADE)

    def test_indices_espurios_contam_so_a_tag(self):
        """Os índices de `espurias` são posições na série da tag, mesmo com outra tag no meio."""
        pt101 = leituras("PT101", [100] * 6)
        pt102 = leituras("PT102", [10, 11, 9, 10, 12, 900, 11, 10])
        intercalados = [r for par in zip(pt101, pt102) for r in par] + pt102[len(pt101):]
        m = medir(intercalados, "PT102", IDENTIDADE)
        self.assertEqual(m.espurias, [5])
        self.assertEqual(m.n_validas, 7)

    def test_sobram_menos_de_duas_validas(self):
        """Com um limiar pequeno só a mediana fica válida, e medir levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(leituras("PT101", [1, 2, 3]), "PT101", IDENTIDADE, limiar=0.5)

    def test_contagem_fora_da_curva_nao_e_tratada(self):
        """Uma contagem fora do domínio da curva deixa passar o ValueError da própria curva."""
        curta = CurvaCalibracao([0.0, 1000.0, 2000.0], [0.0, 100.0, 200.0], "linear")
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(leituras("PT102", [1500, 1600, 2500]), "PT102", curta)

    def test_limiar_menor_descarta_mais(self):
        """Uma leitura com z entre 3 e 6 fica com o limiar padrão e sai com limiar=3."""
        contagens = [10, 11, 9, 10, 12, 11, 10, 9, 15]   # o 15 tem z robusto perto de 4
        padrao = medir(leituras("PT101", contagens), "PT101", IDENTIDADE)
        rigoroso = medir(leituras("PT101", contagens), "PT101", IDENTIDADE, limiar=3.0)
        self.assertEqual((padrao.espurias, rigoroso.espurias), ([], [8]))
        self.assertTrue(math.isclose(rigoroso.medida.valor, sum(contagens[:8]) / 8))


if __name__ == "__main__":
    unittest.main()

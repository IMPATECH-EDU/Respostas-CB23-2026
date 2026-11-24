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

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")


def _registros(tag: str, contagens: list) -> list:
    """Registros de leitura da `tag`, um a cada 6 s, com as contagens dadas."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
            for i, c in enumerate(contagens)]


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestKahanRegressao(unittest.TestCase):
    """Issue #7: o AcumuladorKahan deve realmente compensar o arredondamento."""

    def test_um_milhao_de_pulsos(self):
        """Um milhão de parcelas de 0,1 somam 100000.0 com erro bem menor que o ingênuo."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([0.1] * 1_000_000)
        self.assertLess(abs(kahan.total - 100000.0), 1e-9)

    def test_melhor_que_o_ingenuo(self):
        """O erro do Kahan é estritamente menor que o do acumulador ingênuo."""
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        parcelas = [0.1] * 1_000_000
        ingenuo.adicionar_todos(parcelas)
        kahan.adicionar_todos(parcelas)
        self.assertLess(abs(kahan.total - 100000.0), abs(ingenuo.total - 100000.0))

    def test_recupera_parcelas_menores_que_a_precisao(self):
        """Dez parcelas de 1e-16 depois de 1.0 não se perdem: o total passa de 1.0."""
        kahan = AcumuladorKahan()
        kahan.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertGreater(kahan.total, 1.0)
        self.assertTrue(math.isclose(kahan.total, 1.0 + 1e-15, rel_tol=0, abs_tol=1e-16))


class TestMedirContrato(unittest.TestCase):
    """Issue #6: regras do contrato de `medir` que a aceitação não verifica."""

    def setUp(self):
        self.contagens = [10, 11, 9, 10, 12, 11, 10, 9]

    def test_u_sistematica_negativa(self):
        """Uma incerteza sistemática negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", self.contagens), "PT101", IDENTIDADE, u_sistematica=-1.0)

    def test_mad_zero(self):
        """Leituras todas iguais (MAD zero) levantam ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", [10] * 8), "PT101", IDENTIDADE)

    def test_contagem_fora_do_dominio_chega_a_quem_chamou(self):
        """Contagem fora do domínio da curva propaga o ValueError da curva."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", self.contagens + [5000]), "PT101", IDENTIDADE)

    def test_espurias_em_ordem_crescente(self):
        """Duas leituras espúrias aparecem nos índices certos, em ordem crescente."""
        regs = _registros("PT101", [500] + self.contagens + [600])
        m = medir(regs, "PT101", IDENTIDADE)
        self.assertEqual(m.espurias, [0, 9])
        self.assertEqual(m.n_validas, 8)

    def test_limiar_maior_aceita_mais_leituras(self):
        """Um limiar muito alto não descarta nenhuma leitura."""
        m = medir(_registros("PT101", self.contagens + [500]), "PT101", IDENTIDADE,
                  limiar=1e6)
        self.assertEqual(m.espurias, [])
        self.assertEqual(m.n_validas, 9)

    def test_incerteza_sistematica_nao_diminui_com_n(self):
        """Com u_sistematica grande, a incerteza total fica quase igual a ela."""
        m = medir(_registros("PT101", self.contagens * 50), "PT101", IDENTIDADE,
                  u_sistematica=3.0)
        self.assertGreaterEqual(m.medida.incerteza, 3.0)
        self.assertAlmostEqual(m.medida.incerteza, 3.0, places=1)


if __name__ == "__main__":
    unittest.main()

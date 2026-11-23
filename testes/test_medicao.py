"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
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
    """Issue #7: testes de regressão do AcumuladorKahan (escritos antes da correção)."""

    def test_kahan_um_milhao_de_decimos_da_exato(self):
        """1 000 000 parcelas de 0,1 somadas com Kahan dão exatamente 100000.0."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 1_000_000)
        self.assertEqual(acumulador.total, 100000.0)

    def test_kahan_erro_bem_menor_que_o_ingenuo(self):
        """Com 100 000 parcelas de 0,1, o erro do Kahan é pelo menos 1000 vezes menor que o do ingênuo."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        kahan.adicionar_todos([0.1] * 100_000)
        ingenuo.adicionar_todos([0.1] * 100_000)
        erro_ingenuo = abs(ingenuo.total - 10000.0)
        erro_kahan = abs(kahan.total - 10000.0)
        self.assertGreater(erro_ingenuo, 0.0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)

    def test_kahan_guarda_parcelas_pequenas(self):
        """Somar 1.0 e depois dez parcelas de 1e-16 dá 1 + 1e-15 com Kahan (o ingênuo perde todas)."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1.0] + [1e-16] * 10)
        self.assertAlmostEqual(acumulador.total - 1.0, 1e-15, delta=2e-16)


class TestMedirContrato(unittest.TestCase):
    """Issue #6: regras do contrato de medir que os testes de aceitação não verificam."""

    def setUp(self):
        self.contagens = [10, 11, 9, 10, 12, 11, 10, 9]

    def test_u_sistematica_negativa(self):
        """u_sistematica negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", self.contagens), "PT101", IDENTIDADE, u_sistematica=-1.0)

    def test_mad_zero(self):
        """Leituras todas iguais (MAD zero) levantam ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros("PT101", [10] * 8), "PT101", IDENTIDADE)

    def test_espurias_em_ordem_crescente(self):
        """Várias espúrias são devolvidas com os índices da série da tag, em ordem crescente."""
        contagens = [500] + self.contagens + [600]
        m = medir(_registros("PT101", contagens), "PT101", IDENTIDADE)
        self.assertEqual(m.espurias, [0, 9])
        self.assertEqual(m.n_validas, 8)

    def test_erro_da_curva_chega_a_quem_chamou(self):
        """Contagem fora do domínio da curva: o ValueError da curva não é engolido por medir."""
        curva_curta = CurvaCalibracao([0.0, 5.0, 11.0], [0.0, 5.0, 11.0], "linear")
        with self.assertRaises(ValueError):
            medir(_registros("PT101", self.contagens), "PT101", curva_curta)

    def test_ignora_registros_sem_contagens(self):
        """Registros da tag sem a chave contagens (alarmes) não entram na medição."""
        regs = _registros("PT102", self.contagens)
        regs.append(Registro(datetime(2026, 10, 5, 9), "ALARME", "PT102",
                             {"evento": "pressao_alta", "limite": 2000.0}))
        self.assertEqual(medir(regs, "PT102", IDENTIDADE).n_validas, 8)


if __name__ == "__main__":
    unittest.main()
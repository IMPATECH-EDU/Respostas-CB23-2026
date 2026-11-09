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


class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Testes de regressão da issue #7: o Kahan precisa compensar o arredondamento."""

    def test_um_milhao_de_pulsos(self):
        """Issue #7: 1 000 000 de pulsos de 0,1 L somam 100000.0 com o Kahan."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)
        self.assertAlmostEqual(acumulador.total, 100000.0, delta=1e-9)

    def test_mais_preciso_que_o_ingenuo(self):
        """Issue #7: com as mesmas parcelas, o erro do Kahan é menor que o do ingênuo."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
            ingenuo.adicionar(0.1)
        self.assertLess(abs(kahan.total - 100000.0), abs(ingenuo.total - 100000.0))


class TestMedir(unittest.TestCase):
    """Testes da função `medir` (issue #6), com registros sintéticos."""

    def setUp(self):
        # Curva que não muda o valor (contagem = kPa), só para os testes.
        self.curva = CurvaCalibracao([0, 2500, 5000], [0, 2500, 5000], "linear")

    def _registros(self, contagens, tag="PT101"):
        inicio = datetime(2026, 1, 1)
        return [Registro(inicio + timedelta(seconds=i), "INFO", tag, {"contagens": float(c)})
                for i, c in enumerate(contagens)]

    def test_descarta_leitura_espuria(self):
        """medir: uma leitura absurda (3000 entre valores perto de 100) fica fora da média."""
        contagens = [100, 101, 99, 100, 102, 98, 100, 101, 99, 100, 3000]
        m = medir(self._registros(contagens), "PT101", self.curva)
        self.assertEqual(m.espurias, [10])
        self.assertEqual(m.n_validas, 10)
        self.assertAlmostEqual(m.medida.valor, 100.0)

    def test_u_sistematica_negativa(self):
        """medir: u_sistematica negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(self._registros([100, 101, 99]), "PT101", self.curva, u_sistematica=-1.0)

    def test_indice_da_espuria_e_da_serie_da_tag(self):
        """medir: o índice da espúria conta só as leituras da tag, ignorando as outras tags."""
        registros = (self._registros([100, 101, 99], "PT101")
                     + self._registros([100, 101, 99, 100, 102, 98, 100, 101, 99, 100, 3000],
                                       "PT102"))
        m = medir(registros, "PT102", self.curva)
        self.assertEqual(m.espurias, [10])

    def test_incerteza_soma_em_quadratura(self):
        """medir: a incerteza total é sqrt(erro padrão² + u_sistematica²)."""
        contagens = [98, 99, 100, 101, 102, 98, 99, 100, 101, 102]
        registros = self._registros(contagens)
        sem_sistematica = medir(registros, "PT101", self.curva, u_sistematica=0.0)
        com_sistematica = medir(registros, "PT101", self.curva, u_sistematica=1.5)
        erro_padrao = sem_sistematica.desvio / math.sqrt(10)
        self.assertAlmostEqual(sem_sistematica.medida.incerteza, erro_padrao)
        self.assertAlmostEqual(com_sistematica.medida.incerteza, math.hypot(erro_padrao, 1.5))

    def test_mad_zero(self):
        """medir: se a MAD for zero (maioria das leituras iguais), levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(self._registros([100, 100, 100, 100, 100, 100, 3000]), "PT101", self.curva)

    def test_tag_com_menos_de_duas_leituras(self):
        """medir: uma tag com apenas 1 leitura levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(self._registros([100]), "PT101", self.curva)

    def test_contagem_fora_do_dominio_chega_a_quem_chamou(self):
        """medir: contagem fora do domínio da curva não é tratada e levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(self._registros([100, 101, 99, 6000]), "PT101", self.curva)


if __name__ == "__main__":
    unittest.main()
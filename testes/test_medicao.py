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


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Dois testes de regressão para a issue #7."""

    def test_acumulador_kahan_1000(self):
        """1000000 pulsos acima de 0,1 L deveria ser 100000.0."""
        kahan = AcumuladorKahan()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
        self.assertAlmostEqual(kahan.total, 100000.0)

    def test_acumulador_kahan_2997(self):
        """299798 pulsos acima de 0,1 L deveria ser 29979.8."""
        kahan = AcumuladorKahan()
        for _ in range(299798):
            kahan.adicionar(0.1)
        self.assertAlmostEqual(kahan.total, 29979.8)

class TestMedir(unittest.TestCase):
    """Dois testes para a função `medir` que não são feitos pelos testes de aceitação."""

    def setUp(self):
        """Construção dos atributos para os outros testes."""
        t0 = datetime(2027, 1, 7, 21, 58, 0)
        self.curva = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
        self.registros = lambda contagens: [Registro(t0 + timedelta(seconds=13 * i), "INFO", "PT101", {"contagens": float(c)}) for i, c in enumerate(contagens)]

    def test_u_sistematica_negativa(self):
        """u_sistematica negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(self.registros([10, 11, 9, 10]), "PT101", self.curva, u_sistematica=-1.0)

    def test_mad_zero(self):
        """Leituras todas iguais dão MAD zero e levantam ValueError."""
        with self.assertRaises(ValueError):
            medir(self.registros([10, 10, 10, 10]), "PT101", self.curva)


if __name__ == "__main__":
    unittest.main()

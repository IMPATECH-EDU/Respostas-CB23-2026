"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime
import math

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir
from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan

"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring de uma linha
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou np.allclose.
"""
from datetime import datetime
import math
import unittest

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
    """Testes de regressão da issue #7 para AcumuladorKahan."""

    def test_kahan_um_milhao_de_decimos(self):
        """Regressão #7: somar 1 000 000 de parcelas de 0,1 L devolve 100000.0."""
        acc = AcumuladorKahan()
        acc.adicionar_todos([0.1] * 1_000_000)
        self.assertAlmostEqual(acc.total, 100000.0, places=9)

    def test_kahan_parcelas_pequenas_apos_base_grande(self):
        """Regressão #7: parcelas de 1e-13 somadas a 1e4 não se perdem na soma compensada."""
        acc = AcumuladorKahan()
        acc.adicionar(1e4)
        acc.adicionar_todos([1e-13] * 10_000)
        acc.adicionar(-1e4)
        self.assertAlmostEqual(acc.total, 1e-9, places=12)


class TestMedirContrato(unittest.TestCase):
    """Testes de casos de borda do contrato de `medir` (issue #6)."""

    def _curva_identidade(self) -> CurvaCalibracao:
        return CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], metodo="linear")

    def _registros(self, valores: list[float], tag: str = "PT101") -> list[Registro]:
        t0 = datetime(2026, 1, 1, 0, 0, 0)
        return [Registro(t0, "INFO", tag, {"contagens": v}) for v in valores]

    def test_medir_u_sistematica_negativa(self):
        """Incerteza sistemática negativa levanta ValueError."""
        regs = self._registros([100.0, 102.0, 101.0])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", self._curva_identidade(), u_sistematica=-0.1)

    def test_medir_mad_zero(self):
        """Série constante (MAD igual a zero) levanta ValueError."""
        regs = self._registros([500.0, 500.0, 500.0, 500.0])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", self._curva_identidade())

    def test_medir_descarta_espurias_e_registra_indices(self):
        """Leituras espúrias são descartadas e seus índices originais retornam em `espurias`."""
        regs = self._registros([100.0, 101.0, 9999.0, 99.0, 100.5, 5000.0])
        curva = CurvaCalibracao([0.0, 5000.0, 10000.0], [0.0, 5000.0, 10000.0], metodo="linear")
        res = medir(regs, "PT101", curva, u_sistematica=1.5)
        self.assertEqual(res.espurias, [2, 5])
        self.assertEqual(res.n_validas, 4)
        self.assertAlmostEqual(res.medida.valor, 100.125)
        self.assertTrue(math.isclose(res.medida.incerteza, math.hypot(res.desvio / 2.0, 1.5)))


if __name__ == "__main__":
    unittest.main()
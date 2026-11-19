"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo
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
class TestMedirContrato(unittest.TestCase):
    """Regras do contrato de `medir` que os testes de aceitação não verificam."""

    IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")

    @staticmethod
    def _registros(tag, contagens):
        """Auxiliar: monta os registros da `tag`, um a cada 6 s, com as contagens dadas."""
        t0 = datetime(2026, 10, 5, 8, 0, 0)
        return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)})
                for i, c in enumerate(contagens)]

    def test_erros_do_contrato(self):
        """u_sistematica negativa, MAD zero e menos de 2 válidas levantam ValueError."""
        boas = self._registros("PT101", [10, 11, 9, 10, 12, 11, 10, 9])
        with self.assertRaises(ValueError):
            medir(boas, "PT101", self.IDENTIDADE, u_sistematica=-1.0)
        with self.assertRaises(ValueError):
            medir(self._registros("PT101", [10, 10, 10, 10, 11]), "PT101", self.IDENTIDADE)
        with self.assertRaises(ValueError):
            medir(self._registros("PT101", [1, 2, 3, 4, 100, 200]), "PT101", self.IDENTIDADE,
                  limiar=0.1)

    def test_espuria_baixa_e_erro_da_curva(self):
        """Espúria abaixo da mediana tem o índice certo; contagem fora do domínio da curva passa como ValueError."""
        m = medir(self._registros("PT101", [10, 11, 9, 10, 5, 12, 11, 10, 9]), "PT101",
                  self.IDENTIDADE, limiar=3.0)
        self.assertEqual(m.espurias, [4])
        with self.assertRaises(ValueError):
            medir(self._registros("PT101", [10, 11, 9, 10, 5000, 12, 11, 10, 9]), "PT101",
                  self.IDENTIDADE)
            
if __name__ == "__main__":
    unittest.main()

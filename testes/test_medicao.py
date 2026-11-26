"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

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


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoKahan(unittest.TestCase):
    """Testes de regressão do defeito de compensação da soma de Kahan."""

    def test_kahan_milhao_de_decimos(self):
        """Um milhão de parcelas de 0,1 deve totalizar 100000 sem erro acumulado."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 1_000_000)
        self.assertAlmostEqual(acumulador.total, 100_000.0, places=10)

    def test_kahan_preserva_parcelas_pequenas(self):
        """A compensação deve recuperar parcelas pequenas perdidas na soma."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1e16, 1.0, 1.0])
        self.assertEqual(acumulador.total, 1e16 + 2.0)


class TestCasosAdicionaisMedir(unittest.TestCase):
    """Casos de borda adicionais para o contrato de medir."""

    def setUp(self):
        self.curva = CurvaCalibracao([0, 100, 200], [0, 100, 200], "linear")
        t0 = datetime(2026, 10, 5, 8, 0, 0)
        self.registros = [
            Registro(t0 + timedelta(seconds=6*i), "INFO", "PT101", {"contagens": float(v)})
            for i, v in enumerate([10, 11, 9, 10, 12, 11])
        ]

    def test_medir_rejeita_incerteza_sistematica_negativa(self):
        """A incerteza sistemática negativa deve ser rejeitada."""
        with self.assertRaises(ValueError):
            medir(self.registros, "PT101", self.curva, u_sistematica=-0.1)

    def test_medir_rejeita_mad_zero(self):
        """Uma série constante tem MAD zero e não permite calcular z robusto."""
        constantes = [Registro(r.instante, r.nivel, r.tag, {"contagens": 10.0})
                      for r in self.registros]
        with self.assertRaises(ValueError):
            medir(constantes, "PT101", self.curva)

    def test_medir_propaga_erro_de_dominio_da_curva(self):
        """Contagens fora do domínio devem propagar o ValueError da calibração."""
        fora = list(self.registros)
        r = fora[-1]
        fora[-1] = Registro(r.instante, r.nivel, r.tag, {"contagens": 500.0})
        with self.assertRaises(ValueError):
            medir(fora, "PT101", self.curva)


if __name__ == "__main__":
    unittest.main()

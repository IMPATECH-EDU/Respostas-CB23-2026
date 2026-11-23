"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.medicao import medir, Medida, CurvaCalibracao, Registro
import datetime as dt


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).

class TestAcumuladorKahan(unittest.TestCase):
    """Testes de regressão da issue #7."""

    def test_absorcao(self):
        """Soma 1e-6 a 10e6 num total de 1e6 vezes."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar(1.0 * 10**6)
        acumulador.adicionar_todos([1e-6] * 10**6)
        self.assertAlmostEqual(acumulador.total, 10**6 + 1.0)

    def test_absorcao_2(self):
        """Soma 1e-6 a 10e8 num total de 1e6 vezes."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar(1.0 * 10**8)
        acumulador.adicionar_todos([1e-6] * 10**6)
        self.assertAlmostEqual(acumulador.total, 10**8 + 1.0)

class TestMedir(unittest.TestCase):
    """Testes de regressão da issue #6."""

    def test_medir(self):
        """Testa a função medir."""

        curva = CurvaCalibracao([8, 10, 12, 14], [8, 10, 12, 14])

        interval = dt.timedelta(seconds=6)
        instantes = [dt.datetime.now() + i * interval for i in range(4)]

        registros = [
            Registro(instantes[0], "INFO", "PT101", {"contagens": 10}),
            Registro(instantes[1], "INFO", "PT101", {"contagens": 12}),
            Registro(instantes[2], "INFO", "PT101", {"contagens": 11}),
            Registro(instantes[3], "INFO", "PT101", {"contagens": 9}),
        ]

        medicao = medir(registros, "PT101", curva, u_sistematica=0.5, limiar=2.0)

        self.assertIsInstance(medicao.medida, Medida)
        self.assertAlmostEqual(medicao.medida.valor, 10.5)  # média das válidas
        self.assertEqual(medicao.n_validas, 4)  # número de leituras válidas

    def test_value_errors(self):
        """Testa a função medir com menos de duas leituras válidas e com u_sistematica negativo."""

        curva = CurvaCalibracao([1, 2, 3, 4], [1, 4, 9, 16])

        interval = dt.timedelta(seconds=6)
        instantes = [dt.datetime.now() + i * interval for i in range(4)]

        registros = [
            Registro(instantes[0], "INFO", "PT101", {"contagens": 2}),
            Registro(instantes[1], "INFO", "PT101", {"contagens": 2.5}),
            Registro(instantes[2], "INFO", "PT101", {"contagens": 3}),
            Registro(instantes[3], "INFO", "PT101", {"contagens": 99}),
        ]

        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva, u_sistematica=0.5, limiar=2.0)

        with self.assertRaises(ValueError):
            medir(registros, "sensor1", curva, u_sistematica=-1.0, limiar=2.0)

if __name__ == "__main__":
    unittest.main()

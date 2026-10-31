"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo ,  AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import ler_log
from elevatoria.medicao import medir

class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)

# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TesteAcumuladorKahRegressao(unittest.TestCase):
    """Teste de regressão do 'AcumuladorKahan' da Issue #7:a correção do Kahan não pode ser zero"""
    def test_dez_decimos(self):
        """São 10 parcelas de valores iguais a 0.1, o total é 1.0"""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 10)
        self.assertEqual(acumulador.total, 1.0)

    def test_comparacao_kahan_ingenuo(self):
        """Numa soma grande, como a de 100 mil parcelas, o erro do Kahan é menor do que o erro do ingenuo"""
        ingenuo = AcumuladorIngenuo()
        kahan = AcumuladorKahan()
        ingenuo.adicionar_todos([0.1] * 10 ** 5)
        kahan.adicionar_todos([0.1] * 10 ** 5)
        erro_ingenuo = abs(ingenuo.total - 10 ** 4)
        erro_kahan = abs(kahan.total - 10 ** 4)
        self.assertLess(erro_kahan, erro_ingenuo)

class TestMedirRegras(unittest.TestCase):
    """Regras do contrato de medir que os testes de aceitação não verificam"""
    def test_incerteza_negativa(self):
        """Com u_sistematica negativa, medir levanta ValueError"""
        texto = ("2026-10-05 08:00:00 INFO PT101 contagens=100\n"
                 "2026-10-05 08:00:06 INFO PT101 contagens=101\n"
                 "2026-10-05 08:00:12 INFO PT101 contagens=102\n")
        registros, _ = ler_log(texto)
        curva = CurvaCalibracao([0, 2000, 4095], [0, 2000, 4095], "linear")
        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva, u_sistematica=-1.0)

    def test_mad_zero(self):
            """Com todas as leituras iguais, a MAD é zero e medir levanta ValueError"""
            texto = ("2026-10-05 08:00:00 INFO PT101 contagens=100\n"
                     "2026-10-05 08:00:06 INFO PT101 contagens=100\n"
                     "2026-10-05 08:00:12 INFO PT101 contagens=100\n")
            registros, _ = ler_log(texto)
            curva = CurvaCalibracao([0, 2000, 4095], [0, 2000, 4095], "linear")
            with self.assertRaises(ValueError):
                medir(registros, "PT101", curva, u_sistematica=1.0)

if __name__ == "__main__":
    unittest.main()
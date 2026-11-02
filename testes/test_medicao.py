"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo,AcumuladorKahan
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
class TestAcumuladorKahan(unittest.TestCase):
    """Regressão da issue #7: o AcumuladorKahan não compensava o arredondamento."""
 
    def test_um_milhao_de_pulsos(self):
        """1 000 000 de parcelas de 0,1 L devem somar exatamente 100000.0, e não 100000.00000133288"""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 1_000_000)
        self.assertEqual(acumulador.total, 100000.0)
 
    def test_erro_do_kahan_e_bem_menor_que_o_do_ingenuo(self):
        """Com 100_000 parcelas de 0,1 L, o erro do Kahan é no mínimo 1000 vezes menor."""
        ingenuo, kahan = AcumuladorIngenuo(), AcumuladorKahan()
        for acumulador in (ingenuo, kahan):
            acumulador.adicionar_todos([0.1] * 100_000)
        erro_ingenuo = abs(ingenuo.total - 10_000.0)
        erro_kahan = abs(kahan.total - 10_000.0)
        self.assertGreater(erro_ingenuo, 0.0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)

class TestMedirContrato(unittest.TestCase):
    """Issue #6: regras do contrato de `medir` que os testes de aceitação não verificam."""
 
    def test_incerteza_sistematica_negativa_levanta_valueerror(self):
        """u_sistematica < 0 não faz sentido e deve levantar ValueError."""
        regs = _registros("PT101", [10, 11, 9, 10, 12, 11, 10, 9])
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, u_sistematica=-0.5)
 
    def test_mad_zero_levanta_valueerror(self):
        """Com todas as leituras iguais a MAD é zero e o z robusto não existe: ValueError."""
        regs = _registros("PT101", [10] * 8)
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE)

if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
import math
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir

IDENTIDADE = CurvaCalibracao([0.0, 2000.0, 4095.0], [0.0, 2000.0, 4095.0], "linear")
def registros(tag, contagens):
    """Registros de leitura da `tag`, um a cada 6 s, com as contagens dadas."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(t0 + timedelta(seconds=6 * i), "INFO", tag, {"contagens": float(c)}) for i, c in enumerate(contagens)]

def somar(acumulador, valores):
    """Soma `valores` com o `acumulador` e devolve o total."""
    acumulador.adicionar_todos(valores)
    return acumulador.total

class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)

class TestKahanRegressao(unittest.TestCase):
    """Issue #7: o AcumuladorKahan não compensava o arredondamento."""

def test_dez_parcelas_de_0_1_somam_exatamente_1(self):
    """Com a compensação, 10 parcelas de 0,1 dão exatamente 1.0 (a ingênua dá 0.999...)."""
    self.assertEqual(somar(AcumuladorKahan(), [0.1] * 10), 1.0)

def test_um_milhao_de_pulsos(self):
    """O caso do relato: 1.000.000 de parcelas de 0,1 devem dar 100000.0, sem o erro de 1e-6."""
    total = somar(AcumuladorKahan(), [0.1] * 1_000_000)
    self.assertLess(abs(total - 100000.0), 1e-9)

def test_parcela_pequena_nao_some_perto_de_numero_grande(self):
    """Dez parcelas de 1.0 somadas a 1e16 não se perdem: o total é 1e16 + 10."""
    valores = [1e16] + [1.0] * 10
    self.assertEqual(somar(AcumuladorKahan(), valores), math.fsum(valores))

def test_kahan_fica_mais_perto_do_exato_que_o_ingenuo(self):
    """Com 100 mil parcelas, o erro do Kahan (contra math.fsum) é bem menor que o do ingênuo."""
    valores = [0.1, 0.2, 0.3, 0.7] * 25_000
    exato = math.fsum(valores)
    erro_kahan = abs(somar(AcumuladorKahan(), valores) - exato)
    erro_ingenuo = abs(somar(AcumuladorIngenuo(), valores) - exato)
    self.assertGreater(erro_ingenuo, 0.0)
    self.assertLess(erro_kahan, erro_ingenuo / 1000)
    
# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

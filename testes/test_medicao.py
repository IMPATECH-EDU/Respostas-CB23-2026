"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan

import os
import sys
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if raiz not in sys.path:
    sys.path.append(raiz)

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir, Medida
from fornecido.medida import Medida

class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestAcumuladorKahan(unittest.TestCase):

    def test_soma_um_milhao_de_decimos(self):
        """Verifica a precisão da soma de um milhão de décimos."""
        acumulador = AcumuladorKahan()

        for _ in range(1_000_000):
            acumulador.adicionar(0.1)

        self.assertAlmostEqual(acumulador.total, 100000.0, places=9)

    def test_kahan_e_mais_preciso_que_ingenuo(self):
        """Verifica que a soma de Kahan é mais precisa que a soma ingenua."""
        ingenuo = AcumuladorIngenuo()
        kahan = AcumuladorKahan()

        for _ in range(1_000_000):
            ingenuo.adicionar(0.1)
            kahan.adicionar(0.1)

        erro_ingenuo = abs(ingenuo.total - 100000.0)
        erro_kahan = abs(kahan.total - 100000.0)

        self.assertLess(erro_kahan, erro_ingenuo)

class TestMedir(unittest.TestCase):

    def test_u_sistematica_negativa(self):
        """Verifica se incerteza sistemática negativa gera ValueError."""
        
        inst= datetime.strptime("2026-05-10 08:00:00", "%Y-%m-%d %H:%M:%S")
        
        registros = [
            Registro(instante=inst, nivel= "INFO", tag="PT101", valores={"contagens": 100}),
            Registro(instante=inst, nivel= "INFO", tag="PT101", valores={"contagens": 110}),
        ]

        curva=CurvaCalibracao()
        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva, u_sistematica=-1)


if __name__ == "__main__":
    unittest.main()

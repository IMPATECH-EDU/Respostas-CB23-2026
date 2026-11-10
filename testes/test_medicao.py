"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime, timedelta

from elevatoria.acumuladores import AcumuladorIngenuo
from elevatoria.acumuladores import AcumuladorKahan
from elevatoria.medicao import medir
from elevatoria.dados import Registro
from fornecido.testes_aceitacao.test_aceitacao_m2 import IDENTIDADE


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestAcumuladorKahanExemplo(unittest.TestCase):
    def test_mi_parcelas(self):
        '''Acúmulo de um milhão de parcelas de 0.1 e depois comparação do erro com o ingênuo'''
        kahan = AcumuladorKahan()
        ingenuo = AcumuladorIngenuo()

        for _ in range(int(1e6)):
            kahan.adicionar(0.1)
            ingenuo.adicionar(0.1)

        self.assertTrue((abs(kahan.total - 1e5)) < (abs(ingenuo.total - 1e5)/1e3))

    def test_dif_grande_uso(self):
        '''Perda de precisão por diferença de grandeza (1e8 e [1e-5]*[1e4])'''
        kahan = AcumuladorKahan()
        kahan.adicionar(1e8)

        for _ in range(int(1e4)):
            kahan.adicionar(1e-5)

        val_esperado = 1e8 + 0.1
        self.assertTrue(abs(kahan.total - val_esperado) < 1e-5)


class TestMedicaoMedir(unittest.TestCase):
    '''2 testes de medir que os testes de aceitação não cobrem'''
    def test_u_sistematica_negativo(self):
        '''Verifica se um u_sistematica menor que 0 levantará ValueError'''
        with self.assertRaises(ValueError):
            u_sistematica = -1
            medir([], "PT101", IDENTIDADE, u_sistematica)

    def test_validas_menor_2(self):
        '''Verfica se após a remoção das espurias, sobrarão 2 ou mais valores válidos'''
        t0 = datetime(2026, 10, 5, 8, 0, 0)
        regs = [
            Registro(t0, "INFO", "PT101", {"contagens": 100.0}),
            Registro(t0 + timedelta(seconds=6), "INFO", "PT101", {"contagens": 101.0}),
            Registro(t0 + timedelta(seconds=12), "INFO", "PT101", {"contagens": 1000.0}),
        ]
        with self.assertRaises(ValueError):
            medir(regs, "PT101", IDENTIDADE, limiar=0.1)

if __name__ == "__main__":
    unittest.main()

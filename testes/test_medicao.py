"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


if __name__ == "__main__":
    unittest.main()

class TestKahanRegressao(unittest.TestCase):
    """Testes de regressão da issue #7."""

    def test_kahan_compensa_muitas_parcelas_de_decimo(self):
        """Regressão #7: um milhão de décimos deve totalizar 100000 sem erro acumulado relevante."""
        from elevatoria.acumuladores import AcumuladorKahan
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 1_000_000)
        self.assertAlmostEqual(acumulador.total, 100000.0, delta=1e-9)

    def test_kahan_tem_erro_menor_que_soma_ingenua(self):
        """Regressão #7: a soma compensada deve melhorar a soma direta em muitas parcelas."""
        from elevatoria.acumuladores import AcumuladorKahan
        from elevatoria.acumuladores import AcumuladorIngenuo
        parcelas = [0.1] * 100_000
        ingenuo = AcumuladorIngenuo()
        kahan = AcumuladorKahan()
        ingenuo.adicionar_todos(parcelas)
        kahan.adicionar_todos(parcelas)
        self.assertLess(abs(kahan.total - 10000.0), abs(ingenuo.total - 10000.0))

    def test_medir_rejeita_incerteza_sistematica_negativa(self):
        """A incerteza sistemática não pode ser negativa."""
        from elevatoria.dados import Registro
        from elevatoria.calibracao import CurvaCalibracao
        from elevatoria.medicao import medir
        from datetime import datetime, timedelta
        inicio = datetime(2026, 10, 5, 8)
        regs = [Registro(inicio + timedelta(seconds=6*i), "INFO", "PT101", {"contagens": float(c)})
                for i, c in enumerate([10, 11, 9, 10])]
        curva = CurvaCalibracao([0, 20, 40], [0, 20, 40], "linear")
        with self.assertRaises(ValueError):
            medir(regs, "PT101", curva, u_sistematica=-1.0)

    def test_medir_rejeita_mad_zero(self):
        """Uma série constante tem MAD zero e não permite calcular o z robusto."""
        from elevatoria.dados import Registro
        from elevatoria.calibracao import CurvaCalibracao
        from elevatoria.medicao import medir
        from datetime import datetime, timedelta
        inicio = datetime(2026, 10, 5, 8)
        regs = [Registro(inicio + timedelta(seconds=6*i), "INFO", "PT101", {"contagens": 10.0})
                for i in range(4)]
        curva = CurvaCalibracao([0, 20, 40], [0, 20, 40], "linear")
        with self.assertRaises(ValueError):
            medir(regs, "PT101", curva)

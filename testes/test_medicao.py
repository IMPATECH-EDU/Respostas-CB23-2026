"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.medicao import medir, altura_manometrica


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Testes de regressão para a Issue #7 (defeito no AcumuladorKahan)."""

    def test_regressao_um_milhao_de_decimos(self):
        """Testa se o AcumuladorKahan soma 1.000.000 de parcelas 0.1 sem acumular erro flutuante."""
        acum = AcumuladorKahan()
        for _ in range(1_000_000):
            acum.adicionar(0.1)
        self.assertEqual(acum.total, 100000.0)

    def test_regressao_desempenho_superior_ao_ingenuo(self):
        """Verifica se o erro do AcumuladorKahan é estritamente menor que o do AcumuladorIngenuo."""
        kahan = AcumuladorKahan()
        ingenuo = AcumuladorIngenuo()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
            ingenuo.adicionar(0.1)
        erro_kahan = abs(kahan.total - 100000.0)
        erro_ingenuo = abs(ingenuo.total - 100000.0)
        self.assertLess(erro_kahan, erro_ingenuo)


class TestMedicaoContrato(unittest.TestCase):
    """Testes para cobrir regras do contrato de medicao.py (Issue #6)."""

    def test_medir_tag_inexistente_lanca_value_error(self):
        """Garante que a função medir levanta ValueError caso a tag informada não exista nos registros."""
        registros = [{"tag": "PT101", "contagens": 1000}]
        with self.assertRaises(ValueError):
            medir(registros, "TAG_INEXISTENTE", lambda x: float(x), u_sistematica=1.0)

    def test_medir_descarta_outlier_com_z_score_robusto(self):
        """Garante que leituras espúrias (outliers) são filtradas pela mediana e MAD antes da média."""
        registros = [{"tag": "PT101", "contagens": 1000}] * 20 + [{"tag": "PT101", "contagens": 99999}]
        res = medir(registros, "PT101", lambda x: float(x), u_sistematica=0.1)
        self.assertAlmostEqual(res.medida.valor, 1000.0, places=2)


if __name__ == "__main__":
    unittest.main()
"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
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
class TestKahanRegressao(unittest.TestCase):
    def test_soma_um_milhao_de_decimos(self):
        """Totaliza um milhão de parcelas de 0,1 L com erro sob controle."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)

        self.assertAlmostEqual(acumulador.total, 100_000.0, delta=1e-9)

    def test_recupera_duas_parcelas_pequenas(self):
        """Recupera duas parcelas unitárias somadas após um valor grande."""
        acumulador = AcumuladorKahan()
        for parcela in (1e16, 1.0, 1.0, -1e16):
            acumulador.adicionar(parcela)

        self.assertAlmostEqual(acumulador.total, 2.0, delta=1e-12)


class TestMedirContrato(unittest.TestCase):
    def test_rejeita_incerteza_sistematica_negativa(self):
        """Rejeita uma incerteza sistemática menor que zero."""
        curva = CurvaCalibracao(
            [0.0, 20.0, 40.0], [0.0, 20.0, 40.0], "linear"
        )
        registros, _ = ler_log(
            "2026-10-05 08:00:00 INFO PT101 contagens=10\n"
            "2026-10-05 08:00:06 INFO PT101 contagens=12"
        )

        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva, u_sistematica=-1.0)

    def test_propaga_erro_de_contagem_fora_do_dominio(self):
        """Propaga ValueError da curva para uma contagem fora do domínio."""
        curva = CurvaCalibracao(
            [0.0, 20.0, 40.0], [0.0, 20.0, 40.0], "linear"
        )
        registros, _ = ler_log(
            "2026-10-05 08:00:00 INFO PT101 contagens=10\n"
            "2026-10-05 08:00:06 INFO PT101 contagens=50"
        )

        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva)

if __name__ == "__main__":
    unittest.main()

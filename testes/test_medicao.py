"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime

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


class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Regressões da issue #7: a compensação deve superar a soma ingênua."""

    def test_kahan_um_milhao_de_decimos(self) -> None:
        """Kahan totaliza um milhão de pulsos de 0,1 L sem acumular o erro da soma ingênua."""
        ingenuo = AcumuladorIngenuo()
        kahan = AcumuladorKahan()
        for _ in range(1_000_000):
            ingenuo.adicionar(0.1)
            kahan.adicionar(0.1)

        esperado = 100_000.0
        self.assertGreater(abs(ingenuo.total - esperado), 1e-7)
        self.assertAlmostEqual(kahan.total, esperado, delta=1e-10)

    def test_kahan_recupera_unidades_entre_valores_grandes(self) -> None:
        """Kahan recupera duas unidades perdidas pela soma ingênua entre valores grandes."""
        parcelas = [1e16, 1.0, 1.0, -1e16]
        ingenuo = AcumuladorIngenuo()
        kahan = AcumuladorKahan()
        ingenuo.adicionar_todos(parcelas)
        kahan.adicionar_todos(parcelas)

        self.assertAlmostEqual(ingenuo.total, 0.0, delta=1e-12)
        self.assertAlmostEqual(kahan.total, 2.0, delta=1e-12)


def _registros(contagens: list[float]) -> list[Registro]:
    """Cria leituras de PT101 na ordem das contagens fornecidas."""
    instante = datetime(2026, 10, 5, 8, 0, 0)
    return [Registro(instante, "INFO", "PT101", {"contagens": c}) for c in contagens]


class TestMedirContrato(unittest.TestCase):
    """Regras de medir não verificadas pelos testes de aceitação."""

    def test_rejeita_mad_zero(self) -> None:
        """MAD zero levanta ValueError mesmo quando a série não é constante."""
        identidade = CurvaCalibracao([0, 1, 2], [0, 1, 2], "linear")
        for contagens in [[1, 1, 1, 1], [1, 1, 1, 2]]:
            with self.subTest(contagens=contagens), self.assertRaises(ValueError):
                medir(_registros(contagens), "PT101", identidade)

    def test_filtra_apos_calibracao_nao_linear(self) -> None:
        """O z robusto identifica espúrias nos valores calibrados pela curva não linear."""
        quadratica = CurvaCalibracao([0, 20, 40], [0, 400, 1600], "spline")
        contagens = [10, 11, 12, 13, 14, 15, 16, 30]

        resultado = medir(_registros(contagens), "PT101", quadratica)

        self.assertEqual(resultado.espurias, [7])
        self.assertEqual(resultado.n_validas, 7)
        # As pressões válidas são 100, 121, 144, 169, 196, 225 e 256: média 173.
        self.assertAlmostEqual(resultado.medida.valor, 173.0)


if __name__ == "__main__":
    unittest.main()

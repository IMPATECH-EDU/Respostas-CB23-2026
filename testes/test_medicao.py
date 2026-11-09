"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan

from datetime import datetime, timedelta

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir


def criar_registros(tag: str, contagens: list[float]) -> list[Registro]:
    """Cria registros fictícios de uma tag para os testes."""
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    return [
        Registro(
            t0 + timedelta(seconds=6 * i),
            "INFO",
            tag,
            {"contagens": float(c)}
        )
        for i, c in enumerate(contagens)
    ]


class TestMedir(unittest.TestCase):

    def test_rejeita_incerteza_sistematica_negativa(self):
        """Rejeita uma incerteza sistemática negativa."""
        contagens = [10, 11, 9, 10, 12, 11, 10, 9]
        registros = criar_registros("PT101", contagens)

        curva = CurvaCalibracao(
            [0.0, 2000.0, 4095.0],
            [0.0, 2000.0, 4095.0],
            "linear"
        )

        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva, u_sistematica=-1.0)

    def test_rejeita_mad_zero(self):
        """Rejeita leituras cuja MAD é zero."""
        contagens = [10] * 8
        registros = criar_registros("PT101", contagens)

        curva = CurvaCalibracao(
            [0.0, 2000.0, 4095.0],
            [0.0, 2000.0, 4095.0],
            "linear"
        )

        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva)

    def test_repassa_erro_da_curva(self):
        """Repassa o erro quando uma contagem está fora do domínio da curva."""
        contagens = [5000] * 8
        registros = criar_registros("PT101", contagens)

        curva = CurvaCalibracao(
            [0.0, 2000.0, 4095.0],
            [0.0, 2000.0, 4095.0],
            "linear"
        )

        with self.assertRaises(ValueError):
            medir(registros, "PT101", curva)

class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).
class TestRegressaoIssue7(unittest.TestCase):

    def test_milhao_de_pulsos(self):
        """Acumula um milhão de parcelas de 0,1 L com precisão."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos(0.1 for _ in range(1_000_000))

        self.assertAlmostEqual(acumulador.total, 100000.0, places=9)

    def test_compensacao_de_parcelas_pequenas(self):
        """Preserva parcelas pequenas somadas entre valores muito grandes."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1e16, 1.0, 1.0, -1e16])

        self.assertAlmostEqual(acumulador.total, 2.0, places=12)


if __name__ == "__main__":
    unittest.main()

"""Testes do Marco 2: compensação numérica e medição robusta."""
import math
import unittest
from datetime import datetime
from itertools import repeat

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestKahanRegressao(unittest.TestCase):
    """Regressões da compensação de arredondamento da issue #7."""

    def test_pulsos_decimais(self) -> None:
        """Cem mil pulsos decimais não acumulam o erro da soma ingênua."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos(repeat(0.1, 100_000))
        self.assertAlmostEqual(acumulador.total, 10_000.0, delta=1e-11)

    def test_parcelas_menores_que_ulp(self) -> None:
        """Parcelas unitárias perdidas isoladamente são recuperadas pela compensação."""
        acumulador = AcumuladorKahan()
        parcelas = [float(2 ** 54), 1.0, 1.0, 1.0, 1.0]
        acumulador.adicionar_todos(parcelas)
        self.assertAlmostEqual(acumulador.total, math.fsum(parcelas), delta=0.5)


def _leituras(valores: list[float]) -> list[Registro]:
    return [Registro(datetime(2026, 10, 5), "INFO", "PT102", {"contagens": x})
            for x in valores]


class TestContratosMedicao(unittest.TestCase):
    """Validações e indexação da medição robusta."""

    def setUp(self) -> None:
        """Prepara uma curva identidade com domínio de zero a cem."""
        self.curva = CurvaCalibracao([0, 50, 100], [0, 50, 100], "linear")

    def test_mad_zero(self) -> None:
        """Leituras idênticas são rejeitadas porque não permitem calcular o z robusto."""
        with self.assertRaisesRegex(ValueError, "MAD"):
            medir(_leituras([8, 8, 8, 8]), "PT102", self.curva)

    def test_incerteza_negativa(self) -> None:
        """Incerteza sistemática negativa é rejeitada antes da medição."""
        with self.assertRaisesRegex(ValueError, "u_sistematica"):
            medir(_leituras([8, 9, 10]), "PT102", self.curva, -0.5)

    def test_filtragem_deixa_uma_leitura(self) -> None:
        """Um limiar restritivo que deixa apenas a mediana causa ValueError."""
        with self.assertRaisesRegex(ValueError, "menos de duas"):
            medir(_leituras([1, 2, 3]), "PT102", self.curva, limiar=0.1)

    def test_extrapolacao_propaga_erro(self) -> None:
        """Uma leitura fora do domínio não é descartada silenciosamente como espúria."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(_leituras([8, 9, 101]), "PT102", self.curva)

    def test_indices_da_tag_ignoram_eventos(self) -> None:
        """Os índices das espúrias referem-se só às contagens da tag solicitada."""
        regs = _leituras([10, 11, 9, 10, 12, 11, 10, 9, 90])
        regs.insert(0, Registro(datetime(2026, 10, 5), "INFO", "B1", {"evento": "partida"}))
        regs.insert(4, Registro(datetime(2026, 10, 5), "ALARME", "PT102", {"evento": "alta"}))
        resultado = medir(regs, "PT102", self.curva)
        self.assertEqual(resultado.espurias, [8])
        self.assertEqual(resultado.n_validas, 8)

    def test_incerteza_sistematica_nao_diminui(self) -> None:
        """Repetir a amostra reduz só a contribuição aleatória da incerteza."""
        valores = [8, 9, 10, 11]
        curta = medir(_leituras(valores), "PT102", self.curva, 2.0)
        longa = medir(_leituras(valores * 20), "PT102", self.curva, 2.0)
        self.assertGreater(longa.medida.incerteza, 2.0)
        self.assertLess(longa.medida.incerteza, curta.medida.incerteza)


if __name__ == "__main__":
    unittest.main()

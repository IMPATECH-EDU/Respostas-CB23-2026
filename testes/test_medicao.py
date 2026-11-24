"""Testes do Marco 2 da estação elevatória."""
import unittest
from itertools import repeat

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro, ler_log
from elevatoria.medicao import medir


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato fornecido pela disciplina."""

    def test_sem_parcelas(self) -> None:
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestRegressaoKahan(unittest.TestCase):
    """Casos em que a compensação altera o resultado representável."""

    def test_pulsos_de_um_decimo(self) -> None:
        """Um milhão de pulsos de 0,1 L totaliza exatamente 100000 L."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos(repeat(0.1, 1_000_000))
        self.assertEqual(acumulador.total, 100_000.0)

    def test_duas_unidades_apos_dois_elevado_a_53(self) -> None:
        """Duas unidades somadas separadamente recuperam um passo representável."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([float(2**53), 1.0, 1.0])
        self.assertEqual(acumulador.total, float(2**53 + 2))


class TestMedirContrato(unittest.TestCase):
    """Casos de erro do contrato de medição."""

    def setUp(self) -> None:
        """Usa uma calibração identidade com domínio de zero a dez."""
        self.curva = CurvaCalibracao([0, 5, 10], [0, 5, 10], "linear")

    def leituras(self, valores: list[int]) -> list[Registro]:
        """Monta registros da PT101 com o leitor do Marco 1."""
        linhas = [f"2026-10-05 08:00:00 INFO PT101 contagens={v}" for v in valores]
        registros, _ = ler_log("\n".join(linhas))
        return registros

    def test_mad_zero(self) -> None:
        """Uma maioria de valores idênticos pode zerar a MAD mesmo com variação."""
        with self.assertRaises(ValueError):
            medir(self.leituras([2, 2, 2, 8]), "PT101", self.curva)

    def test_uma_valida_apos_filtro(self) -> None:
        """Se só a mediana sobreviver ao filtro, falta um ponto para estimar o desvio."""
        with self.assertRaises(ValueError):
            medir(self.leituras([1, 2, 3]), "PT101", self.curva, limiar=0.1)

    def test_incerteza_negativa(self) -> None:
        """Uma incerteza sistemática negativa é rejeitada."""
        with self.assertRaises(ValueError):
            medir(self.leituras([1, 2, 3]), "PT101", self.curva, u_sistematica=-1)

    def test_fora_do_dominio(self) -> None:
        """Uma contagem fora da calibração propaga o erro de domínio da curva."""
        with self.assertRaisesRegex(ValueError, "fora do domínio"):
            medir(self.leituras([1, 2, 11]), "PT101", self.curva)


if __name__ == "__main__":
    unittest.main()

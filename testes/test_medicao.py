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


class TestCompensacao(unittest.TestCase):
    """Regressões que tornam visível o arredondamento de uma soma."""

    def test_dez_mil_decimos(self) -> None:
        """Dez mil décimos totalizam mil dentro de uma tolerância de 1e-12."""
        soma = AcumuladorKahan()
        soma.adicionar_todos([0.1] * 10_000)
        self.assertAlmostEqual(soma.total, 1000.0, delta=1e-12)

    def test_duas_unidades_apos_total_grande(self) -> None:
        """A primeira unidade perdida em 2**53 é recuperada ao somar a segunda."""
        soma = AcumuladorKahan()
        soma.adicionar_todos([2.0**53, 1.0, 1.0])
        self.assertAlmostEqual(soma.total, float(2**53 + 2), delta=0.25)


class TestLimitesDaMedicao(unittest.TestCase):
    """Casos que impedem o cálculo de uma pressão com incerteza."""

    curva = CurvaCalibracao([0, 10, 20], [0, 10, 20], "linear")

    def _leituras(self, contagens: list[int]) -> list[Registro]:
        """Monta leituras de um transmissor para isolar o filtro estatístico."""
        instante = datetime(2026, 10, 5, 8)
        return [Registro(instante, "INFO", "PT102", {"contagens": float(c)}) for c in contagens]

    def test_mad_zero(self) -> None:
        """Três valores centrais idênticos tornam a MAD nula, mesmo com um valor distante."""
        with self.assertRaisesRegex(ValueError, "MAD"):
            medir(self._leituras([5, 5, 5, 16]), "PT102", self.curva)

    def test_filtro_deixa_so_a_mediana(self) -> None:
        """Um limiar estreito pode deixar uma única leitura, insuficiente para o desvio."""
        with self.assertRaisesRegex(ValueError, "duas leituras válidas"):
            medir(self._leituras([3, 6, 9]), "PT102", self.curva, limiar=0.1)

    def test_incerteza_sistematica_negativa(self) -> None:
        """Uma incerteza de instrumento negativa invalida a medição."""
        with self.assertRaises(ValueError):
            medir(self._leituras([3, 6, 9]), "PT102", self.curva, u_sistematica=-1)

    def test_contagem_fora_da_calibracao(self) -> None:
        """O erro de domínio da curva chega ao chamador antes do descarte de espúrias."""
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(self._leituras([3, 6, 25]), "PT102", self.curva)


if __name__ == "__main__":
    unittest.main()

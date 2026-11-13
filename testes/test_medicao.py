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


class TestAcumuladorKahan(unittest.TestCase):
    """Testes de regressão da compensação de arredondamento (issue #7)."""

    def test_um_milhao_de_pulsos(self) -> None:
        """Um milhão de parcelas de 0,1 L totaliza 100000 L com erro mínimo."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)

        self.assertAlmostEqual(acumulador.total, 100_000.0, places=9)

    def test_parcelas_pequenas_entre_grandes(self) -> None:
        """A compensação preserva duas unidades entre parcelas grandes que se anulam."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1e16, 1.0, 1.0, -1e16])

        self.assertAlmostEqual(acumulador.total, 2.0)


class TestMedir(unittest.TestCase):
    """Verifica validações de medir não cobertas pelos testes de aceitação."""

    def setUp(self) -> None:
        """Prepara uma curva identidade para conferir as validações."""
        self.curva = CurvaCalibracao([0, 2000, 4095], [0, 2000, 4095], "linear")

    def _registros(self, contagens: list[float]) -> list[Registro]:
        """Cria registros de PT101 com as contagens recebidas."""
        instante = datetime(2026, 10, 5, 8, 0, 0)
        return [Registro(instante, "INFO", "PT101", {"contagens": c}) for c in contagens]

    def test_incerteza_negativa(self) -> None:
        """Uma incerteza sistemática negativa levanta ValueError."""
        registros = self._registros([10.0, 11.0, 12.0])
        with self.assertRaisesRegex(ValueError, "incerteza"):
            medir(registros, "PT101", self.curva, u_sistematica=-1.0)

    def test_mad_zero(self) -> None:
        """Leituras iguais produzem MAD zero e levantam ValueError."""
        registros = self._registros([10.0, 10.0, 10.0])
        with self.assertRaisesRegex(ValueError, "MAD"):
            medir(registros, "PT101", self.curva)

    def test_poucas_validas_apos_filtro(self) -> None:
        """O filtro não pode deixar menos de duas leituras válidas."""
        registros = self._registros([10.0, 11.0, 12.0])
        with self.assertRaisesRegex(ValueError, "leituras válidas"):
            medir(registros, "PT101", self.curva, limiar=0.1)

    def test_contagem_fora_do_dominio(self) -> None:
        """O erro de domínio da curva chega a quem chamou medir."""
        registros = self._registros([10.0, 11.0, 5000.0])
        with self.assertRaisesRegex(ValueError, "domínio"):
            medir(registros, "PT101", self.curva)


if __name__ == "__main__":
    unittest.main()

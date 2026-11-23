"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import ler_log
from elevatoria.medicao import medir

from elevatoria.acumuladores import AcumuladorKahan

from elevatoria.acumuladores import AcumuladorIngenuo


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestKahan(unittest.TestCase):
    """Regressões da soma compensada."""

    def test_pulsos_repetidos(self) -> None:
        """Cem mil parcelas de 0,1 totalizam 10000 com compensação."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([0.1] * 100_000)
        self.assertAlmostEqual(acumulador.total, 10_000.0, delta=1e-10)

    def test_parcelas_menores_que_a_resolucao_da_soma(self) -> None:
        """Parcelas isoladas que se perderiam somam uma diferença representável."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1e16, 1.0, 1.0, -1e16])
        self.assertAlmostEqual(acumulador.total, 2.0)



class TestMedirValidacao(unittest.TestCase):
    """Casos em que a medição deve recusar os dados."""

    def test_rejeita_mad_zero(self) -> None:
        """Leituras idênticas não permitem calcular o z robusto."""
        linha = "2026-10-05 08:00:00 INFO PT102 contagens=2"
        registros, _ = ler_log("\n".join([linha] * 3))
        curva = CurvaCalibracao([0, 2, 4], [0, 20, 40])
        with self.assertRaisesRegex(ValueError, "MAD"):
            medir(registros, "PT102", curva)

    def test_rejeita_incerteza_negativa(self) -> None:
        """A medição recusa incerteza sistemática negativa."""
        texto = "\n".join(f"2026-10-05 08:00:00 INFO PT102 contagens={x}" for x in [1, 2, 3])
        registros, _ = ler_log(texto)
        curva = CurvaCalibracao([0, 2, 4], [0, 20, 40])
        with self.assertRaisesRegex(ValueError, "sistemática"):
            medir(registros, "PT102", curva, u_sistematica=-1)


if __name__ == "__main__":
    unittest.main()

"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime
from itertools import repeat

import numpy as np
from scipy import stats

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self) -> None:
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Acrescente abaixo as suas classes de teste, começando pelos testes de regressão da
# issue #7 (escreva-os ANTES de corrigir o defeito e confirme que falham).


class TestRegressaoKahan(unittest.TestCase):
    """Expõe a perda de parcelas pequenas antes da correção da issue #7."""

    def test_milhao_de_decimos(self) -> None:
        """Um milhão de décimos totaliza 100000 L com erro inferior a 1e-10 L."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos(repeat(0.1, 1_000_000))
        self.assertAlmostEqual(acumulador.total, 100_000.0, delta=1e-10)

    def test_parcelas_pequenas_entre_grandes(self) -> None:
        """Preserva duas unidades somadas entre parcelas grandes que se cancelam."""
        acumulador = AcumuladorKahan()
        acumulador.adicionar_todos([1e16, 1.0, 1.0, -1e16])
        self.assertAlmostEqual(acumulador.total, 2.0)


def _registros(contagens: list[float], tag: str = "PT102") -> list[Registro]:
    """Cria leituras de uma tag na ordem das contagens fornecidas."""
    instante = datetime(2026, 10, 5, 8)
    return [Registro(instante, "INFO", tag, {"contagens": float(c)}) for c in contagens]


class TestContratoMedir(unittest.TestCase):
    """Cobre limites e índices que os testes de aceitação não verificam."""

    def setUp(self) -> None:
        """Prepara uma curva identidade para conferir as estatísticas diretamente."""
        self.curva = CurvaCalibracao([0, 2000, 4095], [0, 2000, 4095], "linear")

    def test_incerteza_sistematica_negativa(self) -> None:
        """Incerteza sistemática negativa é rejeitada com mensagem explicativa."""
        with self.assertRaisesRegex(ValueError, "incerteza|u_sistematica"):
            medir(_registros([9, 10, 11]), "PT102", self.curva, u_sistematica=-0.1)

    def test_mad_zero(self) -> None:
        """MAD zero é rejeitada mesmo quando existe uma leitura diferente."""
        with self.assertRaisesRegex(ValueError, "MAD"):
            medir(_registros([10, 10, 10, 11]), "PT102", self.curva)

    def test_poucas_validas_apos_descarte(self) -> None:
        """Rejeita zero ou uma leitura válida após aplicar o limiar robusto."""
        for contagens, limiar in (([1, 2], 0.0), ([1, 2, 3], 0.1)):
            with self.subTest(contagens=contagens):
                with self.assertRaisesRegex(ValueError, "válidas"):
                    medir(_registros(contagens), "PT102", self.curva, limiar=limiar)

    def test_propaga_erro_da_curva(self) -> None:
        """Contagem fora do domínio não é descartada como espúria nem ocultada."""
        with self.assertRaisesRegex(ValueError, "fora do domínio"):
            medir(_registros([9, 10, 11, 5000]), "PT102", self.curva)

    def test_indices_na_serie_da_tag(self) -> None:
        """Índices das espúrias ignoram outras tags e alarmes sem contagens."""
        leituras = _registros([500, 10, 11, 9, 10, 12, 11, 10, 9, 600])
        registros = []
        for leitura in leituras:
            registros.extend(_registros([3000], tag="PT101"))
            registros.append(Registro(leitura.instante, "ALARME", "PT102", {"evento": "alarme"}))
            registros.append(leitura)
        resultado = medir(registros, "PT102", self.curva)
        self.assertEqual(resultado.espurias, [0, 9])
        self.assertEqual(resultado.n_validas, 8)
        self.assertAlmostEqual(resultado.medida.valor, 10.25)

    def test_leitura_no_limiar_e_valida(self) -> None:
        """Uma leitura exatamente no limiar robusto é mantida."""
        valores = np.array([9.0, 10.0, 11.0])
        # Nos nós, a curva reproduz os valores sem arredondamento de interpolação.
        curva = CurvaCalibracao(valores, valores, "linear")
        limiar = 1.0 / stats.median_abs_deviation(valores, scale="normal")
        resultado = medir(_registros(valores.tolist()), "PT102", curva, limiar=limiar)
        self.assertEqual(resultado.espurias, [])
        self.assertEqual(resultado.n_validas, 3)
        self.assertAlmostEqual(resultado.medida.valor, 10.0)

    def test_incerteza_sistematica_nao_diminui(self) -> None:
        """Repetir amostras reduz o erro padrão, preservando a parcela sistemática."""
        valores = [9, 10, 11]
        pequena = medir(_registros(valores), "PT102", self.curva, u_sistematica=2.0)
        grande = medir(_registros(valores * 100), "PT102", self.curva, u_sistematica=2.0)
        self.assertAlmostEqual(pequena.medida.valor, grande.medida.valor)
        self.assertLess(grande.medida.incerteza, pequena.medida.incerteza)
        self.assertGreater(grande.medida.incerteza, 2.0)


if __name__ == "__main__":
    unittest.main()

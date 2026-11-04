"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

import numpy as np

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import ler_log
from elevatoria.medicao import altura_manometrica, medir


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


# Issue #7: regressão do AcumuladorKahan

def _somar(acumulador, parcelas) -> float:
    """Soma as parcelas com o acumulador dado e devolve o total."""
    for parcela in parcelas:
        acumulador.adicionar(parcela)
    return acumulador.total


class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Testes de regressão da issue #7 (escritos antes da correção)."""

    def test_um_milhao_de_decimos_de_litro(self):
        """Um milhão de parcelas de 0,1 deve dar 100000, com erro bem abaixo do ingênuo (1,3e-6)."""
        total = _somar(AcumuladorKahan(), [0.1] * 1_000_000)
        self.assertAlmostEqual(total, 100000.0, delta=1e-8)

    def test_kahan_bem_melhor_que_o_ingenuo(self):
        """O erro do Kahan deve ser pelo menos mil vezes menor que o do ingênuo."""
        parcelas = [0.1] * 1_000_000
        erro_ingenuo = abs(_somar(AcumuladorIngenuo(), parcelas) - 100000.0)
        erro_kahan = abs(_somar(AcumuladorKahan(), parcelas) - 100000.0)
        self.assertLessEqual(erro_kahan, erro_ingenuo / 1000)

    def test_parcelas_menores_que_o_arredondamento(self):
        """Parcelas de 1e-16 somadas a 1.0 se perdem no ingênuo, mas o Kahan as acumula."""
        parcelas = [1.0] + [1e-16] * 1_000_000
        self.assertAlmostEqual(_somar(AcumuladorKahan(), parcelas), 1.0 + 1e-10, delta=1e-12)
        self.assertEqual(_somar(AcumuladorIngenuo(), parcelas), 1.0)

    def test_valores_variados_contra_math_fsum(self):
        """Com valores sortidos, o Kahan fica mais perto da soma exata (math.fsum) que o ingênuo."""
        parcelas = np.random.default_rng(7).uniform(0.0, 1.0, 200_000).tolist()
        exato = math.fsum(parcelas)
        erro_ingenuo = abs(_somar(AcumuladorIngenuo(), parcelas) - exato)
        erro_kahan = abs(_somar(AcumuladorKahan(), parcelas) - exato)
        self.assertLess(erro_kahan, erro_ingenuo)


# Issue #6: auxiliares dos testes de medir

def _linha(i: int, tag: str, resto: str, nivel: str = "INFO") -> str:
    """Linha de log da i-ésima leitura (uma a cada 6 s)."""
    segundos = 6 * i
    return f"2026-10-05 08:{segundos // 60:02d}:{segundos % 60:02d} {nivel} {tag} {resto}"


def _registros(**series: list):
    """Registros de um log em que cada tag (argumento) tem a sua lista de contagens."""
    linhas = []
    for tag, contagens in series.items():
        linhas += [_linha(i, tag, f"contagens={c}") for i, c in enumerate(contagens)]
    registros, invalidas = ler_log("\n".join(linhas) + "\n")
    assert invalidas == []
    return registros


def _curva_identidade() -> CurvaCalibracao:
    """Curva em que contagens e kPa são iguais (domínio de 0 a 4000)."""
    pontos = [0, 1000, 2000, 3000, 4000]
    return CurvaCalibracao(pontos, pontos, "linear")


BASE = [100, 101, 99, 100, 102, 98, 100, 101, 99, 100]


class TestMedirContrato(unittest.TestCase):
    """Regras do contrato de `medir` que os testes de aceitação não verificam."""

    def test_u_sistematica_negativa(self):
        """Uma incerteza sistemática negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros(PT101=BASE), "PT101", _curva_identidade(), u_sistematica=-0.1)

    def test_tag_sem_leituras_ou_com_uma_so(self):
        """Uma tag ausente do log e uma tag com uma única leitura levantam ValueError."""
        registros = _registros(PT101=BASE, PT102=[100])
        for tag in ["FT201", "PT102"]:
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                medir(registros, tag, _curva_identidade())

    def test_mad_zero(self):
        """Leituras todas iguais têm MAD zero e levantam ValueError."""
        with self.assertRaises(ValueError):
            medir(_registros(PT101=[100] * 6), "PT101", _curva_identidade())

    def test_sobram_menos_de_duas_validas(self):
        """Com limiar 0 só a leitura da mediana sobra e isso levanta ValueError."""
        registros = _registros(PT101=[10, 20, 30, 40, 50])
        with self.assertRaises(ValueError):
            medir(registros, "PT101", _curva_identidade(), limiar=0.0)

    def test_contagem_fora_do_dominio_chega_a_quem_chamou(self):
        """O ValueError da curva (contagem acima de 4000) não é tratado por `medir`."""
        registros = _registros(PT101=BASE[:-1] + [5000])
        with self.assertRaises(ValueError):
            medir(registros, "PT101", _curva_identidade())

    def test_espuria_e_descartada_e_estatisticas_sem_ela(self):
        """A leitura espúria sai de média e desvio, e seu índice aparece em espurias."""
        valores = BASE.copy()
        valores[4] = 900
        m = medir(_registros(PT101=valores), "PT101", _curva_identidade())
        validas = np.array(valores[:4] + valores[5:], dtype=float)
        self.assertEqual(m.espurias, [4])
        self.assertEqual(m.n_validas, 9)
        self.assertAlmostEqual(m.medida.valor, validas.mean())
        self.assertAlmostEqual(m.desvio, validas.std(ddof=1))

    def test_indices_sao_posicoes_na_serie_da_tag(self):
        """Os índices das espúrias contam só as leituras da tag, não as linhas do log."""
        linhas = [_linha(0, "PT102", "contagens=100"),
                  _linha(1, "PT102", "evento=pressao_alta limite=2000", nivel="ALARME"),
                  _linha(1, "PT101", "contagens=50"),
                  _linha(2, "PT102", "contagens=101"),
                  _linha(3, "PT102", "contagens=99"),
                  _linha(4, "PT102", "contagens=1500"),
                  _linha(5, "PT102", "contagens=100"),
                  _linha(6, "PT102", "contagens=102")]
        registros, _ = ler_log("\n".join(linhas) + "\n")
        m = medir(registros, "PT102", _curva_identidade())
        self.assertEqual(m.espurias, [3])
        self.assertEqual(m.n_validas, 5)

    def test_incerteza_combina_erro_padrao_e_sistematica(self):
        """A incerteza é sqrt(erro_padrao² + u_sistematica²) e cresce com u_sistematica."""
        registros = _registros(PT101=BASE)
        curva = _curva_identidade()
        erro_padrao = np.std(BASE, ddof=1) / math.sqrt(len(BASE))
        sem_sist = medir(registros, "PT101", curva, u_sistematica=0.0)
        com_sist = medir(registros, "PT101", curva, u_sistematica=2.0)
        self.assertAlmostEqual(sem_sist.medida.incerteza, erro_padrao)
        self.assertAlmostEqual(com_sist.medida.incerteza, math.hypot(erro_padrao, 2.0))
        self.assertAlmostEqual(com_sist.medida.valor, sem_sist.medida.valor)

    def test_resultado_guarda_a_tag(self):
        """A Medicao devolvida traz a tag medida."""
        m = medir(_registros(PT101=BASE, PT102=BASE), "PT102", _curva_identidade())
        self.assertEqual(m.tag, "PT102")


class TestAlturaManometrica(unittest.TestCase):
    """altura_manometrica com uma curva de identidade e leituras conhecidas."""

    def setUp(self):
        self.registros = _registros(PT101=[99, 101] * 5, PT102=[399, 401] * 5)

    def test_valor_da_altura(self):
        """Com 100 kPa na sucção e 400 kPa no recalque, H = 300000 / (998 * 9,81) metros."""
        h = altura_manometrica(self.registros, _curva_identidade())
        self.assertAlmostEqual(h.valor, 300_000.0 / (998.0 * 9.81))

    def test_incerteza_cresce_com_a_sistematica(self):
        """Uma incerteza sistemática maior nos transmissores aumenta a incerteza de H."""
        curva = _curva_identidade()
        pequena = altura_manometrica(self.registros, curva, u_sistematica=0.1)
        grande = altura_manometrica(self.registros, curva, u_sistematica=3.0)
        self.assertGreater(grande.incerteza, pequena.incerteza)
        self.assertGreater(pequena.incerteza, 0.0)


if __name__ == "__main__":
    unittest.main()

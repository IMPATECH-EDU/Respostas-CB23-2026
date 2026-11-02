"""Medição de pressão a partir do log: calibração, estatística e incerteza (issues #6 e #7).

Este módulo junta peças que já existem na base:

- `serie` (de `elevatoria/dados.py`, o seu Marco 1): as contagens de uma tag no log;
- `CurvaCalibracao` (de `elevatoria/calibracao.py`, escrita por um colega): contagens -> kPa;
- `scipy.stats`: mediana, MAD e erro padrão;
- `Medida` (de `fornecido/medida.py`, da equipe de metrologia): valor ± incerteza.

As funções e classes implementam os contratos das issues #6 e #7.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import stats

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro, serie
from fornecido.medida import Medida

#: Massa específica da água (kg/m³), com a sua incerteza.
MASSA_ESPECIFICA = Medida(998.0, 1.0)

#: Aceleração da gravidade (m/s²), considerada exata.
GRAVIDADE = 9.81


@dataclass(frozen=True)
class Medicao:
    """Resultado da medição de uma grandeza a partir do log."""

    tag: str
    medida: Medida        # média das leituras válidas, com a incerteza total
    desvio: float         # desvio padrão amostral (ddof=1) das leituras válidas: a precisão
    n_validas: int        # número de leituras válidas (sem as espúrias)
    espurias: list[int]   # índices das leituras descartadas, em ordem crescente


def medir(registros: list[Registro], tag: str, curva: CurvaCalibracao,
          u_sistematica: float = 0.0, limiar: float = 6.0) -> Medicao:
    """Mede a grandeza registrada pela `tag` no log."""
    if u_sistematica < 0:
        raise ValueError("u_sistematica não pode ser negativa")

    s = serie(registros, tag, "contagens")
    if len(s) < 2:
        raise ValueError(f"a tag {tag} deve ter pelo menos 2 leituras")

    try:
        x = np.array([curva(float(c)) for c in s], dtype=float)
    except TypeError:
        x = np.array(curva(s), dtype=float)

    mediana = float(np.median(x))
    mad = float(stats.median_abs_deviation(x, scale="normal"))

    if mad == 0.0:
        raise ValueError("A MAD das leituras é zero")

    z = np.abs((x - mediana) / mad)
    espurias = [i for i, val in enumerate(z) if val > limiar]
    validas = np.array([val for i, val in enumerate(x) if i not in espurias], dtype=float)

    if len(validas) < 2:
        raise ValueError("Sobra menos de 2 leituras válidas após descarte de espúrias")

    media = float(np.mean(validas))
    desvio = float(np.std(validas, ddof=1))
    erro_padrao = float(stats.sem(validas))
    u_total = math.sqrt(erro_padrao ** 2 + u_sistematica ** 2)

    return Medicao(
        tag=tag,
        medida=Medida(media, u_total),
        desvio=desvio,
        n_validas=len(validas),
        espurias=espurias,
    )


def altura_manometrica(registros: list[Registro], curva: CurvaCalibracao,
                       u_sistematica: float = 1.5) -> Medida:
    """Altura manométrica da bomba, em metros, com a sua incerteza."""
    m_pt101 = medir(registros, "PT101", curva, u_sistematica=u_sistematica)
    m_pt102 = medir(registros, "PT102", curva, u_sistematica=u_sistematica)

    p_pt101 = m_pt101.medida
    p_pt102 = m_pt102.medida

    return (p_pt102 - p_pt101) * 1000.0 / (MASSA_ESPECIFICA * GRAVIDADE)


# ---------------------------------------------------------------------------------------
# Issue #7: acumuladores de precisão
# ---------------------------------------------------------------------------------------

class AcumuladorIngenuo:
    """Acumulador simples em ponto flutuante."""

    def __init__(self) -> None:
        self._total = 0.0

    def adicionar(self, val: float) -> None:
        self._total += float(val)

    def total(self) -> float:
        return self._total


class AcumuladorKahan:
    """Acumulador com algoritmo de Kahan para compensação de erro de arredondamento."""

    def __init__(self) -> None:
        self._total = 0.0
        self._c = 0.0

    def adicionar(self, val: float) -> None:
        y = float(val) - self._c
        t = self._total + y
        self._c = (t - self._total) - y
        self._total = t

    def total(self) -> float:
        return self._total


class AcumuladorInteiro:
    """Acumulador exato em números inteiros."""

    def __init__(self, fator: float = 1.0) -> None:
        self._fator = fator
        self._total_int = 0

    def adicionar(self, val: int | float) -> None:
        self._total_int += int(val)

    def total(self) -> float:
        return float(self._total_int * self._fator)
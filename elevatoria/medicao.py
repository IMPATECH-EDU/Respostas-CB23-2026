"""Medição de pressão a partir do log: calibração, estatística e incerteza (issue #6).

Este módulo junta peças que já existem na base:

- `serie` (de `elevatoria/dados.py`, o seu Marco 1): as contagens de uma tag no log;
- `CurvaCalibracao` (de `elevatoria/calibracao.py`, escrita por um colega): contagens -> kPa;
- `scipy.stats`: mediana, MAD e erro padrão;
- `Medida` (de `fornecido/medida.py`, da equipe de metrologia): valor ± incerteza.

As funções marcadas com `NotImplementedError` são a issue #6; as docstrings descrevem o
contrato. Não mude nomes nem assinaturas públicas: o `marco2.py` e os testes dependem deles.
Funções auxiliares privadas (`_nome`) são permitidas.
"""
from __future__ import annotations

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
    if u_sistematica < 0.0:
        raise ValueError("u_sistematica não pode ser negativa")

    contagens = serie(registros, tag, "contagens")
    if len(contagens) < 2:
        raise ValueError(f"a tag {tag} possui menos de 2 leituras")

    x_kpa = np.asarray(curva(contagens))
    mediana = float(np.median(x_kpa))
    mad = float(stats.median_abs_deviation(x_kpa, scale="normal"))

    if mad == 0.0:
        raise ValueError("MAD é zero")

    z = np.abs((x_kpa - mediana) / mad)
    espurias = [int(i) for i in np.where(z > limiar)[0]]
    validas = x_kpa[z <= limiar]

    if len(validas) < 2:
        raise ValueError("menos de 2 leituras válidas após remoção de espúrias")

    media = float(np.mean(validas))
    desvio = float(np.std(validas, ddof=1))
    erro_padrao = float(stats.sem(validas))

    u_total = float(np.sqrt(erro_padrao**2 + u_sistematica**2))
    medida = Medida(media, u_total)

    return Medicao(
        tag=tag,
        medida=medida,
        desvio=desvio,
        n_validas=len(validas),
        espurias=espurias,
    )


def altura_manometrica(registros: list[Registro], curva: CurvaCalibracao,
                       u_sistematica: float = 1.5) -> Medida:
    """Altura manométrica da bomba, em metros, com a sua incerteza."""
    m_succao = medir(registros, "PT101", curva, u_sistematica=u_sistematica)
    m_recalque = medir(registros, "PT102", curva, u_sistematica=u_sistematica)

    delta_p = m_recalque.medida - m_succao.medida
    return (delta_p * 1000) / (MASSA_ESPECIFICA * GRAVIDADE)
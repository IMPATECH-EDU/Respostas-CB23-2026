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
        raise ValueError("Incerteza sistemática não pode ser negativa")

    contagens = serie(registros, tag, "contagens")
    if len(contagens) < 2:
        raise ValueError("A tag precisa ter pelo menos 2 leituras")

    # 1 e 2. Converte as contagens para kPa
    pressao_kpa = np.array([curva(c) for c in contagens], dtype=float)

    # 3. Z robusto e filtro de espúrias
    mediana = float(np.median(pressao_kpa))
    mad = float(stats.median_abs_deviation(pressao_kpa, scale="normal"))

    if mad == 0:
        raise ValueError("MAD é zero")

    z_scores = np.abs(pressao_kpa - mediana) / mad
    
    validas_mask = z_scores <= limiar
    pressao_validas = pressao_kpa[validas_mask]
    
    if len(pressao_validas) < 2:
        raise ValueError("Sobra de leituras válidas é menor que 2")

    espurias = list(np.where(~validas_mask)[0])

    # 4. Estatísticas sobre leituras válidas
    media = float(np.mean(pressao_validas))
    desvio = float(np.std(pressao_validas, ddof=1))
    erro_padrao = float(stats.sem(pressao_validas))

    # 5. Incerteza total e retorno do objeto Medicao
    u_total = math.sqrt(erro_padrao**2 + u_sistematica**2)
    medida_obj = Medida(media, u_total)

    return Medicao(
        tag=tag,
        medida=medida_obj,
        desvio=desvio,
        n_validas=len(pressao_validas),
        espurias=espurias,
    )


def altura_manometrica(registros: list[Registro], curva: CurvaCalibracao,
                       u_sistematica: float = 1.5) -> Medida:
    """Altura manométrica da bomba, em metros, com a sua incerteza."""
    med_pt102 = medir(registros, "PT102", curva, u_sistematica=u_sistematica)
    med_pt101 = medir(registros, "PT101", curva, u_sistematica=u_sistematica)

    p_pt102 = med_pt102.medida
    p_pt101 = med_pt101.medida

    # H = (P_PT102 - P_PT101) * 1000 / (MASSA_ESPECIFICA * GRAVIDADE)
    delta_p = p_pt102 - p_pt101
    h = (delta_p * 1000) / (MASSA_ESPECIFICA * GRAVIDADE)

    return h
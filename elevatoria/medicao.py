"""Medição de pressão a partir do log: calibração, estatística e incerteza (issue #6).

Este módulo junta peças que já existem na base:

- `serie` (de `elevatoria/dados.py`, o seu Marco 1): as contagens de uma tag no log;
- `CurvaCalibracao` (de `elevatoria/calibracao.py`, escrita por um colega): contagens -> kPa;
- `scipy.stats`: mediana, MAD e erro padrão;
- `Medida` (de `fornecido/medida.py`, da equipe de metrologia): valor ± incerteza.

As duas funções implementam a medição de pressão e de altura da issue #6.
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
    """Mede a grandeza registrada pela `tag` no log.

    Passos:

    1. obtém as contagens da `tag` (chave `"contagens"`) com `serie`, do Marco 1;
    2. converte as contagens com a `curva`;
    3. descarta as leituras espúrias pelo z robusto: `z = (x - mediana) / MAD`, com a MAD
       calculada por `scipy.stats.median_abs_deviation(x, scale="normal")`; uma leitura é
       espúria se `|z| > limiar`. Os índices em `espurias` são posições na série da tag
       (a primeira leitura da tag tem índice 0);
    4. com as leituras válidas, calcula a média, o desvio padrão amostral (`ddof=1`) e o erro
       padrão da média (`scipy.stats.sem`);
    5. devolve uma `Medicao` cuja `medida` é `Medida(média, u)`, com
       `u = sqrt(erro_padrao² + u_sistematica²)`.

    `u_sistematica` é a incerteza do instrumento, que não diminui com o número de leituras.

    Levanta `ValueError` se `u_sistematica < 0`, se a tag tiver menos de 2 leituras, se a MAD
    for zero ou se sobrarem menos de 2 leituras válidas. Um `ValueError` da curva (contagem
    fora do domínio) não é tratado: ele chega a quem chamou `medir`.
    """
    if u_sistematica < 0:
        raise ValueError("a incerteza sistemática deve ser não negativa")
    contagens = serie(registros, tag, "contagens")
    if contagens.size < 2:
        raise ValueError(f"{tag} precisa de pelo menos duas leituras com contagens")
    pressoes = curva(contagens)
    mediana = np.median(pressoes)
    mad = stats.median_abs_deviation(pressoes, scale="normal")
    if mad == 0:
        raise ValueError(f"MAD zero em {tag}: o z robusto é indefinido")
    z = (pressoes - mediana) / mad
    descartar = np.abs(z) > limiar
    validas = pressoes[~descartar]
    if validas.size < 2:
        raise ValueError(f"{tag} ficou com menos de duas leituras válidas após a filtragem")
    incerteza = np.hypot(stats.sem(validas), u_sistematica)
    return Medicao(tag=tag, medida=Medida(float(validas.mean()), float(incerteza)),
                   desvio=float(validas.std(ddof=1)), n_validas=validas.size,
                   espurias=np.flatnonzero(descartar).tolist())


def altura_manometrica(registros: list[Registro], curva: CurvaCalibracao,
                       u_sistematica: float = 1.5) -> Medida:
    """Altura manométrica da bomba, em metros, com a sua incerteza.

    `H = (P_PT102 - P_PT101) * 1000 / (MASSA_ESPECIFICA * GRAVIDADE)`, em que `P_PT101` e
    `P_PT102` são as `medida`s de `medir` para as duas tags, em kPa (o fator 1000 converte
    para Pa), ambas com a incerteza sistemática `u_sistematica`. Todas as contas são feitas
    com `Medida`, que propaga as incertezas.
    """
    succao = medir(registros, "PT101", curva, u_sistematica).medida
    recalque = medir(registros, "PT102", curva, u_sistematica).medida
    return (recalque - succao) * 1000 / (MASSA_ESPECIFICA * GRAVIDADE)

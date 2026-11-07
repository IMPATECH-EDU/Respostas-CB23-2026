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
        raise ValueError(f"u_sistematica não pode ser negativa; recebi {u_sistematica}")
    contagens = serie(registros, tag, "contagens")
    if len(contagens) < 2:
        raise ValueError(f"a tag {tag} precisa de pelo menos 2 leituras; tem {len(contagens)}")

    pressoes = np.asarray(curva(np.asarray(contagens)))    # ValueError da curva sobe direto
    validas, espurias = _separar_espurias(pressoes, limiar)
    if validas.size < 2:
        raise ValueError(f"sobraram {validas.size} leituras válidas de {tag}; são precisas 2")

    erro_padrao = float(stats.sem(validas))
    incerteza = float(np.hypot(erro_padrao, u_sistematica))
    return Medicao(tag=tag,
                   medida=Medida(float(np.mean(validas)), incerteza),
                   desvio=float(np.std(validas, ddof=1)),
                   n_validas=int(validas.size),
                   espurias=espurias)


def _separar_espurias(x: np.ndarray, limiar: float) -> tuple[np.ndarray, list[int]]:
    """`(leituras válidas, índices das espúrias)` pelo z robusto `(x - mediana) / MAD`.

    Levanta `ValueError` se a MAD for zero (o z robusto fica indefinido).
    """
    mad = float(stats.median_abs_deviation(x, scale="normal"))
    if mad == 0.0:
        raise ValueError("a MAD das leituras é zero: não dá para calcular o z robusto")
    z = (x - np.median(x)) / mad
    fora = np.abs(z) > limiar
    return x[~fora], np.flatnonzero(fora).tolist()


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
    pa_por_kpa = 1000.0
    return (recalque - succao) * pa_por_kpa / (MASSA_ESPECIFICA * GRAVIDADE)

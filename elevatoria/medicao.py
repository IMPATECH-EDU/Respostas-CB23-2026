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
    """Resultado estatístico e metrológico de uma medição do log.

    Attributes:
        tag: Identificador do instrumento medido.
        medida: Média das leituras válidas e incerteza total associada.
        desvio: Desvio padrão amostral das leituras válidas, como medida de precisão.
        n_validas: Número de leituras usadas no cálculo.
        espurias: Índices das leituras descartadas, na série extraída da tag.
    """

    tag: str
    medida: Medida        # média das leituras válidas, com a incerteza total
    desvio: float         # desvio padrão amostral (ddof=1) das leituras válidas: a precisão
    n_validas: int        # número de leituras válidas (sem as espúrias)
    espurias: list[int]   # índices das leituras descartadas, em ordem crescente


def medir(registros: list[Registro], tag: str, curva: CurvaCalibracao,
          u_sistematica: float = 0.0, limiar: float = 6.0) -> Medicao:
    """Estima a pressão média de uma tag e sua incerteza combinada.

    Args:
        registros: Registros estruturados do log.
        tag: Tag de pressão a medir; seus registros devem conter `"contagens"`.
        curva: Curva que converte contagens em kPa.
        u_sistematica: Incerteza sistemática não negativa, em kPa.
        limiar: Limite estrito do valor absoluto do z-score robusto para rejeitar leituras.

    Returns:
        `Medicao` com média em `Medida`, desvio padrão amostral, número de leituras válidas
        e índices das leituras descartadas. A incerteza da medida combina erro padrão e
        incerteza sistemática pela raiz da soma dos quadrados.

    Raises:
        ValueError: Se `u_sistematica` for negativa, houver menos de duas leituras da tag,
            a MAD for zero ou restarem menos de duas leituras válidas.
        ValueError: Propaga também o erro da curva se uma contagem estiver fora do domínio
            calibrado.
    """
    if u_sistematica < 0:
        raise ValueError(f"u_sistematica deve ser não negativa; recebi {u_sistematica!r}")

    contagens = serie(registros, tag, "contagens")
    if len(contagens) < 2:
        raise ValueError(f"menos de 2 leituras para a tag {tag!r}")

    x = curva(contagens)

    mediana = np.median(x)
    mad = stats.median_abs_deviation(x, scale="normal")

    if mad == 0.0:
        raise ValueError(f"MAD = 0 para a tag {tag!r}")

    z = (x - mediana) / mad
    espurias_mask = np.abs(z) > limiar
    espurias = np.where(espurias_mask)[0].tolist()

    x_validas = x[~espurias_mask]

    if len(x_validas) < 2:
        raise ValueError(f"menos de 2 leituras válidas para a tag {tag!r}")

    media = np.mean(x_validas)
    desvio = np.std(x_validas, ddof=1)
    erro_padrao = stats.sem(x_validas, ddof=1)
    u = np.sqrt(erro_padrao**2 + u_sistematica**2)

    return Medicao(tag, Medida(media, u), desvio, len(x_validas), espurias)


def altura_manometrica(registros: list[Registro], curva: CurvaCalibracao,
                       u_sistematica: float = 1.5) -> Medida:
    """Calcula a altura manométrica da bomba e propaga sua incerteza.

    Args:
        registros: Registros estruturados do log, com leituras para `PT101` e `PT102`.
        curva: Curva que converte contagens em kPa.
        u_sistematica: Incerteza sistemática usada para cada transmissor, em kPa.

    Returns:
        `Medida` da altura em metros, calculada como
        `(P_PT102 - P_PT101) * 1000 / (MASSA_ESPECIFICA * GRAVIDADE)`.

    Raises:
        ValueError: Propaga erros de validação ou de calibração levantados por `medir`.
    """
    medicao_PT101 = medir(registros, "PT101", curva, u_sistematica)
    medicao_PT102 = medir(registros, "PT102", curva, u_sistematica)

    pt101 = medicao_PT101.medida
    pt102 = medicao_PT102.medida

    return (pt102 - pt101) * 1000 / (MASSA_ESPECIFICA * GRAVIDADE)
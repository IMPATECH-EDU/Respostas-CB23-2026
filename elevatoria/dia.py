"""Curvas da bomba por mínimos quadrados e o balanço do dia de operação (issue #10).

Este módulo junta peças que já existem na base:

- o registro de vazão do dia, a potência e as faixas tarifárias (de `fornecido/energia.py`,
  da equipe de energia);
- as regras de integração `Trapezio` e `Simpson` (de `elevatoria/integracao.py`, escritas por
  um colega);
- o NumPy ou o SciPy, para o ajuste de curvas (há mais de um caminho: veja `ajustar_polinomio`).

As funções marcadas com `NotImplementedError` são a issue #10; as docstrings descrevem o
contrato. Não mude nomes nem assinaturas públicas: o `marco4.py` e os testes dependem deles.
Funções auxiliares privadas (`_nome`) são permitidas.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from elevatoria.integracao import Integrador
from fornecido.energia import FAIXAS_TARIFARIAS, potencia_eletrica


def ajustar_polinomio(x: np.ndarray, y: np.ndarray, grau: int) -> np.ndarray:
    """Coeficientes `[c0, c1, ..., c_grau]` do polinômio de mínimos quadrados de grau `grau`.

    O polinômio `p(x) = c0 + c1·x + ... + c_grau·x^grau` minimiza `Σ (y_i - p(x_i))²`. Os
    coeficientes estão em ordem **crescente**: avalie o polinômio com
    `np.polynomial.polynomial.polyval(x, coeficientes)`.

    O NumPy e o SciPy oferecem mais de um método para resolver esse problema, e a escolha é
    sua. Alguns pontos de partida, para ler na documentação:

    - `np.polynomial.polynomial.polyfit`;
    - `np.polyfit` (atenção: devolve os coeficientes em ordem **decrescente**);
    - `np.linalg.lstsq` ou `scipy.linalg.lstsq`, aplicados à matriz
      `np.vander(x, grau + 1, increasing=True)`;
    - a fatoração QR dessa mesma matriz, com `np.linalg.qr` e `scipy.linalg.solve_triangular`.

    Método escolhido: `np.polynomial.polynomial.polyfit`. Ele já devolve os coeficientes em
    ordem crescente e resolve o problema por SVD (`lstsq`) sobre a matriz de Vandermonde, sem
    formar as equações normais `AᵀA c = Aᵀy`, cujo condicionamento é o quadrado do de `A`.

    Args:
        x: abscissas do ensaio (vetor 1D), por exemplo a vazão em L/s.
        y: valores medidos (vetor 1D do mesmo tamanho de `x`), por exemplo altura (m).
        grau: grau do polinômio (inteiro ≥ 0).

    Returns:
        `ndarray` de tamanho `grau + 1` com `[c0, c1, ..., c_grau]`.

    Raises:
        ValueError: se `x` e `y` não forem vetores 1D do mesmo tamanho, se `grau < 0` ou se
            `len(x) < grau + 1`.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("x e y devem ser vetores 1D do mesmo tamanho")
    if grau < 0:
        raise ValueError(f"o grau deve ser não negativo; recebi {grau}")
    if x.size < grau + 1:
        raise ValueError(f"são necessários ao menos {grau + 1} pontos para o grau {grau}; recebi {x.size}")
    # polyfit do módulo polynomial já devolve a ordem crescente e resolve o problema por
    # mínimos quadrados (SVD) sobre a matriz de Vandermonde, sem formar as equações normais.
    return np.asarray(np.polynomial.polynomial.polyfit(x, y, grau), dtype=float)


@dataclass(frozen=True)
class ResumoDia:
    """Balanço do dia de operação."""

    volume_m3: float                    # volume bombeado (m³)
    energia_kwh: float                  # energia consumida (kWh)
    custo_reais: float                  # custo da energia (R$): a soma de custo_por_faixa
    custo_por_faixa: tuple[float, ...]  # custo de cada faixa, na ordem de FAIXAS_TARIFARIAS


def dia_de_operacao(t: np.ndarray, vazao: np.ndarray, coef_altura: np.ndarray,
                    coef_rendimento: np.ndarray, integrador: Integrador) -> ResumoDia:
    """Volume, energia e custo de um dia de operação a partir do registro de vazão.

    `t` (h) e `vazao` (L/s) são o registro do dia; `coef_altura` e `coef_rendimento` são os
    coeficientes (em ordem crescente, como os de `ajustar_polinomio`) das curvas da bomba,
    altura (m) e rendimento em função da vazão. Passos:

    1. em cada instante, a altura e o rendimento da bomba, com
       `np.polynomial.polynomial.polyval(vazao, coeficientes)`, e a potência (kW), com
       `potencia_eletrica` (de `fornecido/energia.py`);
    2. o volume (m³): `3,6 · ∫ vazão dt` (L/s × h = 3,6 m³);
    3. a energia (kWh): `∫ potência dt`;
    4. o custo de cada faixa `(início, fim, tarifa)` de `FAIXAS_TARIFARIAS`: `tarifa · ∫ potência
       dt`, com a integral feita só com os instantes `início ≤ t ≤ fim`. O custo total é a
       soma das faixas.

    Todas as integrais usam `integrador.integrar_tabela(x, y)`.

    Como o registro tem leituras perdidas, `t` pode ser uma malha **não uniforme**; por isso o
    `integrador` precisa aceitar espaçamentos diferentes (o `Simpson` recusa essa tabela). Os
    limites de faixa pertencem às duas faixas vizinhas (18 h e 21 h), e cada integral de faixa
    usa só os instantes dentro dela, sem interpolar: por isso os limites devem estar em `t`.

    Args:
        t: instantes das leituras (h), estritamente crescentes, de 0 a 24.
        vazao: vazão registrada (L/s) em cada instante, do mesmo tamanho de `t`.
        coef_altura: coeficientes (ordem crescente) da altura da bomba (m) em função de Q.
        coef_rendimento: coeficientes (ordem crescente) do rendimento em função de Q.
        integrador: regra com `integrar_tabela(x, y)`, por exemplo `Trapezio()`.

    Returns:
        `ResumoDia` com volume (m³), energia (kWh), custo total (R$) e custo por faixa (R$).

    Raises:
        ValueError: se `t` e `vazao` não forem vetores 1D do mesmo tamanho, se algum limite de
            faixa (0, 18, 21 e 24 h) não estiver entre os instantes de `t`, ou se o rendimento
            ajustado não for positivo em algum instante (erro de `potencia_eletrica`).
    """
    t = np.asarray(t, dtype=float)
    vazao = np.asarray(vazao, dtype=float)
    if t.ndim != 1 or t.shape != vazao.shape:
        raise ValueError("t e vazao devem ser vetores 1D do mesmo tamanho")
    limites = {inicio for inicio, _, _ in FAIXAS_TARIFARIAS} | {FAIXAS_TARIFARIAS[-1][1]}
    for limite in sorted(limites):
        if not np.any(np.isclose(t, limite, rtol=0.0, atol=1e-9)):
            raise ValueError(f"o limite de faixa {limite:g} h não está entre os instantes de t")

    polyval = np.polynomial.polynomial.polyval
    altura = polyval(vazao, coef_altura)
    rendimento = polyval(vazao, coef_rendimento)
    potencia = potencia_eletrica(vazao, altura, rendimento)

    volume = 3.6 * integrador.integrar_tabela(t, vazao)
    energia = integrador.integrar_tabela(t, potencia)

    custos = []
    for inicio, fim, preco in FAIXAS_TARIFARIAS:
        na_faixa = (t >= inicio - 1e-9) & (t <= fim + 1e-9)
        custos.append(float(preco * integrador.integrar_tabela(t[na_faixa], potencia[na_faixa])))
    return ResumoDia(float(volume), float(energia), float(sum(custos)), tuple(custos))
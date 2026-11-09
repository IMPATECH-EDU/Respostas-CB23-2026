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

    Levanta `ValueError` se `x` e `y` não forem vetores 1D do mesmo tamanho, se `grau < 0` ou se
    houver menos pontos que coeficientes (`len(x) < grau + 1`).
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if x_arr.ndim != 1 or y_arr.ndim != 1 or x_arr.size != y_arr.size:
        raise ValueError("x e y devem ser vetores 1D do mesmo tamanho")
    if grau < 0:
        raise ValueError(f"grau deve ser não negativo; recebi {grau}")
    if x_arr.size < grau + 1:
        raise ValueError(f"número de pontos ({x_arr.size}) menor que número de coeficientes ({grau + 1})")

    coefs = np.polynomial.polynomial.polyfit(x_arr, y_arr, grau)
    return np.asarray(coefs, dtype=float)


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

    Levanta `ValueError` se `t` e `vazao` tiverem tamanhos diferentes ou se algum limite de
    faixa (0, 18, 21 e 24 h) não estiver entre os instantes de `t`.
    """
    t_arr = np.asarray(t, dtype=float)
    q_arr = np.asarray(vazao, dtype=float)
    if t_arr.ndim != 1 or q_arr.ndim != 1 or t_arr.size != q_arr.size:
        raise ValueError("t e vazao devem ser vetores 1D do mesmo tamanho")

    for limite in (0.0, 18.0, 21.0, 24.0):
        if not np.any(np.isclose(t_arr, limite, atol=1e-8)):
            raise ValueError(f"limite de faixa {limite} não encontrado em t")

    altura = np.polynomial.polynomial.polyval(q_arr, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(q_arr, coef_rendimento)
    potencia = potencia_eletrica(q_arr, altura, rendimento)

    volume_m3 = 3.6 * integrador.integrar_tabela(t_arr, q_arr)
    energia_kwh = integrador.integrar_tabela(t_arr, potencia)

    custos = []
    for inicio, fim, tarifa in FAIXAS_TARIFARIAS:
        mask = (t_arr >= inicio - 1e-9) & (t_arr <= fim + 1e-9)
        t_faixa = t_arr[mask]
        pot_faixa = potencia[mask]
        custo_faixa = tarifa * integrador.integrar_tabela(t_faixa, pot_faixa)
        custos.append(float(custo_faixa))

    custo_total = float(sum(custos))
    return ResumoDia(
        volume_m3=float(volume_m3),
        energia_kwh=float(energia_kwh),
        custo_reais=custo_total,
        custo_por_faixa=tuple(custos)
    )

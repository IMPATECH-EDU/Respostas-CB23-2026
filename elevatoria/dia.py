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
from scipy.linalg import solve_triangular

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
    xs = np.asarray(x, dtype=float)
    ys = np.asarray(y, dtype=float)
    if xs.ndim != 1 or ys.ndim != 1 or xs.size != ys.size:
        raise ValueError("x e y devem ser vetores 1D do mesmo tamanho")
    if grau < 0:
        raise ValueError(f"o grau não pode ser negativo; recebi {grau}")
    if xs.size < grau + 1:
        raise ValueError(f"grau {grau} pede pelo menos {grau + 1} pontos; recebi {xs.size}")

    # Mínimos quadrados por QR: com A = QR, min ||A·c - y|| vira o sistema triangular R·c = Qᵀ·y.
    # Não forma AᵀA (equações normais), que elevaria ao quadrado o condicionamento de A.
    vandermonde = np.vander(xs, grau + 1, increasing=True)     # colunas 1, x, x², ...
    q, r = np.linalg.qr(vandermonde)                            # forma reduzida: R é (grau+1)²
    diagonal = np.abs(np.diag(r))
    if np.any(diagonal <= 1e-12 * diagonal.max()):
        raise ValueError(f"os valores de x não têm pontos distintos suficientes para o grau {grau}")
    return solve_triangular(r, q.T @ ys, lower=False)


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
    horas = np.asarray(t, dtype=float)
    q = np.asarray(vazao, dtype=float)
    if horas.shape != q.shape:
        raise ValueError(f"t e vazao precisam ter o mesmo tamanho; recebi {horas.size} e {q.size}")
    limites = sorted({inicio for inicio, _, _ in FAIXAS_TARIFARIAS}
                     | {fim for _, fim, _ in FAIXAS_TARIFARIAS})
    faltando = [h for h in limites if not np.any(np.isclose(horas, h, rtol=0.0, atol=1e-9))]
    if faltando:
        raise ValueError(f"os limites de faixa {faltando} h não estão entre os instantes de t")

    # 1. altura, rendimento e potência elétrica em cada leitura
    altura = np.polynomial.polynomial.polyval(q, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(q, coef_rendimento)
    potencia = potencia_eletrica(q, altura, rendimento)

    # 2. e 3. volume (L/s·h -> m³) e energia (kW·h) no dia inteiro
    volume = 3.6 * integrador.integrar_tabela(horas, q)
    energia = integrador.integrar_tabela(horas, potencia)

    # 4. custo faixa a faixa: a tarifa é constante dentro de cada uma, então a integral não
    #    atravessa a descontinuidade (os pontos de fronteira entram nas duas faixas vizinhas)
    custos = []
    for inicio, fim, tarifa in FAIXAS_TARIFARIAS:
        dentro = (horas >= inicio - 1e-9) & (horas <= fim + 1e-9)
        custos.append(tarifa * integrador.integrar_tabela(horas[dentro], potencia[dentro]))

    return ResumoDia(volume_m3=float(volume), energia_kwh=float(energia),
                     custo_reais=float(sum(custos)), custo_por_faixa=tuple(float(c) for c in custos))

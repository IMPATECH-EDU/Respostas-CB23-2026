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
from numpy.polynomial import polynomial as P
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
    houver menos pontos que coeficientes (`len(x) < grau + 1`). Também levanta `ValueError` se
    `grau` não for inteiro ou se houver menos valores **distintos** de `x` que coeficientes: com
    abscissas repetidas o polinômio não fica determinado.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError(f"x e y devem ser vetores 1D do mesmo tamanho; recebi {x.shape} e {y.shape}")
    if isinstance(grau, bool) or not isinstance(grau, (int, np.integer)):
        raise ValueError(f"o grau deve ser um inteiro; recebi {grau!r}")
    if grau < 0:
        raise ValueError(f"o grau não pode ser negativo; recebi {grau}")
    n_coef = grau + 1
    if x.size < n_coef:
        raise ValueError(f"grau {grau} tem {n_coef} coeficientes, mas só há {x.size} pontos")
    if np.unique(x).size < n_coef:
        raise ValueError(f"grau {grau} pede {n_coef} valores distintos de x; "
                         f"há só {np.unique(x).size}")

    # Mínimos quadrados pela fatoração QR, sem montar as equações normais VᵀV c = Vᵀy: elas
    # elevariam ao quadrado o número de condição da matriz de Vandermonde V.
    V = np.vander(x, n_coef, increasing=True)
    # As colunas 1, x, x², ... têm tamanhos muito diferentes (no ensaio, x vai a 100 e x² a
    # 10 000). Dividir cada coluna pela sua norma equilibra a matriz; no fim, desfaz-se a escala.
    escala = np.linalg.norm(V, axis=0)
    Q, R = np.linalg.qr(V / escala)             # V/escala = Q·R, Q ortonormal, R triangular
    return solve_triangular(R, Q.T @ y) / escala


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
    faixa (0, 18, 21 e 24 h) não estiver entre os instantes de `t`. Um `ValueError` do
    integrador (por exemplo, `Simpson` com leituras faltando) não é tratado: ele chega a quem
    chamou `dia_de_operacao`.
    """
    t = np.asarray(t, dtype=float)
    vazao = np.asarray(vazao, dtype=float)
    if t.ndim != 1 or t.shape != vazao.shape:
        raise ValueError(f"t e vazao devem ser vetores 1D do mesmo tamanho; recebi {t.shape} e {vazao.shape}")
    limites = sorted({a for a, _, _ in FAIXAS_TARIFARIAS} | {b for _, b, _ in FAIXAS_TARIFARIAS})
    faltando = [limite for limite in limites if not np.any(t == limite)]
    if faltando:
        raise ValueError(f"o registro não tem leitura nos limites das faixas {faltando} h")

    altura = P.polyval(vazao, coef_altura)
    rendimento = P.polyval(vazao, coef_rendimento)
    potencia = potencia_eletrica(vazao, altura, rendimento)          # kW em cada instante

    volume = 3.6 * integrador.integrar_tabela(t, vazao)            # (L/s)·h = 3,6 m³
    energia = integrador.integrar_tabela(t, potencia)
    custos = tuple(tarifa * _integral_na_faixa(integrador, t, potencia, inicio, fim)
                   for inicio, fim, tarifa in FAIXAS_TARIFARIAS)
    return ResumoDia(volume_m3=float(volume), energia_kwh=float(energia),
                     custo_reais=float(sum(custos)), custo_por_faixa=custos)


def _integral_na_faixa(integrador: Integrador, t: np.ndarray, y: np.ndarray,
                       inicio: float, fim: float) -> float:
    """Integral de `y` só com os instantes `inicio <= t <= fim` (os dois limites entram).

    A tarifa salta às 18 h e às 21 h. Dentro de uma faixa ela é constante e sai da integral;
    uma integral que atravessasse o salto perderia a ordem da regra (Etapa 1(b) do marco4.py).
    """
    dentro = (t >= inicio) & (t <= fim)
    return float(integrador.integrar_tabela(t[dentro], y[dentro]))

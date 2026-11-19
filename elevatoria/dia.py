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
    houver NaN ou infinito nos dados, ou menos de `grau + 1` valores distintos em `x` (aí o
    polinômio de mínimos quadrados não é único).

    Método: QR da Vandermonde em `t = (x - centro) / raio`, que leva os `x` para `[-1, 1]`, e
    depois a troca de base de volta para `1, x, x², ...`.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError(f"x e y devem ser vetores 1D do mesmo tamanho; recebi {x.shape} e {y.shape}")
    if grau < 0:
        raise ValueError(f"o grau não pode ser negativo; recebi {grau}")
    if x.size < grau + 1:
        raise ValueError(f"grau {grau} pede pelo menos {grau + 1} pontos; recebi {x.size}")
    if not (np.isfinite(x).all() and np.isfinite(y).all()):
        raise ValueError("x e y não podem ter NaN nem infinito")
    distintos = np.unique(x).size
    if distintos < grau + 1:
        raise ValueError(f"só {distintos} valores distintos de x: o grau {grau} fica indeterminado")
    # Na base 1, x, x², ... com x de 0 a 100, as colunas vão de 1 a 100**grau e ficam quase
    # paralelas. Em t, todas ficam em [-1, 1] e o QR resolve sem perder dígitos à toa.
    centro = (x.max() + x.min()) / 2
    raio = (x.max() - x.min()) / 2
    if raio == 0:   # todos os x iguais, o que só passa com grau 0
        raio = 1.0
    q, r = np.linalg.qr(np.vander((x - centro) / raio, grau + 1, increasing=True))
    coef_t = solve_triangular(r, q.T @ y)
    return _base_de_x(coef_t, centro, raio)


def _base_de_x(coef_t: np.ndarray, centro: float, raio: float) -> np.ndarray:
    """Coeficientes em x de `sum(coef_t[k] * t**k)`, com `t = (x - centro) / raio`.

    Horner com polinômios: começa pelo coeficiente mais alto e, a cada passo, multiplica o
    acumulado por `t` (em x, `-centro/raio + x/raio`) e soma o coeficiente seguinte.
    """
    alfa, beta = -centro / raio, 1.0 / raio
    coef = np.zeros_like(coef_t)
    for c in coef_t[::-1]:
        coef = alfa * coef + beta * np.concatenate(([0.0], coef[:-1]))
        coef[0] += c
    return coef


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
    t = np.asarray(t, dtype=float)
    vazao = np.asarray(vazao, dtype=float)
    if t.shape != vazao.shape:
        raise ValueError(f"t e vazao têm tamanhos diferentes: {t.size} e {vazao.size}")
    limites = {limite for faixa in FAIXAS_TARIFARIAS for limite in faixa[:2]}
    faltando = sorted(limites - set(t.tolist()))
    if faltando:
        raise ValueError(f"o registro não tem leitura nos limites de faixa {faltando} (h)")
    potencia = potencia_eletrica(vazao, P.polyval(vazao, coef_altura),
                                 P.polyval(vazao, coef_rendimento))
    custos = []
    for inicio, fim, tarifa in FAIXAS_TARIFARIAS:
        na_faixa = (t >= inicio) & (t <= fim)
        custos.append(tarifa * integrador.integrar_tabela(t[na_faixa], potencia[na_faixa]))
    return ResumoDia(volume_m3=3.6 * integrador.integrar_tabela(t, vazao),
                     energia_kwh=integrador.integrar_tabela(t, potencia),
                     custo_reais=sum(custos),
                     custo_por_faixa=tuple(custos))

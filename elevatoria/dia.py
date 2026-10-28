"""Ajuste das curvas da bomba e balanço do dia de operação."""
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
    houver menos pontos que coeficientes (`len(x) < grau + 1`). Também rejeita
    valores não finitos e graus não inteiros com `ValueError`.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("x e y devem ser vetores 1D do mesmo tamanho")
    if isinstance(grau, bool) or not isinstance(grau, (int, np.integer)) or grau < 0:
        raise ValueError("grau deve ser um inteiro não negativo")
    if x.size < grau + 1:
        raise ValueError("o número de pontos deve ser pelo menos grau + 1")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("x e y devem conter somente valores finitos")
    return np.polynomial.polynomial.polyfit(x, y, grau)


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
    faixa (0, 18, 21 e 24 h) não estiver entre os instantes de `t`. As entradas
    devem ser vetores 1D finitos; violações também levantam `ValueError`.
    Erros da potência e do integrador são propagados para quem chamou.
    """
    t, vazao = np.asarray(t, dtype=float), np.asarray(vazao, dtype=float)
    if t.ndim != 1 or vazao.ndim != 1 or t.size != vazao.size:
        raise ValueError("t e vazao devem ser vetores 1D do mesmo tamanho")
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(vazao)):
        raise ValueError("t e vazao devem conter somente valores finitos")
    limites = {limite for inicio, fim, _ in FAIXAS_TARIFARIAS for limite in (inicio, fim)}
    for limite in limites:
        if not np.any(t == limite):
            raise ValueError(f"falta a leitura no limite tarifário de {limite:g} h")
    altura = np.polynomial.polynomial.polyval(vazao, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(vazao, coef_rendimento)
    potencia = potencia_eletrica(vazao, altura, rendimento)
    volume = 3.6 * integrador.integrar_tabela(t, vazao)
    energia = integrador.integrar_tabela(t, potencia)
    custos = []
    for inicio, fim, tarifa in FAIXAS_TARIFARIAS:
        faixa = (t >= inicio) & (t <= fim)
        custos.append(tarifa * integrador.integrar_tabela(t[faixa], potencia[faixa]))
    return ResumoDia(volume, energia, sum(custos), tuple(custos))

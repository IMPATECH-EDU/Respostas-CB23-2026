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

    Levanta `ValueError` se `x` e `y` não forem vetores 1D do mesmo tamanho, se `grau < 0` ou se
    houver menos pontos que coeficientes (`len(x) < grau + 1`).
    """
    x = np.asarray(x)
    y = np.asarray(y)

    if len(x) != len(y):
        raise ValueError('É necessário ter a mesma quantidade de valores em x e em y')
    if x.ndim != 1 or y.ndim != 1:
        raise ValueError('É necesário que x e y tenham dimensão 1D')
    if grau<0:
        raise ValueError('O grau precisa ser não negativo')
    if len(x) < grau + 1:
        raise ValueError('Não pode ter menos pontos do que coeficientes')

    coeficientes = np.polynomial.polynomial.polyfit(x,y,grau)
    return coeficientes
    


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

    if len(t) != len(vazao):
        raise ValueError('as listas com valores de tempo e de vazão')

    
    altura = np.polynomial.polynomial.polyval(vazao, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(vazao, coef_rendimento)
    potencia = potencia_eletrica(vazao, altura, rendimento)

    volume = 3.6*integrador.integrar_tabela(t, vazao)
    energia = integrador.integrar_tabela(t, potencia)

    custos = []

    if (0.0 not in t or 18.0 not in t or 21.0 not in t or 24.0 not in t):
        raise ValueError('É necessário que os limites de intervalos estejam no intervalo de tempos')

    for i in range(3):
      inicio = FAIXAS_TARIFARIAS[i][0]
      fim = FAIXAS_TARIFARIAS[i][1]
      mascara = (t >= inicio) & (t <= fim)
      t_faixa = t[mascara]
   
      potencia_faixa = potencia[mascara]
      tarifa = FAIXAS_TARIFARIAS[i][2]

      custo = tarifa*integrador.integrar_tabela(t_faixa, potencia_faixa)
      custos.append(custo)
    custo_em_reais = custos[0] + custos[1] + custos[2]

    return ResumoDia(volume, energia, custo_em_reais, tuple(custos))

    
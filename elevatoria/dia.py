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
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)

    if x_arr.ndim != 1 or y_arr.ndim != 1:
        raise ValueError("Os vetores x e y devem ser unidimensionais (1D).")

    if x_arr.size != y_arr.size:
        raise ValueError(f"x e y devem ter o mesmo tamanho. Recebido: {x_arr.size} e {y_arr.size}.")

    if grau < 0:
        raise ValueError(f"O grau do polinômio deve ser não negativo. Recebido: {grau}.")

    if x_arr.size < grau + 1:
        raise ValueError(
            f"Número de pontos ({x_arr.size}) é menor do que o necessário ({grau + 1}) para grau {grau}."
        )

    # Devolve coeficientes em ordem crescente [c0, c1, ..., c_grau]
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

    if t_arr.size != q_arr.size:
        raise ValueError(f"t e vazao devem ter o mesmo tamanho. Recebido {t_arr.size} e {q_arr.size}.")

    # Validação da presença dos limites das faixas tarifárias no vetor t
    limites_obrigatorios = {0.0, 18.0, 21.0, 24.0}
    for faixa in FAIXAS_TARIFARIAS:
        limites_obrigatorios.add(float(faixa.inicio))
        limites_obrigatorios.add(float(faixa.fim))

    for lim in limites_obrigatorios:
        if not np.any(np.isclose(t_arr, lim)):
            raise ValueError(f"O limite de faixa {lim}h não está presente nos instantes de t.")

    # 1. Altura, rendimento e potência
    altura = np.polynomial.polynomial.polyval(q_arr, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(q_arr, coef_rendimento)
    potencia = np.vectorize(potencia_eletrica)(q_arr, altura, rendimento)

    # 2. Volume acumulado (m³) = 3.6 * ∫ Q dt (com Q em L/s e t em h)
    int_q = integrador.integrar_tabela(t_arr, q_arr)
    volume_m3 = float(3.6 * int_q)

    # 3. Energia total acumulada (kWh) = ∫ P dt (com P em kW e t em h)
    energia_kwh = float(integrador.integrar_tabela(t_arr, potencia))

    # 4. Custos por faixa tarifária
    custos_faixas = []
    for faixa in FAIXAS_TARIFARIAS:
        mascara = (t_arr >= faixa.inicio) & (t_arr <= faixa.fim)
        t_faixa = t_arr[mascara]
        pot_faixa = potencia[mascara]

        int_pot_faixa = integrador.integrar_tabela(t_faixa, pot_faixa)
        custo_faixa = float(faixa.tarifa * int_pot_faixa)
        custos_faixas.append(custo_faixa)

    custo_total = float(sum(custos_faixas))

    return ResumoDia(
        volume_m3=volume_m3,
        energia_kwh=energia_kwh,
        custo_reais=custo_total,
        custo_por_faixa=tuple(custos_faixas),
    )
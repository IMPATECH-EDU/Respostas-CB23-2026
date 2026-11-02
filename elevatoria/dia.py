"""Curvas da bomba por mínimos quadrados e o balanço do dia de operação (issue #10).

Este módulo junta peças que já existem na base:

- o registro de vazão do dia, a potência e as faixas tarifárias (de `fornecido/energia.py`,
  da equipe de energia);
- as regras de integração `Trapezio` e `Simpson` (de `elevatoria/integracao.py`, escritas por
  um colega);
- o NumPy ou o SciPy, para o ajuste de curvas (há mais de um caminho: veja `ajustar_polinomio`).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from elevatoria.integracao import Integrador
from fornecido.energia import FAIXAS_TARIFARIAS, potencia_eletrica


def ajustar_polinomio(x: np.ndarray, y: np.ndarray, grau: int) -> np.ndarray:
    """Coeficientes `[c0, c1, ..., c_grau]` do polinômio de mínimos quadrados de grau `grau`."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("x e y devem ser vetores 1D do mesmo tamanho")
    if grau < 0:
        raise ValueError(f"grau deve ser não negativo; recebi {grau}")
    if x.size < grau + 1:
        raise ValueError(f"número de pontos ({x.size}) deve ser pelo menos grau + 1 ({grau + 1})")

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
    """Volume, energia e custo de um dia de operação a partir do registro de vazão."""
    t = np.asarray(t, dtype=float)
    vazao = np.asarray(vazao, dtype=float)

    if t.ndim != 1 or vazao.ndim != 1 or t.size != vazao.size:
        raise ValueError("t e vazao devem ser vetores 1D do mesmo tamanho")

    limites_obrigatorios = [0.0, 18.0, 21.0, 24.0]
    for lim in limites_obrigatorios:
        if not np.any(np.isclose(t, lim)):
            raise ValueError(f"limite de faixa {lim} h não está presente em t")

    altura = np.polynomial.polynomial.polyval(vazao, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(vazao, coef_rendimento)
    potencia = potencia_eletrica(vazao, altura, rendimento)

    volume_m3 = 3.6 * integrador.integrar_tabela(t, vazao)
    energia_kwh = integrador.integrar_tabela(t, potencia)

    custos_faixas = []
    for inicio, fim, tarifa in FAIXAS_TARIFARIAS:
        mask = (t >= inicio) & (t <= fim)
        t_faixa = t[mask]
        pot_faixa = potencia[mask]
        integral_pot = integrador.integrar_tabela(t_faixa, pot_faixa)
        custos_faixas.append(float(tarifa * integral_pot))

    custo_por_faixa = tuple(custos_faixas)
    custo_reais = float(sum(custo_por_faixa))

    return ResumoDia(
        volume_m3=float(volume_m3),
        energia_kwh=float(energia_kwh),
        custo_reais=custo_reais,
        custo_por_faixa=custo_por_faixa,
    )
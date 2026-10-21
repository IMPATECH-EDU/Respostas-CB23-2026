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
    """Ajusta por mínimos quadrados um polinômio aos pontos fornecidos.

    O polinômio `p(x) = c0 + c1·x + ... + c_grau·x^grau` minimiza
    `Σ (y_i - p(x_i))²`. Os coeficientes retornados estão em ordem crescente e podem ser
    avaliados com `np.polynomial.polynomial.polyval`.

    Args:
        x: Abscissas dos pontos, como vetor unidimensional.
        y: Valores associados às abscissas, como vetor unidimensional do mesmo tamanho.
        grau: Grau inteiro não negativo do polinômio.

    Returns:
        Array de `grau + 1` coeficientes `[c0, c1, ..., c_grau]`, em ordem crescente.

    Raises:
        ValueError: Se `grau` não for um inteiro não negativo, se `x` e `y` não forem
            vetores unidimensionais de mesmo tamanho ou se houver menos pontos que
            coeficientes (`len(x) < grau + 1`).
    """
    if isinstance(grau, bool) or not isinstance(grau, (int, np.integer)) or grau < 0:
        raise ValueError(f"grau deve ser um inteiro não negativo; recebi {grau!r}")
    grau = int(grau)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("x e y devem ser vetores 1D do mesmo tamanho")
    if x.size < grau + 1:
        raise ValueError(f"menos pontos ({x.size}) que coeficientes ({grau + 1})")
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
    """Calcula o volume, a energia consumida e o custo diário de bombeamento.

    Args:
        t: Instantes do registro, em horas, como vetor unidimensional crescente. Deve conter
            os limites tarifários 0, 18, 21 e 24 h.
        vazao: Vazão registrada em cada instante, em L/s; deve ter o mesmo tamanho de `t`.
        coef_altura: Coeficientes crescentes do polinômio de altura da bomba, em metros,
            como retornados por `ajustar_polinomio`.
        coef_rendimento: Coeficientes crescentes do polinômio de rendimento da bomba,
            como retornados por `ajustar_polinomio`.
        integrador: Regra que implementa `integrar_tabela(x, y)`, usada para calcular as
            integrais do registro.

    Returns:
        `ResumoDia` com volume em m³, energia em kWh, custo total em reais e o custo de cada
        faixa tarifária, na ordem de `FAIXAS_TARIFARIAS`. O custo total é a soma dos custos
        por faixa.

    Raises:
        ValueError: Se `t` e `vazao` não forem vetores unidimensionais de mesmo tamanho,
            se faltar algum limite tarifário, se o rendimento calculado não for positivo
            ou se o integrador rejeitar uma tabela de entrada.
    """
    t = np.asarray(t, dtype=float)
    vazao = np.asarray(vazao, dtype=float)
    if t.ndim != 1 or vazao.ndim != 1 or t.size != vazao.size:
        raise ValueError("t e vazao devem ser vetores 1D do mesmo tamanho")
    limites = {inicio for inicio, _, _ in FAIXAS_TARIFARIAS} | {FAIXAS_TARIFARIAS[-1][1]}
    if not limites.issubset(t):
        raise ValueError(f"t deve conter os limites das faixas: {sorted(limites)}")
    altura = np.polynomial.polynomial.polyval(vazao, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(vazao, coef_rendimento)
    potencia = potencia_eletrica(vazao, altura, rendimento)
    volume = 3.6 * integrador.integrar_tabela(t, vazao)
    energia = integrador.integrar_tabela(t, potencia)
    custo_por_faixa = tuple(integrador.integrar_tabela(t[(t >= inicio) & (t <= fim)],potencia[(t >= inicio) & (t <= fim)]) * tarifa for inicio, fim, tarifa in FAIXAS_TARIFARIAS)
    custo_total = sum(custo_por_faixa)
    return ResumoDia(volume, energia, custo_total, custo_por_faixa)

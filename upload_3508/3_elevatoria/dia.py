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

    Escolha desta implementação: fatoração QR reduzida da matriz de Vandermonde `V = QR`, e
    depois `R c = Qᵀ y`, por substituição regressiva. Não forma `VᵀV` (as equações normais),
    que elevaria ao quadrado o número de condição. Também levanta `ValueError` se `grau` não
    for inteiro, se houver valores não finitos ou se os `x` distintos não bastarem para
    determinar o polinômio (diagonal de `R` nula).
    """
    abscissas = np.asarray(x, dtype=float)
    ordenadas = np.asarray(y, dtype=float)
    if abscissas.ndim != 1 or ordenadas.ndim != 1 or abscissas.size != ordenadas.size:
        raise ValueError("x e y devem ser vetores 1D do mesmo tamanho")
    if isinstance(grau, bool) or not isinstance(grau, (int, np.integer)):
        raise ValueError(f"o grau deve ser um inteiro; recebi {grau!r}")
    if grau < 0:
        raise ValueError(f"o grau não pode ser negativo; recebi {grau}")
    if abscissas.size < grau + 1:
        raise ValueError(f"{abscissas.size} pontos não determinam {grau + 1} coeficientes")
    if not (np.all(np.isfinite(abscissas)) and np.all(np.isfinite(ordenadas))):
        raise ValueError("x e y não podem ter NaN nem infinito")

    vandermonde = np.vander(abscissas, grau + 1, increasing=True)   # colunas 1, x, x², ...
    q, r = np.linalg.qr(vandermonde)                                 # modo reduzido
    diagonal = np.abs(np.diag(r))
    if np.any(diagonal <= 1e-12 * diagonal.max()):
        raise ValueError("x distintos insuficientes para o grau pedido (problema mal posto)")
    return solve_triangular(r, q.T @ ordenadas, lower=False)


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

    Os `ValueError` de `potencia_eletrica` (rendimento não positivo em algum instante) e do
    `integrador` (por exemplo, o Simpson com malha irregular) chegam a quem chamou.
    """
    instantes = np.asarray(t, dtype=float)
    q = np.asarray(vazao, dtype=float)
    if instantes.ndim != 1 or instantes.shape != q.shape:
        raise ValueError(f"t e vazao devem ser vetores 1D do mesmo tamanho; recebi "
                         f"{instantes.shape} e {q.shape}")
    limites = sorted({inicio for inicio, _, _ in FAIXAS_TARIFARIAS}
                     | {fim for _, fim, _ in FAIXAS_TARIFARIAS})
    faltando = [h for h in limites if h not in instantes]
    if faltando:
        raise ValueError(f"o registro não tem leitura nos limites das faixas: {faltando} h")

    altura = np.polynomial.polynomial.polyval(q, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(q, coef_rendimento)
    potencia = potencia_eletrica(q, altura, rendimento)               # kW em cada instante

    volume = 3.6 * integrador.integrar_tabela(instantes, q)            # L/s · h -> m³
    energia = integrador.integrar_tabela(instantes, potencia)
    custos = []
    for inicio, fim, tarifa in FAIXAS_TARIFARIAS:
        # Integra cada faixa só com os seus pontos: a tarifa salta nos limites, e a regra não
        # deve "ver" o salto, senão a ordem de convergência cai (Etapa 1(b) do marco4.py).
        na_faixa = (instantes >= inicio) & (instantes <= fim)
        custos.append(tarifa * integrador.integrar_tabela(instantes[na_faixa], potencia[na_faixa]))
    custo_por_faixa = tuple(float(c) for c in custos)
    return ResumoDia(volume_m3=float(volume), energia_kwh=float(energia),
                     custo_reais=float(sum(custo_por_faixa)), custo_por_faixa=custo_por_faixa)

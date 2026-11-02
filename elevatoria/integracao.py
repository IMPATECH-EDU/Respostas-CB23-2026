"""Regras de integração numérica: trapézio e Simpson.

Escrito por um colega da equipe. Todas as regras seguem a interface da classe abstrata
`Integrador` e podem integrar de dois jeitos:

- `integrar(f, a, b, n)`: uma função `f` (que recebe e devolve `ndarray`) em `[a, b]`, com `n`
  subintervalos iguais;
- `integrar_tabela(x, y)`: valores `y` conhecidos só nos pontos `x` (dados medidos).

Veja a issue #11 no ENUNCIADO_MARCO4.md.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

import numpy as np

Funcao = Callable[[np.ndarray], np.ndarray]


def _validar_tabela(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Converte para `ndarray` e confere: 1D, mesmo tamanho (≥ 2) e `x` estritamente crescente."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or x.size < 2:
        raise ValueError("x e y devem ser vetores 1D do mesmo tamanho, com pelo menos 2 pontos")
    if not np.all(np.diff(x) > 0):
        raise ValueError("x deve ser estritamente crescente")
    return x, y


class Integrador(ABC):
    """Interface comum das regras de integração. A classe não pode ser instanciada."""

    #: Ordem de convergência da regra: o erro cai como h^ordem.
    ordem_teorica: int = 0

    @abstractmethod
    def integrar(self, f: Funcao, a: float, b: float, n: int) -> float:
        """Integral de `f` em `[a, b]` com `n` subintervalos iguais."""

    @abstractmethod
    def integrar_tabela(self, x: np.ndarray, y: np.ndarray) -> float:
        """Integral a partir dos valores `y` nos pontos `x`."""


class Trapezio(Integrador):
    """Regra composta do trapézio (ordem 2)."""

    ordem_teorica = 2

    def integrar(self, f: Funcao, a: float, b: float, n: int) -> float:
        """Trapézio composto com `n` subintervalos iguais. `ValueError` se `n < 1`."""
        if n < 1:
            raise ValueError(f"n deve ser pelo menos 1; recebi {n}")
        x = np.linspace(a, b, n + 1)
        y = np.asarray(f(x), dtype=float)
        h = (b - a) / n
        return float(h * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1]))

    def integrar_tabela(self, x: np.ndarray, y: np.ndarray) -> float:
        """Soma das áreas dos trapézios entre pontos consecutivos.

        Aceita malha **não uniforme**: cada trapézio usa a sua própria largura `x[i+1] - x[i]`.
        """
        x, y = _validar_tabela(x, y)
        # O SCADA registra uma leitura a cada 15 min, então o passo é o mesmo em toda a tabela.
        h = x[1] - x[0]
        return float(h * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1]))


class Simpson(Integrador):
    """Regra composta de Simpson (ordem 4)."""

    ordem_teorica = 4

    def integrar(self, f: Funcao, a: float, b: float, n: int) -> float:
        """Simpson composto com `n` subintervalos iguais. `ValueError` se `n` não for par e positivo."""
        if n < 2 or n % 2:
            raise ValueError(f"n deve ser par e positivo; recebi {n}")
        x = np.linspace(a, b, n + 1)
        y = np.asarray(f(x), dtype=float)
        h = (b - a) / n
        return float(h / 3.0 * (y[0] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-1:2].sum() + y[-1]))

    def integrar_tabela(self, x: np.ndarray, y: np.ndarray) -> float:
        """Simpson a partir de uma tabela.

        Exige malha **uniforme** e um número **ímpar** de pontos (um número par de
        subintervalos); levanta `ValueError` caso contrário.
        """
        x, y = _validar_tabela(x, y)
        passos = np.diff(x)
        if not np.allclose(passos, passos[0], rtol=1e-9, atol=0.0):
            raise ValueError("a regra de Simpson exige pontos igualmente espaçados")
        if x.size % 2 == 0:
            raise ValueError("a regra de Simpson exige um número ímpar de pontos")
        h = passos[0]
        return float(h / 3.0 * (y[0] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-1:2].sum() + y[-1]))

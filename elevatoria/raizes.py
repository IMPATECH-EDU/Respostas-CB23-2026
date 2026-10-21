"""Métodos para encontrar raízes de funções de uma variável.

Escrito por um colega da equipe. Todos os métodos seguem a interface da classe abstrata
`MetodoRaiz` e, por isso, servem como `resolvedor` da `Tubulacao` (fornecido/hidraulica.py).
Veja a issue #9 no ENUNCIADO_MARCO3.md.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional

Funcao = Callable[[float], float]


@dataclass(frozen=True)
class ResultadoRaiz:
    """Resultado de um método de raiz."""

    raiz: float                     # a aproximação final
    iteracoes: int                  # número de iterações feitas
    convergiu: bool                 # False se parou por atingir max_iter
    historico: tuple[float, ...]    # as aproximações sucessivas, da primeira à última


class MetodoRaiz(ABC):
    """Interface comum dos métodos de raiz. A classe não pode ser instanciada.

    `tol` é a tolerância do critério de parada e `max_iter`, o número máximo de iterações.
    Levanta `ValueError` se `tol <= 0` ou `max_iter < 1`.
    """

    def __init__(self, tol: float = 1e-10, max_iter: int = 100) -> None:
        if tol <= 0:
            raise ValueError(f"tol deve ser positiva; recebi {tol}")
        if max_iter < 1:
            raise ValueError(f"max_iter deve ser pelo menos 1; recebi {max_iter}")
        self._tol = tol
        self._max_iter = max_iter

    @property
    def tol(self) -> float:
        """Tolerância do critério de parada."""
        return self._tol

    @property
    def max_iter(self) -> int:
        """Número máximo de iterações."""
        return self._max_iter

    @abstractmethod
    def encontrar(self, f: Funcao, a: float, b: float) -> ResultadoRaiz:
        """Uma raiz de `f` no intervalo `[a, b]`."""


class Bisseccao(MetodoRaiz):
    """Método da bissecção.

    Exige que `f(a)` e `f(b)` tenham sinais opostos (`ValueError` caso contrário). A cada
    iteração, divide o intervalo ao meio e fica com a metade em que há troca de sinal. Para
    quando a largura do intervalo fica menor que `tol` e devolve o ponto médio. O
    `historico` guarda o ponto médio de cada iteração.
    """

    def encontrar(self, f: Funcao, a: float, b: float) -> ResultadoRaiz:
        """Uma raiz de `f` em `[a, b]` pela bissecção. O(log2((b - a) / tol)) iterações."""
        if a >= b:
            raise ValueError(f"o intervalo deve ter a < b; recebi [{a}, {b}]")
        fa, fb = f(a), f(b)
        if fa == 0:
            return ResultadoRaiz(a, 0, True, (a,))
        if fb == 0:
            return ResultadoRaiz(b, 0, True, (b,))
        if fa * fb > 0:
            raise ValueError(f"f(a) e f(b) têm o mesmo sinal em [{a}, {b}]: não há garantia de raiz")
        historico = []
        for k in range(1, self.max_iter + 1):
            m = 0.5 * (a + b)
            historico.append(m)
            fm = f(m)
            if fm == 0:
                return ResultadoRaiz(m, k, True, tuple(historico))
            if fa * fm < 0:
                b = m
            else:
                a, fa = m, fm
            if b - a < self.tol:
                m = 0.5 * (a + b)
                historico.append(m)
                return ResultadoRaiz(m, k, True, tuple(historico))
        return ResultadoRaiz(0.5 * (a + b), self.max_iter, False, tuple(historico))


class Newton(MetodoRaiz):
    """Método de Newton: `x_{k+1} = x_k - f(x_k) / f'(x_k)`, a partir do ponto médio de `[a, b]`.

    A derivada é `df(x)`, se fornecida, ou a diferença central `(f(x+h) - f(x-h)) / (2h)`.
    Para quando `|x_{k+1} - x_k| < tol`. Levanta `ValueError` se a derivada for zero. Perto da
    raiz, a convergência é quadrática: o número de dígitos corretos dobra a cada iteração. O
    `historico` guarda o ponto inicial e cada nova aproximação.
    """

    def __init__(self, tol: float = 1e-10, max_iter: int = 100,
                 df: Optional[Funcao] = None, h: float = 1e-6) -> None:
        super().__init__(tol, max_iter)
        if h <= 0:
            raise ValueError(f"h deve ser positivo; recebi {h}")
        self._df = df
        self._h = h

    def _derivada(self, f: Funcao, x: float) -> float:
        """Derivada de `f` em `x`: `df(x)` se fornecida; senão, diferença central."""
        if self._df is not None:
            return self._df(x)
        return (f(x + self._h) - f(x - self._h)) / (2.0 * self._h)

    def encontrar(self, f: Funcao, a: float, b: float) -> ResultadoRaiz:
        """Uma raiz de `f` pelo método de Newton, começando no ponto médio de `[a, b]`."""
        if a >= b:
            raise ValueError(f"o intervalo deve ter a < b; recebi [{a}, {b}]")
        x = 0.5 * (a + b)
        historico = [x]

        for k in range(1, self.max_iter + 1):
            derivada = self._derivada(f, x)
            if derivada == 0:
                raise ValueError(f"derivada nula em x = {x}: o método de Newton não pode continuar")
            x_novo = x - f(x) / derivada
            historico.append(x_novo)
            if abs(x_novo - x) < self.tol:
                return ResultadoRaiz(x_novo, k, True, tuple(historico))
            x = x_novo
        return ResultadoRaiz(x, self.max_iter, False, tuple(historico))

"""Grandezas com incerteza e propagação de incertezas (código fornecido; NÃO ALTERE).

Uma `Medida` é um valor acompanhado da sua incerteza absoluta, na mesma unidade:
`Medida(30.0, 0.5)` representa 30,0 ± 0,5. As operações aritméticas entre medidas (e entre
uma medida e um número) devolvem uma nova `Medida`, com a incerteza calculada pela
propagação de primeira ordem.

Hipótese da propagação: os erros dos operandos são INDEPENDENTES. Sejam `A = Medida(a, ua)`
e `B = Medida(b, ub)`; um número `c` entra nas contas como `Medida(c, 0)`.

    A + B, A - B   ->  incerteza sqrt(ua² + ub²)
    A * B          ->  incerteza sqrt((b·ua)² + (a·ub)²)
    A / B          ->  incerteza sqrt((ua/b)² + (a·ub/b²)²)
    A ** n         ->  incerteza |n| · |a|^(n-1) · ua      (n é um número, não uma Medida)
    -A             ->  incerteza ua

As formas acima equivalem às fórmulas com incertezas relativas (por exemplo, para o produto,
|a·b| · sqrt((ua/a)² + (ub/b)²)), mas não dividem por `a` nem por `b`, e por isso continuam
válidas quando um dos valores é zero.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import Union

Numero = Union[int, float]


@dataclass(frozen=True)
class Medida:
    """Valor com incerteza absoluta (imutável).

    Levanta `ValueError` se o valor não for finito ou se a incerteza for negativa ou não
    finita. Os dois campos são convertidos para `float`.
    """

    valor: float
    incerteza: float = 0.0

    def __post_init__(self) -> None:
        valor, incerteza = float(self.valor), float(self.incerteza)
        if not math.isfinite(valor):
            raise ValueError(f"o valor deve ser finito; recebi {self.valor!r}")
        if not math.isfinite(incerteza) or incerteza < 0.0:
            raise ValueError(f"a incerteza deve ser finita e não negativa; recebi {self.incerteza!r}")
        object.__setattr__(self, "valor", valor)
        object.__setattr__(self, "incerteza", incerteza)

    # ------------------------------------------------------------------------------------
    # Propriedades e comparação
    # ------------------------------------------------------------------------------------
    @property
    def incerteza_relativa(self) -> float:
        """`incerteza / |valor|`; `math.inf` se o valor for zero."""
        if self.valor == 0.0:
            return math.inf
        return self.incerteza / abs(self.valor)

    def compativel_com(self, outra: Medida | Numero, k: float = 2.0) -> bool:
        """`True` se `|a - b| <= k · sqrt(ua² + ub²)`; um número tem incerteza zero."""
        b = _como_medida(outra)
        if b is NotImplemented:
            raise TypeError(f"não sei comparar Medida com {type(outra).__name__}")
        return abs(self.valor - b.valor) <= k * math.hypot(self.incerteza, b.incerteza)

    # ------------------------------------------------------------------------------------
    # Aritmética
    # ------------------------------------------------------------------------------------
    def __add__(self, outra: Medida | Numero) -> Medida:
        b = _como_medida(outra)
        if b is NotImplemented:
            return NotImplemented
        return Medida(self.valor + b.valor, math.hypot(self.incerteza, b.incerteza))

    def __radd__(self, outra: Numero) -> Medida:
        return self.__add__(outra)

    def __sub__(self, outra: Medida | Numero) -> Medida:
        b = _como_medida(outra)
        if b is NotImplemented:
            return NotImplemented
        return Medida(self.valor - b.valor, math.hypot(self.incerteza, b.incerteza))

    def __rsub__(self, outra: Numero) -> Medida:
        a = _como_medida(outra)
        if a is NotImplemented:
            return NotImplemented
        return a - self

    def __mul__(self, outra: Medida | Numero) -> Medida:
        b = _como_medida(outra)
        if b is NotImplemented:
            return NotImplemented
        a = self
        return Medida(a.valor * b.valor,
                      math.hypot(b.valor * a.incerteza, a.valor * b.incerteza))

    def __rmul__(self, outra: Numero) -> Medida:
        return self.__mul__(outra)

    def __truediv__(self, outra: Medida | Numero) -> Medida:
        b = _como_medida(outra)
        if b is NotImplemented:
            return NotImplemented
        if b.valor == 0.0:
            raise ZeroDivisionError("divisão por uma Medida de valor zero")
        a = self
        return Medida(a.valor / b.valor,
                      math.hypot(a.incerteza / b.valor, a.valor * b.incerteza / b.valor ** 2))

    def __rtruediv__(self, outra: Numero) -> Medida:
        a = _como_medida(outra)
        if a is NotImplemented:
            return NotImplemented
        return a / self

    def __pow__(self, n: Numero) -> Medida:
        if isinstance(n, Medida) or not isinstance(n, Real):
            return NotImplemented
        n = float(n)
        a, ua = self.valor, self.incerteza
        if a == 0.0 and n < 1.0:
            raise ValueError("0 elevado a um expoente menor que 1 não tem incerteza definida")
        if a < 0.0 and not n.is_integer():
            raise ValueError("base negativa com expoente não inteiro")
        return Medida(a ** n, abs(n) * abs(a) ** (n - 1.0) * ua)

    def __neg__(self) -> Medida:
        return Medida(-self.valor, self.incerteza)

    # ------------------------------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------------------------------
    def __str__(self) -> str:
        """`valor ± incerteza`, com a incerteza em 2 algarismos significativos.

        O valor é arredondado na mesma casa decimal da incerteza. Exemplos:
        `Medida(12.3456, 0.321)` -> `"12.35 ± 0.32"`; `Medida(1234.6, 12.0)` -> `"1235 ± 12"`.
        Com incerteza zero, o valor é mostrado com até 10 algarismos: `"9.81 ± 0"`.
        """
        if self.incerteza == 0.0:
            return f"{self.valor:.10g} ± 0"
        casas = 1 - math.floor(math.log10(self.incerteza))
        u = round(self.incerteza, casas)
        casas = 1 - math.floor(math.log10(u))          # 0.0996 vira 0.10, e não 0.100
        u, v = round(self.incerteza, casas), round(self.valor, casas)
        if casas > 0:
            return f"{v:.{casas}f} ± {u:.{casas}f}"
        return f"{v:.0f} ± {u:.0f}"


def _como_medida(x: object) -> Medida:
    """Converte um número em `Medida(x, 0)`; devolve `NotImplemented` para outros tipos."""
    if isinstance(x, Medida):
        return x
    if isinstance(x, Real):
        return Medida(float(x), 0.0)
    return NotImplemented

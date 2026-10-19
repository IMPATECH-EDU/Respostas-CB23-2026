"""Totalizadores: somas de muitas parcelas, uma de cada vez.

Usados para totalizar os pulsos do medidor de vazão (cada pulso vale 0,1 L). Todos os
acumuladores seguem a interface da classe abstrata `Acumulador`, então qualquer código que
recebe um `Acumulador` funciona com qualquer uma das estratégias (polimorfismo).

Este módulo foi escrito por um colega. Veja a issue #7 no ENUNCIADO_MARCO2.md.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable


class Acumulador(ABC):
    """Soma de uma sequência de números, parcela a parcela.

    As subclasses definem `adicionar` e `total`. A classe não pode ser instanciada.
    """

    @abstractmethod
    def adicionar(self, x: float) -> None:
        """Acrescenta a parcela `x` ao total."""

    @property
    @abstractmethod
    def total(self) -> float:
        """O total acumulado até agora, como `float`."""

    def adicionar_todos(self, valores: Iterable[float]) -> None:
        """Chama `adicionar` para cada elemento de `valores`, na ordem. O(n)."""
        for x in valores:
            self.adicionar(x)


class AcumuladorIngenuo(Acumulador):
    """Soma direta em `float`: `soma = soma + x` a cada parcela."""

    def __init__(self) -> None:
        self._soma = 0.0

    def adicionar(self, x: float) -> None:
        """Acrescenta `x` à soma."""
        self._soma = self._soma + float(x)

    @property
    def total(self) -> float:
        """A soma acumulada."""
        return self._soma


class AcumuladorKahan(Acumulador):
    """Soma compensada de Kahan.

    Além da soma, guarda uma correção: a parte de cada parcela que se perdeu no
    arredondamento da soma. A correção é descontada da parcela seguinte, e assim o erro de
    arredondamento não se acumula.
    """

    def __init__(self) -> None:
        self._soma = 0.0
        self._correcao = 0.0

    def adicionar(self, x: float) -> None:
        """Acrescenta `x` à soma, compensando o arredondamento."""
        y = float(x) - self._correcao
        t = self._soma + y
        self._correcao = t - (self._soma + y)   # o que se perdeu ao arredondar soma + y
        self._soma = t

    @property
    def total(self) -> float:
        """A soma acumulada."""
        return self._soma


class AcumuladorInteiro(Acumulador):
    """Soma em aritmética inteira, para parcelas com um número fixo de casas decimais.

    `AcumuladorInteiro(escala)` converte cada parcela, uma única vez, para o inteiro
    `round(x * escala)`, soma os inteiros e devolve `soma / escala` em `total`. Com
    `escala = 10`, por exemplo, 0,1 L vira o inteiro 1 (décimos de litro). Levanta
    `ValueError` se `escala` não for um inteiro positivo.
    """

    def __init__(self, escala: int) -> None:
        if isinstance(escala, bool) or not isinstance(escala, int) or escala < 1:
            raise ValueError(f"escala deve ser um inteiro positivo; recebi {escala!r}")
        self._escala = escala
        self._soma = 0

    def adicionar(self, x: float) -> None:
        """Acrescenta `round(x * escala)` à soma inteira."""
        self._soma += round(float(x) * self._escala)

    @property
    def total(self) -> float:
        """A soma inteira dividida pela escala."""
        return self._soma / self._escala

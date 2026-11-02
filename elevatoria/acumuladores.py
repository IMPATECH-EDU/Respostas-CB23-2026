"""Acumuladores numéricos para totalização de medições (issue #7)."""
from __future__ import annotations


class Acumulador:
    """Classe base para acumuladores numéricos."""

    @property
    def total(self) -> float:
        """Devolve o valor total acumulado."""
        raise NotImplementedError

    def adicionar(self, val: float) -> None:
        """Adiciona uma parcela ao totalizador."""
        raise NotImplementedError


class AcumuladorIngenuo(Acumulador):
    """Acumulador simples em ponto flutuante (sujeito a erros de arredondamento)."""

    def __init__(self) -> None:
        self._total = 0.0

    def adicionar(self, val: float) -> None:
        self._total += float(val)

    @property
    def total(self) -> float:
        return self._total


class AcumuladorKahan(Acumulador):
    """Acumulador com algoritmo de Kahan para compensação de erro de arredondamento."""

    def __init__(self) -> None:
        self._total = 0.0
        self._c = 0.0

    def adicionar(self, val: float) -> None:
        y = float(val) - self._c
        t = self._total + y
        self._c = (t - self._total) - y
        self._total = t

    @property
    def total(self) -> float:
        return self._total


class AcumuladorInteiro(Acumulador):
    """Acumulador exato que trabalha com contagem discreta de pulsos inteiros."""

    def __init__(self, fator: float = 1.0) -> None:
        self._fator = float(fator)
        self._total_int = 0

    def adicionar(self, val: float) -> None:
        self._total_int += int(round(float(val) * self._fator))

    @property
    def total(self) -> float:
        return float(self._total_int / self._fator)
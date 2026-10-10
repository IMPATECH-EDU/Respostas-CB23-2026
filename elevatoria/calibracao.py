"""Curvas de calibração: conversão de contagens do A/D em unidade de engenharia.

Escrito por um colega da equipe. Não há issues abertas neste módulo: leia-o e use-o.
"""
from __future__ import annotations

from typing import Callable, Iterable, Union

import numpy as np
from scipy.interpolate import CubicSpline, make_interp_spline

Escalar = Union[int, float]


class CurvaCalibracao:
    """Converte uma grandeza de entrada em uma de saída, interpolando uma tabela.

    `CurvaCalibracao(entradas, saidas, metodo)` guarda, por composição, um interpolador do
    SciPy construído a partir da tabela:

    - `metodo="linear"`: `make_interp_spline(entradas, saidas, k=1)`;
    - `metodo="spline"`: `CubicSpline(entradas, saidas)` (spline cúbica).

    Levanta `ValueError` se `entradas` e `saidas` não forem vetores 1D do mesmo tamanho, com
    pelo menos 3 pontos, se `entradas` não for estritamente crescente ou se `metodo` não for
    `"linear"` nem `"spline"`.

    A curva **não extrapola**: qualquer método que receba um ponto fora do domínio levanta
    `ValueError`.

    Exemplo:
        >>> curva = CurvaCalibracao([0, 1, 2], [0, 10, 20], "linear")
        >>> curva(1.5)
        15.0
    """

    def __init__(self, entradas: Iterable[float], saidas: Iterable[float],
                 metodo: str = "spline") -> None:
        x = np.array(entradas, dtype=float)
        y = np.array(saidas, dtype=float)
        if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
            raise ValueError("entradas e saidas devem ser vetores 1D do mesmo tamanho")
        if x.size < 3:
            raise ValueError(f"a tabela precisa de pelo menos 3 pontos; recebi {x.size}")
        if not np.all(np.diff(x) > 0):
            raise ValueError("as entradas devem ser estritamente crescentes")
        if metodo == "linear":
            self._interpolador = make_interp_spline(x, y, k=1)
        elif metodo == "spline":
            self._interpolador = CubicSpline(x, y)
        else:
            raise ValueError(f"método desconhecido: {metodo!r} (use 'linear' ou 'spline')")
        self._metodo = metodo
        self._dominio = (float(x[0]), float(x[-1]))

    @property
    def metodo(self) -> str:
        """O método de interpolação (`"linear"` ou `"spline"`)."""
        return self._metodo

    @property
    def dominio(self) -> tuple[float, float]:
        """`(mínimo, máximo)` das entradas."""
        return self._dominio

    def __call__(self, x: Escalar | np.ndarray) -> float | np.ndarray:
        """Valor interpolado em `x`: `float` para escalar, `ndarray` para array (ou lista).

        Levanta `ValueError` se algum ponto estiver fora do domínio.
        """
        pontos = np.asarray(x, dtype=float)
        self._conferir_dominio(pontos)
        valores = self._interpolador(pontos)
        return float(valores) if pontos.ndim == 0 else np.asarray(valores)

    def derivada(self, x: float) -> float:
        """Derivada exata do interpolador em `x`."""
        self._conferir_dominio(np.asarray(x, dtype=float))
        return float(self._interpolador(x, 1))

    def diferenca_adiante(self, x: float, h: float) -> float:
        """Aproximação da derivada por diferença adiante: `(f(x + h) - f(x)) / h`.

        Levanta `ValueError` se `h <= 0` ou se `x` ou `x + h` estiverem fora do domínio.
        """
        if h <= 0:
            raise ValueError(f"h deve ser positivo; recebi {h}")
        return (self(x + h) - self(x)) / h

    def erro_maximo(self, funcao_real: Callable[[np.ndarray], np.ndarray],
                    n: int = 1000) -> float:
        """Máximo de `|curva(x) - funcao_real(x)|` em `n` pontos igualmente espaçados no domínio."""
        if n < 2:
            raise ValueError(f"n deve ser pelo menos 2; recebi {n}")
        x = np.linspace(self._dominio[0], self._dominio[1], n)
        return float(np.max(np.abs(self(x) - np.asarray(funcao_real(x)))))

    def _conferir_dominio(self, pontos: np.ndarray) -> None:
        """Levanta `ValueError` se algum ponto estiver fora do domínio."""
        inicio, fim = self._dominio
        if np.any(pontos < inicio) or np.any(pontos > fim):
            raise ValueError(f"ponto fora do domínio [{inicio}, {fim}]: a curva não extrapola")

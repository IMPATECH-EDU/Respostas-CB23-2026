from __future__ import annotations

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


class SerieTemporal:
    """Série temporal numérica unidimensional e imutável, apoiada em um `ndarray` de floats.

    Nenhum método modifica a série: as operações devolvem uma nova `SerieTemporal` ou um `float`.
    Todas as contas usam apenas operações do NumPy, sem laços sobre os elementos.
    """

    def __init__(self, valores: np.ndarray | list[float]) -> None:
        """Cria a série a partir de uma lista ou de um `ndarray`.

        Levanta `ValueError` se os valores não formarem um vetor unidimensional.
        """
        arr = np.asarray(valores, dtype=float)
        if arr.ndim != 1:
            raise ValueError("Série temporal deve ser unidimensional")
        self._valores = arr

    @property
    def dtype(self) -> np.dtype:
        """O `dtype` dos valores armazenados (sempre `float64`)."""
        return self._valores.dtype

    @classmethod
    def de_lista(cls, lista: list[float]) -> SerieTemporal:
        """Cria uma série a partir de uma lista. Levanta `ValueError` se ela não for 1D."""
        return cls(lista)

    def __len__(self) -> int:
        """Número de pontos da série."""
        return len(self._valores)

    def __getitem__(self, item: int | slice) -> SerieTemporal | float:
        """Um índice devolve um `float`; uma fatia devolve uma nova `SerieTemporal`."""
        if isinstance(item, slice):
            return SerieTemporal(self._valores[item])
        return float(self._valores[item])

    def __add__(self, other: SerieTemporal | float) -> SerieTemporal:
        """Soma elemento a elemento com outra série (mesmo tamanho) ou com um escalar."""
        if isinstance(other, SerieTemporal):
            return SerieTemporal(self._valores + other._valores)
        return SerieTemporal(self._valores + float(other))

    def __radd__(self, other: float) -> SerieTemporal:
        """Soma com o escalar à esquerda: `2 + s`."""
        return self.__add__(other)

    def __sub__(self, other: SerieTemporal | float) -> SerieTemporal:
        """Subtrai outra série (mesmo tamanho) ou um escalar, elemento a elemento."""
        if isinstance(other, SerieTemporal):
            return SerieTemporal(self._valores - other._valores)
        return SerieTemporal(self._valores - float(other))

    def __rsub__(self, other: float) -> SerieTemporal:
        """Subtração com o escalar à esquerda: `2 - s`."""
        return SerieTemporal(float(other) - self._valores)

    def __mul__(self, scalar: float) -> SerieTemporal:
        """Multiplica todos os elementos por um escalar."""
        return SerieTemporal(self._valores * float(scalar))

    def __rmul__(self, scalar: float) -> SerieTemporal:
        """Multiplicação com o escalar à esquerda: `2 * s`."""
        return self.__mul__(scalar)

    def __truediv__(self, other: SerieTemporal | float) -> SerieTemporal:
        """Divide elemento a elemento por outra série (mesmo tamanho) ou por um escalar."""
        if isinstance(other, SerieTemporal):
            return SerieTemporal(self._valores / other._valores)
        return SerieTemporal(self._valores / float(other))

    def media(self) -> float:
        """Média aritmética dos valores."""
        return float(np.mean(self._valores))

    def mean(self) -> float:
        """Sinônimo de `media`."""
        return self.media()

    def desvio(self, ddof: int = 1) -> float:
        """Desvio padrão, com `ddof` graus de liberdade subtraídos (1 por padrão: amostral)."""
        return float(np.std(self._valores, ddof=ddof))

    def std(self, ddof: int = 1) -> float:
        """Sinônimo de `desvio`."""
        return self.desvio(ddof=ddof)

    def amplitude(self) -> float:
        """Máximo menos mínimo; 0.0 para uma série vazia."""
        if len(self._valores) == 0:
            return 0.0
        return float(np.max(self._valores) - np.min(self._valores))

    def sum(self) -> float:
        """Soma dos valores."""
        return float(np.sum(self._valores))

    def min(self) -> float:
        """Menor valor da série."""
        return float(np.min(self._valores))

    def max(self) -> float:
        """Maior valor da série."""
        return float(np.max(self._valores))

    def media_movel(self, w: int) -> SerieTemporal:
        """Média móvel com janela de `w` pontos: devolve `len(self) - w + 1` valores.

        O i-ésimo valor é a média de `self[i : i + w]`. Levanta `ValueError` se `w` não for um
        inteiro, se `w <= 0` ou se `w` for maior que o tamanho da série.
        """
        if type(w) is not int or w <= 0 or w > len(self._valores):
            raise ValueError(f"Tamanho de janela w={w} inválido para série de tamanho {len(self._valores)}")
        return SerieTemporal(sliding_window_view(self._valores, w).mean(axis=1))

    def reamostrar(self, k: int) -> SerieTemporal:
        """Médias de blocos consecutivos de `k` pontos: devolve `len(self) // k` valores.

        Os pontos que sobram no fim (quando `len(self)` não é múltiplo de `k`) são descartados.
        Levanta `ValueError` se `k` não for um inteiro, se `k <= 0` ou se `k` for maior que o
        tamanho da série.
        """
        if type(k) is not int or k <= 0 or k > len(self._valores):
            raise ValueError(f"Tamanho de bloco k={k} inválido para série de tamanho {len(self._valores)}")
        n_blocos = len(self._valores) // k
        return SerieTemporal(self._valores[: n_blocos * k].reshape(n_blocos, k).mean(axis=1))

    def normalizar(self) -> SerieTemporal:
        """Série padronizada: `(x - média) / desvio` (desvio amostral).

        Levanta `ValueError` se o desvio padrão for zero.
        """
        m = self.media()
        s = self.desvio(ddof=1)
        if s == 0:
            raise ValueError("Não é possível normalizar uma série com desvio padrão igual a zero.")
        return SerieTemporal((self._valores - m) / s)

    def variacao(self) -> SerieTemporal:
        """Diferenças entre pontos consecutivos (`len(self) - 1` valores; vazia se houver ≤ 1 ponto)."""
        if len(self._valores) <= 1:
            return SerieTemporal([])
        return SerieTemporal(np.diff(self._valores))
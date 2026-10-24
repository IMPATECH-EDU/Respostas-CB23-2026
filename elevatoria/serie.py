from __future__ import annotations

import math
import numpy as np


class SerieTemporal:
    """Representa uma série temporal numérica unidimensional e imutável."""

    def __init__(self, valores: np.ndarray | list[float]):
        arr = np.asarray(valores, dtype=float)
        if arr.ndim != 1:
            raise ValueError("Série temporal deve ser unidimensional")
        self._valores = arr

    @property
    def dtype(self) -> np.dtype:
        return self._valores.dtype

    @classmethod
    def de_lista(cls, lista: list[float]) -> SerieTemporal:
        return cls(lista)

    def __len__(self) -> int:
        return len(self._valores)

    def __getitem__(self, item: int | slice) -> SerieTemporal | float:
        if isinstance(item, slice):
            return SerieTemporal(self._valores[item])
        return float(self._valores[item])

    def __add__(self, other: SerieTemporal | float) -> SerieTemporal:
        if isinstance(other, SerieTemporal):
            return SerieTemporal(self._valores + other._valores)
        return SerieTemporal(self._valores + float(other))

    def __radd__(self, other: float) -> SerieTemporal:
        return self.__add__(other)

    def __sub__(self, other: SerieTemporal | float) -> SerieTemporal:
        if isinstance(other, SerieTemporal):
            return SerieTemporal(self._valores - other._valores)
        return SerieTemporal(self._valores - float(other))

    def __rsub__(self, other: float) -> SerieTemporal:
        return SerieTemporal(float(other) - self._valores)

    def __mul__(self, scalar: float) -> SerieTemporal:
        return SerieTemporal(self._valores * float(scalar))

    def __rmul__(self, scalar: float) -> SerieTemporal:
        return self.__mul__(scalar)

    def __truediv__(self, other: SerieTemporal | float) -> SerieTemporal:
        if isinstance(other, SerieTemporal):
            return SerieTemporal(self._valores / other._valores)
        return SerieTemporal(self._valores / float(other))

    def media(self) -> float:
        return float(np.mean(self._valores))

    def mean(self) -> float:
        return self.media()

    def desvio(self, ddof: int = 1) -> float:
        return float(np.std(self._valores, ddof=ddof))

    def std(self, ddof: int = 1) -> float:
        return self.desvio(ddof=ddof)

    def amplitude(self) -> float:
        if len(self._valores) == 0:
            return 0.0
        return float(np.max(self._valores) - np.min(self._valores))

    def sum(self) -> float:
        return float(np.sum(self._valores))

    def min(self) -> float:
        return float(np.min(self._valores))

    def max(self) -> float:
        return float(np.max(self._valores))

    def media_movel(self, w: int) -> SerieTemporal:
        if type(w) is not int or w <= 0 or w > len(self._valores):
            raise ValueError(f"Tamanho de janela w={w} inválido para série de tamanho {len(self._valores)}")

        medias = [
            float(np.mean(self._valores[i : i + w]))
            for i in range(len(self._valores) - w + 1)
        ]
        return SerieTemporal.de_lista(medias)

    def reamostrar(self, k: int) -> SerieTemporal:
        if type(k) is not int or k <= 0 or len(self._valores) % k != 0:
            raise ValueError(f"Tamanho de bloco k={k} inválido para série de tamanho {len(self._valores)}")

        medias = [
            float(np.mean(self._valores[i : i + k]))
            for i in range(0, len(self._valores), k)
        ]
        return SerieTemporal.de_lista(medias)

    def normalizar(self) -> SerieTemporal:
        m = self.media()
        s = self.desvio(ddof=1)
        if s == 0:
            raise ValueError("Não é possível normalizar uma série com desvio padrão igual a zero.")
        return SerieTemporal((self._valores - m) / s)


    def variacao(self) -> SerieTemporal:
        if len(self._valores) <= 1:
            return SerieTemporal([])
        return SerieTemporal(np.diff(self._valores))
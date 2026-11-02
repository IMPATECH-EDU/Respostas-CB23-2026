"""Séries temporais unidimensionais como subclasse de `numpy.ndarray`."""
from __future__ import annotations

from typing import Sequence

import numpy as np


class SerieTemporal(np.ndarray):
    """Série temporal unidimensional de `float`, com métodos de análise vetorizados."""

    @classmethod
    def de_lista(cls, seq: Sequence[float]) -> SerieTemporal:
        """Cria uma `SerieTemporal` de `float` a partir de qualquer sequência."""
        arr = np.array(seq, dtype=float)
        if arr.ndim != 1:
            raise ValueError(f"a série deve ser unidimensional; recebi ndim={arr.ndim}")
        return arr.view(cls)

    def media_movel(self, janela: int) -> SerieTemporal:
        """Médias de `janela` pontos consecutivos: `n - janela + 1` valores."""
        if janela < 1 or janela > len(self):
            raise ValueError(f"janela deve estar entre 1 e {len(self)}; recebi {janela}")
        acumulada = np.pad(np.cumsum(self), (1, 0), mode="constant", constant_values=0.0)
        res = (acumulada[janela:] - acumulada[:-janela]) / janela
        return SerieTemporal.de_lista(res)

    def variacao(self) -> SerieTemporal:
        """Diferenças entre pontos consecutivos (`n - 1` valores)."""
        return np.diff(self)

    def amplitude(self) -> float:
        """Máximo menos mínimo da série, como `float`."""
        return float(self.max() - self.min())

    def normalizar(self) -> SerieTemporal:
        """Série padronizada `(x - média) / desvio`, com desvio amostral (`ddof=1`)."""
        desvio = float(self.std(ddof=1))
        if desvio == 0.0:
            raise ValueError("não é possível normalizar uma série de desvio zero")
        return (self - self.mean()) / desvio

    def reamostrar(self, k: int) -> SerieTemporal:
        """Médias de blocos consecutivos de `k` pontos: `len(self) // k` valores."""
        if k < 1 or k > len(self):
            raise ValueError(f"k deve estar entre 1 e {len(self)}; recebi {k}")
        n_blocos = len(self) // k
        limite = n_blocos * k
        troncado = self[:limite]
        blocos = troncado.reshape(n_blocos, k)
        medias = blocos.mean(axis=1)
        return SerieTemporal.de_lista(medias)
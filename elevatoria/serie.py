"""Séries temporais unidimensionais como subclasse de `numpy.ndarray`."""
from __future__ import annotations

from typing import Sequence

import numpy as np


class SerieTemporal(np.ndarray):
    """Série temporal unidimensional de `float`, com métodos de análise vetorizados.

    Crie instâncias com `SerieTemporal.de_lista(seq)`. Todos os métodos usam apenas
    operações do NumPy (sem laços sobre os elementos) e nenhum deles modifica `self`.
    """

    @classmethod
    def de_lista(cls, seq: Sequence[float]) -> SerieTemporal:
        """Cria uma `SerieTemporal` de `float` (uma cópia) a partir de qualquer sequência.

        Levanta `ValueError` se o resultado não for unidimensional.
        """
        arr = np.array(seq, dtype=float)
        if arr.ndim != 1:
            raise ValueError(f"a série deve ser unidimensional; recebi ndim={arr.ndim}")
        return arr.view(cls)

    def media_movel(self, janela: int) -> SerieTemporal:
        
        if janela < 1 or janela > len(self):
            raise ValueError(f"janela deve estar entre 1 e {len(self)}; recebi {janela}")
        acumulada = np.insert(np.cumsum(self), 0, 0.0)
        return SerieTemporal.de_lista(((acumulada[janela:] - acumulada[:-janela]) / janela).tolist())

    def variacao(self) -> SerieTemporal:
        """Diferenças entre pontos consecutivos (`n - 1` valores)."""
        return np.diff(self)

    def amplitude(self) -> float:
        """Máximo menos mínimo da série, como `float`."""
        return float(self.max() - self.min())

    def normalizar(self) -> SerieTemporal:
        """Série padronizada `(x - média) / desvio`, com desvio amostral (`ddof=1`).

        Levanta `ValueError` se o desvio for zero.
        """
        desvio = float(self.std(ddof=1))
        if desvio == 0.0:
            raise ValueError("não é possível normalizar uma série de desvio zero")
        return (self - self.mean()) / desvio

    def reamostrar(self, k: int) -> SerieTemporal:
    
        if k < 1 or k > len(self):
            raise ValueError(f"k deve estar entre 1 e {len(self)}; recebi {k}")
    
        blocos = int(len(self) // k)
        elementos = blocos * int(k)
        array = np.asarray(self)[:elementos]

        return SerieTemporal.de_lista(array.reshape(blocos, int(k)).mean(axis=1).tolist())
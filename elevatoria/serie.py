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
        """Médias de `janela` pontos consecutivos: `n - janela + 1` valores.

        O valor `i` do resultado é a média de `self[i : i + janela]`. Usa a soma acumulada
        (`np.cumsum`), sem laços. Levanta `ValueError` se `janela < 1` ou `janela > len(self)`.
        """
        if not isinstance(janela, int) or janela < 1 or janela > len(self):
            raise ValueError(f"janela deve ser um inteiro entre 1 e {len(self)}; recebi {janela}")
        acumulada = np.cumsum(np.insert(self, 0, 0.0))
        return SerieTemporal.de_lista((acumulada[janela:] - acumulada[:-janela]) / janela)

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
        """Devolve uma nova SerieTemporal com a média de blocos consecutivos de k pontos.

        Sobras no final do vetor que não completam um bloco de tamanho k são descartadas.
        Levanta ValueError se k não for um inteiro positivo ou se k > len(self).
        """
        if not isinstance(k, int) or k < 1 or k > len(self):
            raise ValueError(f"k deve ser um inteiro positivo e menor ou igual ao tamanho da série; recebi {k!r}")

        n_blocos = len(self) // k
        fatia = self[: n_blocos * k]
        medias = fatia.reshape(n_blocos, k).mean(axis=1)
        
        return SerieTemporal.de_lista(medias)

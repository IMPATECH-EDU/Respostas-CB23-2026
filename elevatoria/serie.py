"""Séries temporais unidimensionais como subclasse de `numpy.ndarray`."""
from __future__ import annotations

from typing import Sequence

import numpy as np


class SerieTemporal(np.ndarray):
    """Série temporal unidimensional de valores float.

    Crie instâncias com ``SerieTemporal.de_lista(seq)``. Os métodos usam operações
    vetorizadas do NumPy e não modificam ``self``.
    """

    @classmethod
    def de_lista(cls, seq: Sequence[float]) -> SerieTemporal:
        """Cria uma série temporal unidimensional a partir de uma sequência.

        Args:
            seq: Sequência de valores numéricos.

        Returns:
            Nova instância de ``SerieTemporal`` com dtype ``float``.

        Raises:
            ValueError: Se o resultado não for unidimensional.
        """
        arr = np.array(seq, dtype=float)
        if arr.ndim != 1:
            raise ValueError(f"a série deve ser unidimensional; recebi ndim={arr.ndim}")
        return arr.view(cls)

    def media_movel(self, janela: int) -> SerieTemporal:
        """Calcula a média móvel em janelas consecutivas.

        Args:
            janela: Tamanho da janela de média.

        Returns:
            Série com ``n - janela + 1`` valores, em que o elemento ``i`` é a média
            de ``self[i : i + janela]``.

        Raises:
            ValueError: Se ``janela < 1`` ou ``janela > len(self)``.
        """
        if janela < 1 or janela > len(self):
            raise ValueError(f"janela deve estar entre 1 e {len(self)}; recebi {janela}")
        
        acumulada = np.concatenate((np.zeros(1), np.cumsum(self)))
        
        ret = self.de_lista((acumulada[janela:] - acumulada[:-janela])/janela)
        return ret

    def variacao(self) -> SerieTemporal:
        """Calcula diferenças entre pontos consecutivos.

        Returns:
            Série com ``n - 1`` elementos contendo ``self[i+1] - self[i]``.
        """
        return np.diff(self)

    def amplitude(self) -> float:
        """Calcula a amplitude da série.

        Returns:
            Diferença entre o valor máximo e o valor mínimo da série.
        """
        return float(self.max() - self.min())

    def normalizar(self) -> SerieTemporal:
        """Padroniza a série com média zero e desvio padrão amostral unitário.

        Returns:
            Série normalizada pela fórmula ``(x - média) / desvio`` com
            ``ddof=1``.

        Raises:
            ValueError: Se o desvio padrão amostral for zero.
        """
        desvio = float(self.std(ddof=1))
        if desvio == 0.0:
            raise ValueError("não é possível normalizar uma série de desvio zero")
        return (self - self.mean()) / desvio

    def reamostrar(self, k: int) -> SerieTemporal:
        """Calcula médias de blocos consecutivos de tamanho ``k``.

        Args:
            k: Número de pontos por bloco.

        Returns:
            Série com ``len(self) // k`` médias de blocos consecutivos. Pontos
            finais que não completam um bloco são descartados.

        Raises:
            ValueError: Se ``k < 1`` ou ``k > len(self)``.
        """
        
        if (k < 1 or k > len(self)):
            raise(ValueError("k inválido."))
        
        matriz = self.copy()[:len(self) - len(self) % k]
        
        matriz.resize(len(matriz)//k, k)
        
        medias = np.mean(matriz, axis=1)
        
        return medias
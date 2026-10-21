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
        """Cria uma série unidimensional de ponto flutuante a partir de uma sequência.

        Args:
            seq: Sequência de valores conversíveis em `float`.

        Returns:
            Nova instância `SerieTemporal`; os dados são copiados para um array NumPy.

        Raises:
            ValueError: Se os valores não puderem ser convertidos para `float` ou se
                resultarem em array não unidimensional.
        """
        arr = np.array(seq, dtype=float)
        if arr.ndim != 1:
            raise ValueError(f"a série deve ser unidimensional; recebi ndim={arr.ndim}")
        return arr.view(cls)

    def media_movel(self, janela: int) -> SerieTemporal:
        """Calcula a média de cada janela consecutiva da série.

        Args:
            janela: Número de pontos em cada janela.

        Returns:
            `SerieTemporal` com `len(self) - janela + 1` valores; o elemento `i` é a média
            de `self[i : i + janela]`.

        Raises:
            ValueError: Se `janela` não for um inteiro entre 1 e o tamanho da série.
        """
        if not isinstance(janela, int) or janela < 1 or janela > len(self):
            raise ValueError(f"janela deve ser um inteiro entre 1 e {len(self)}; recebi {janela}")
        acumulada = np.cumsum(np.insert(self, 0, 0.0))
        return SerieTemporal.de_lista((acumulada[janela:] - acumulada[:-janela]) / janela)

    def variacao(self) -> SerieTemporal:
        """Calcula as diferenças entre cada par de pontos consecutivos.

        Returns:
            `SerieTemporal` de tamanho `max(len(self) - 1, 0)`, com `self[i + 1] - self[i]`.
        """
        return np.diff(self)

    def amplitude(self) -> float:
        """Calcula a diferença entre o maior e o menor valor da série.

        Returns:
            Amplitude da série como `float`.

        Raises:
            ValueError: Se a série estiver vazia.
        """
        return float(self.max() - self.min())

    def normalizar(self) -> SerieTemporal:
        """Padroniza a série usando a média e o desvio padrão amostral.

        Returns:
            Nova `SerieTemporal` com `(x - média) / desvio`, usando `ddof=1`.

        Raises:
            ValueError: Se o desvio padrão amostral for exatamente zero.
        """
        desvio = float(self.std(ddof=1))
        if desvio == 0.0:
            raise ValueError("não é possível normalizar uma série de desvio zero")
        return (self - self.mean()) / desvio

    def reamostrar(self, k: int) -> SerieTemporal:
        """Calcula as médias de blocos consecutivos e não sobrepostos.

        Args:
            k: Número de pontos por bloco.

        Returns:
            Nova `SerieTemporal` com a média de cada bloco completo. Pontos finais que não
            completam um bloco são descartados.

        Raises:
            ValueError: Se `k` não for um inteiro positivo ou for maior que o tamanho da série.
        """
        if not isinstance(k, int) or k < 1 or k > len(self):
            raise ValueError(f"k deve ser um inteiro positivo e menor ou igual ao tamanho da série; recebi {k!r}")

        n_blocos = len(self) // k
        fatia = self[: n_blocos * k]
        medias = fatia.reshape(n_blocos, k).mean(axis=1)
        
        return SerieTemporal.de_lista(medias)

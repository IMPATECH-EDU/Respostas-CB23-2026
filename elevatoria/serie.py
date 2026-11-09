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
        if janela < 1 or janela > len(self):
            raise ValueError(f"janela deve estar entre 1 e {len(self)}; recebi {janela}")
        
        # Insere 0.0 no início para incluir a primeira janela 
        # (do índice 0 a janela-1) na subtração vetorizada
        acumulada = np.cumsum(self)
        cum_zero = np.insert(acumulada, 0, 0.0)
        return ((cum_zero[janela:] - cum_zero[:-janela]) / janela).view(SerieTemporal)
        
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
        """Médias de blocos consecutivos de `k` pontos: `len(self) // k` valores.

        O bloco `j` é `self[j*k : (j+1)*k]`; os `len(self) % k` pontos finais que não
        completam um bloco são descartados. Usa `reshape`, sem laços. Levanta `ValueError`
        se `k < 1` ou `k > len(self)`.
        """
        if k < 1 or k > len(self):
            raise ValueError("k inválido")

        # Calculamos quantos elementos vamos ter ao todo (o que também nos fornece quantos sobram)
        n= k*(len(self)// k) 

        # Tendo n, podemos saber quantos elementos vão sobrar (será sempre l<k essa quantidade), e com isso retirar eles da coleção self
        elems=np.array(self[:n])

        # Agora vamos usar o método reshape para formarmos os (len(self)//k) blocos de tamanho k
        resul=elems.reshape((len(self)// k, k))

        # Por fim realizamos o cálculo da média de cada bloco com .mean(axis=1) [já que queremos 1 valor por linha]
        # e retornamos ele como uma SerieTemporal
        return SerieTemporal(resul.mean(axis=1))
        raise NotImplementedError("issue #5: reamostrar ainda não foi implementado")

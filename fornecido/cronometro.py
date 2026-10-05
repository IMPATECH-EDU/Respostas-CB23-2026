"""Medição de tempo de execução de funções (código fornecido; NÃO ALTERE)."""
from __future__ import annotations

import time
from typing import Any, Callable


def cronometrar(funcao: Callable[..., Any], *args: Any, k: int = 10) -> float:
    """Tempo médio, em segundos, de `k` execuções de `funcao(*args)`.

    Cada execução é medida isoladamente com `time.perf_counter()`. O valor devolvido por
    `funcao` é descartado. Levanta `ValueError` se `k` não for um inteiro positivo.
    """
    if not isinstance(k, int) or k < 1:
        raise ValueError(f"k deve ser um inteiro positivo; recebi {k!r}")
    total = 0.0
    for _ in range(k):
        inicio = time.perf_counter()
        funcao(*args)
        total += time.perf_counter() - inicio
    return total / k

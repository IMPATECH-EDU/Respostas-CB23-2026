from .AP_03_ordenacao import selection_sort, divide_and_conquer_sort, quick_sort

import random
import time
from collections.abc import Callable
from sys import setrecursionlimit


setrecursionlimit(10 ** 6)


def test_sorting_method(sort_function: Callable, l: list, qtd_tests: int = 50) -> float:
    t = time.perf_counter()
    for _ in range(qtd_tests):
        sort_function(l.copy())
    return (time.perf_counter() - t) / qtd_tests


def create_avg_test_case(n: int) -> list[int]:
    l = list(range(n))
    random.shuffle(l)
    return l


def create_worst_test_case(n: int) -> list[int]:
    """Somente o quick sort possui pior caso, os demais o pior é igual o médio.\n
    Conforme se observa na prática.\n
    Ademais, o pior caso do quick sort será, além desse, o caso que a lista está ordenada.
    """
    return list(reversed(range(n)))


if __name__ == '__main__':
    values = [500, 1000, 2000, 4000]
    qtd_tests = 50

    algorithms = {
        "Selection Sort": selection_sort,
        "Divide & Conquer Sort": divide_and_conquer_sort,
        "Quick Sort": quick_sort,
    }

    header = f"{'Algorithm':<22} | {'Case':<8} | {'N':<6} | {'Avg Time (s)':<12}"
    print(header)
    print("-" * len(header))

    for n in values:
        avg_case_list = create_avg_test_case(n)
        worst_case_list = create_worst_test_case(n)

        for name, func in algorithms.items():
            avg_time = test_sorting_method(func, avg_case_list, qtd_tests)
            print(f"{name:<22} | {'Average':<8} | {n:<6} | {avg_time:.6f}")

        for name, func in algorithms.items():
            worst_time = test_sorting_method(func, worst_case_list, qtd_tests)
            print(f"{name:<22} | {'Worst':<8} | {n:<6} | {worst_time:.6f}")

        print("-" * len(header))
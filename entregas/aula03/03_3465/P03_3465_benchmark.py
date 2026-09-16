from .AP_03_ordenacao import *

import random
import time
from abc import abstractmethod
from collections.abc import Callable
from sys import setrecursionlimit


setrecursionlimit(1000000)


class SortTester:
    def __init__(self, n_values: list[int], trials: int) -> None:
        self._n_values = n_values
        self._trials = trials

    @property
    @abstractmethod
    def _sort_function(self) -> Callable:
        raise NotImplementedError
        
    def _test_for_a_given_list(self, l: list) -> int:
        t = time.perf_counter_ns()
        for _ in range(self._trials):
            self._sort_function(l.copy())
        return (time.perf_counter_ns() - t) // self._trials
    
    def _test_cases(self, list_generator: Callable[[int], list]) -> list[int]:
        return [
            self._test_for_a_given_list(
                list_generator(n)
            ) for n in self._n_values
        ]
    
    def _create_avarage_case_list(self, n: int) -> list[int]:
        l = list(range(n))
        random.shuffle(l)
        return l

    def test_avarage_cases(self) -> list[int]:
        return self._test_cases(self._create_avarage_case_list)
    
    @abstractmethod
    def _create_worst_case_list(self, n: int) -> list[int]:
        raise NotImplementedError

    def test_worst_cases(self) -> list[int]:
        return self._test_cases(self._create_worst_case_list)


class SelectionSortTester(SortTester):
    @property
    def _sort_function(self) -> Callable:
        return selection_sort

    def _create_worst_case_list(self, n: int) -> list[int]:
        """Para o selection sort todo caso é o pior caso em O(n^2)
        """
        return list(range(n))
    

class MergeSortTester(SortTester):
    @property
    def _sort_function(self) -> Callable:
        return divide_and_conquer_sort

    def _create_worst_case_list(self, n: int) -> list[int]:
        """O caso médio e pior do merge sort são de mesma complexidade
        o que é feito é tentar aumentar o número de comparações para aumentar
        o tempo de execução.
        """
        def sep(l):
            return l if len(l) < 3 else sep(l[0::2]) + sep(l[1::2])
        
        return sep(list(range(n)))
    

class QuickSortTester(SortTester):
    @property
    def _sort_function(self) -> Callable:
        return quick_sort

    def _create_worst_case_list(self, n: int) -> list[int]:
        """Nesse caso o pivo escolhido sempre é desfavorável e leva à um número
        maior de comparações que gera o pior caso de O(n^2)
        """
        return list(range(n))
    

def print_formated_matrix(m: list[list]):
    columns_indents = [0 for _ in range(len(m[0]))]

    for l in m:
        for j, item in enumerate(l):
            columns_indents[j] = max(
            columns_indents[j],
            len(str(item))
        )
            
    for l in m:
        for j, item in enumerate(l):
            print(f'{item:>{columns_indents[j]}}', end=' ')
        print()


if __name__ == '__main__':
    n_values = tuple((1 << i) for i in range(8, 13))
    trials = 50

    testers = {
        'Selection Sort': SelectionSortTester(n_values, trials),
        'Merge Sort': MergeSortTester(n_values, trials),
        'Quick Sort': QuickSortTester(n_values, trials)
    }

    print("Avarage Cases")

    print_formated_matrix(
        [
            ['N Values'] + list(n_values),
            *(
                [name] + tester.test_avarage_cases() for name, tester in testers.items()
            )
        ]
    )

    print()

    print("Worst Cases")

    print_formated_matrix(
        [
            ['N Values'] + list(n_values),
            *(
                [name] + tester.test_worst_cases() for name, tester in testers.items()
            )
        ]
    )
    
import AulasPraticas.AP_03_ordenacao as ord
import random as rand
import time as time
import sys as sys

sys.setrecursionlimit(10000)

selection_sort_list = []
divide_and_conquer_sort_list = []
quick_sort_list = []

def random_list(n):
    L = []
    for _ in range(n):
        L.append(rand.randint(1, 10000))
    return L

def reverse_list(n):
    L = []
    for i in range(n, 0, -1):
        L.append(i*10 + rand.randint(0,10))
    return L

def ordered_list(n):
    L = []
    for i in range(n):
        L.append(i*10 + rand.randint(0,10))
    return L

def test_execution(n, k, test, list_gen):
    final_time =  0
    for _ in range(n):
        L = list_gen(k)
        start_time = time.perf_counter()
        test(L)
        end_time = time.perf_counter()

        final_time += end_time - start_time

    return final_time/n

def run_comparison(n, k, list_order):
    divide_and_conquer_sort_list.append(test_execution(n, k, ord.divide_and_conquer_sort, list_order))
    quick_sort_list.append(test_execution(n, k, ord.quick_sort, list_order))
    selection_sort_list.append(test_execution(n, k, ord.selection_sort, list_order))

def run_tests(n, k):
    run_comparison(n, k, random_list)
    run_comparison(n, k, ordered_list)
    run_comparison(n, k, reverse_list)

def print_table(k_values):
    algorithms = [
        ord.divide_and_conquer_sort,
        ord.quick_sort,
        ord.selection_sort
    ]

    algorithm_lists = [
        divide_and_conquer_sort_list,
        quick_sort_list,
        selection_sort_list
    ]

    list_generators = [
        random_list,
        reverse_list,
        ordered_list
    ]

    for i in range(len(k_values)):
        k = k_values[i]

        print(f"\nN = {k}")

        print(
            f"{'Algoritmo':<30}"
            f"{random_list.__name__:>20}"
            f"{reverse_list.__name__:>20}"
            f"{ordered_list.__name__:>20}"
        )

        for j in range(len(algorithms)):
            alg_name = algorithms[j].__name__
            results = algorithm_lists[j]

            # Cada k possui 3 resultados:
            # random, ordered, reverse
            base = i * 3

            random_time = results[base]
            ordered_time = results[base + 1]
            reverse_time = results[base + 2]

            print(
                f"{alg_name:<30}"
                f"{random_time:>20.10f}"
                f"{reverse_time:>20.10f}"
                f"{ordered_time:>20.10f}"
            )


k_values = [100, 500, 1000, 5000]

for k in k_values:
    run_tests(50, k)

print_table(k_values)

print()
import random
from time import perf_counter
from AP_03_ordenacao import selection_sort, divide_and_conquer_sort, quick_sort

def generate_random_list(n):
    return random.sample(range(1, n+1), k=n)

def generate_bad_list(n, backwards=True):
    r = range(1, n+1)
    if backwards:
        return list(reversed(r))
    return list(r)


def measure(n, sorting_algo, list_algo, k=50):
    tot = 0
    for _ in range(k):
        li = list_algo(n)
        start = perf_counter()
        sorting_algo(li)
        tot += perf_counter() - start
    return tot / k

def pretty_print(list_algo):
    res = f'N =\t\t{'\t'.join(map(str, choices))}\n'
    for i in range(len(algos)):
        res += f'{names[i]}:\t{'\t'.join(map(lambda x: f'{1000 * measure(x, algos[i], list_algo):.2f}', choices))}\tms\n'
    return res

algos = [selection_sort, divide_and_conquer_sort, quick_sort]

names = ['selection sort', 'merge sort', 'quick sort']
choices = [10, 50, 100, 500]
print('----------------------- Caso médio: -----------------------')
print(pretty_print(generate_random_list))
print('----------- Pior Caso (ordenada ao contrário): ------------')
print(pretty_print(generate_bad_list))

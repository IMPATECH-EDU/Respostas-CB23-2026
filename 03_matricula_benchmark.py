#!/usr/bin/env python3
"""Benchmark de algoritmos de ordenacao - Caso Medio vs Pior Caso.

Script da Atividade Pratica 03 da disciplina CB23 (Programacao 2).
Compara o tempo medio de execucao de selection_sort, divide_and_conquer_sort
(merge sort) e quick_sort para variados tamanhos de entrada N nos cenarios de
caso medio (dados aleatorios) e pior caso (dados inversamente ordenados).

Exemplos de uso:
    python3 03_matricula_benchmark.py
    python3 03_matricula_benchmark.py --K 10 --Ns 100 500 1000
"""

import argparse
import importlib.util
import random
import sys
import time
from pathlib import Path

import AulasPraticas.AP_03_ordenacao

sys.setrecursionlimit(max(10000, 6000))


spec = importlib.util.spec_from_file_location("ap_03_ordenacao", "AP-03-ordenacao.py")
ap3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ap3)
 

def average_case(n):
    """Cenario de caso medio: lista de inteiros aleatorios."""
    return [random.randint(0, 10 ** 6) for _ in range(n)]


def worst_case(n):
    """Cenario de pior caso: lista inversamente ordenada."""
    return list(range(n, 0, -1))


def run_benchmark(algorithm, data_gen, n, k):
    """Executa `algorithm` k vezes sobre instancias geradas por `data_gen(n)`.

    Returns:
        float: media aritmetica dos tempos medidos com time.perf_counter().
    """
    times = []
    for _ in range(k):
        data = data_gen(n)
        start = time.perf_counter()
        algorithm(data)
        times.append(time.perf_counter() - start)
    return sum(times) / len(times)


def format_table(results):
    """Formata a tabela de resultados usando apenas f-strings."""
    col1_w = 17
    col2_w = 10
    col3_w = 6
    col4_w = 16
    sep = (
        "+" + "-" * (col1_w + 2)
        + "+" + "-" * (col2_w + 2)
        + "+" + "-" * (col3_w + 2)
        + "+" + "-" * (col4_w + 2) + "+"
    )
    header = (
        f"| {'Algoritmo':<20}"
        f" | {'Cenario':<{col2_w}}"
        f" | {'N':>{col3_w}}"
        f" | {'Tempo medio (s)':>{col4_w}} |"
    )
    lines = [sep, header, sep]
    for algorithm, scenario, n, mean in results:
        lines.append(
            f"| {algorithm:<{col1_w}}"
            f" | {scenario:<{col2_w}}"
            f" | {n:>{col3_w}}"
            f" | {mean:>{col4_w}.6f} |"
        )
    lines.append(sep)
    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Benchmark de algoritmos de ordenacao (Caso Medio vs Pior Caso)."
    )
    parser.add_argument(
        "--K",
        type=int,
        default=50,
        help="numero de repeticoes por medicao (default: 50)",
    )
    parser.add_argument(
        "--Ns",
        type=int,
        nargs="+",
        default=[100, 500, 1000, 5000],
        help="tamanhos de entrada N a testar (default: 100 500 1000 5000)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    random.seed(42)
    

    algorithms = {
        "selection_sort": ap3.selection_sort,
        "merge_sort": ap3.divide_and_conquer_sort,
        "quick_sort": ap3.quick_sort,
    }
    scenarios = {
        "Medio": average_case,
        "Pior": worst_case,
    }

    sizes = sorted(args.Ns)
    print(f"Benchmark de ordenacao - K={args.K} repeticoes, N={sizes}")

    results = []
    for name, algorithm in algorithms.items():
        for scenario, data_gen in scenarios.items():
            for n in sizes:
                mean = run_benchmark(algorithm, data_gen, n, args.K)
                results.append((name, scenario, n, mean))

    print(format_table(results))
    print()


if __name__ == "__main__":
    main()

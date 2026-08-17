import random as rng
import AP_03_ordenacao as ords
import time
import sys
sys.setrecursionlimit(10000000)

ns = [100, 500, 1000, 5000]
sorts = [ords.selection_sort, ords.divide_and_conquer_sort, ords.quick_sort]
times = []

for N in ns:
    for func in sorts:
        med = 0
        for i in range(50):
            randList = [rng.randint(1, N) for _ in range(N)]
            start = time.perf_counter()
            func(randList)
            end = time.perf_counter()
            med += (end - start)
        times.append(med / 50)
        if func == ords.quick_sort:
            med = 0
            for i in range(50):
                randList = [rng.randint(1, N) for _ in range(N)]
                randList.sort()
                start = time.perf_counter()
                func(randList)
                end = time.perf_counter()
                med += (end - start)
            times.append(med / 50)


headers = ["Tipo de Sort", "N Médio", "N Pior", "Tempo Médio", "Tempo Pior"]
data = [
    ["Selection Sort", "θ(n²)", "O(n²)", times[0], times[0]],
    ["Merge Sort", "θ(n log(n))", "O(n log(n))", times[1], times[1]],
    ["Quick Sort", "θ(n log(n))", "O(n²)", times[2], times[3]]
]


all_rows = [headers] + [[str(item) for item in row] for row in data]

col_widths = [max(len(row[i]) for row in all_rows) for i in range(len(headers))]

row_template = " | ".join(f"{{:<{w}}}" for w in col_widths)
row_template = f"| {row_template} |"

divider = "-" * len(row_template.format(*headers))

print(divider)
print(row_template.format(*headers))
print(divider)
for row in data:
    print(row_template.format(*row))
print(divider)
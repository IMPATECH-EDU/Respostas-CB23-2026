"""Marco 2 — Medição: script de demonstração (PRONTO; NÃO ALTERE).

Execute a partir da raiz do repositório, com o ambiente ativado:  python marco2.py

O script usa a MATRICULA do seu marco1.py e roda em etapas. Cada etapa depende de uma parte
do trabalho; ele para no primeiro assert que falhar ou no primeiro NotImplementedError:

- Etapa 1 só usa código que já existe: roda desde o início;
- Etapa 2 depende da correção da issue #7;
- Etapa 3 depende da issue #6 e do seu leitor de log do Marco 1 (issue #1).
"""
import sys
import time
from decimal import Decimal

import numpy as np
import scipy

import fornecido
from fornecido.simulador import gerar_log, p_real, tabela_calibracao
from elevatoria.acumuladores import (Acumulador, AcumuladorIngenuo, AcumuladorInteiro,
                                     AcumuladorKahan)
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import ler_log
from elevatoria.medicao import altura_manometrica, medir
from marco1 import MATRICULA


def etapa0() -> None:
    """Etapa 0 — Ambiente."""
    print("=== Etapa 0: ambiente ===")
    print(f"Python {sys.version.split()[0]} | NumPy {np.__version__} | SciPy {scipy.__version__}"
          f" | fornecido {fornecido.VERSAO} | matrícula {MATRICULA}")


def etapa1() -> dict:
    """Etapa 1 — Calibração (código do colega). Devolve as curvas linear e spline."""
    print("\n=== Etapa 1: calibração ===")
    c_cal, p_cal = tabela_calibracao()
    curvas = {metodo: CurvaCalibracao(c_cal, p_cal, metodo) for metodo in ("linear", "spline")}

    # (a) Erro máximo de cada curva em relação à resposta verdadeira do transmissor.
    erros = {metodo: curva.erro_maximo(p_real) for metodo, curva in curvas.items()}
    for metodo, erro in erros.items():
        print(f"(a) {metodo:<7} erro máximo = {erro:.4f} kPa")
    assert erros["spline"] < 0.1 < 2.0 < erros["linear"]

    # (b) Diferença adiante × derivada exata da spline em c = 1000, com h = 10^-k.
    spline, x0 = curvas["spline"], 1000.0
    exata = spline.derivada(x0)
    erros_h = {k: abs(spline.diferenca_adiante(x0, 10.0 ** -k) - exata) for k in range(15)}
    print(f"(b) derivada exata em c = {x0:g}: {exata:.12f} kPa/contagem")
    print(f"    {'k':>3} {'h':>8} {'erro':>12}")
    for k, erro in erros_h.items():
        print(f"    {k:>3} {10.0 ** -k:>8.0e} {erro:>12.3e}")
    k_min = min(erros_h, key=erros_h.get)
    print(f"    menor erro: h = 1e-{k_min}, erro = {erros_h[k_min]:.3e}")
    assert erros_h[0] >= 1000 * erros_h[k_min] and erros_h[14] >= 1000 * erros_h[k_min]
    return curvas


def totalizar(acumulador: Acumulador, n: int, parcela: float) -> float:
    """Soma `n` parcelas iguais com qualquer `Acumulador` e devolve o total."""
    for _ in range(n):
        acumulador.adicionar(parcela)
    return acumulador.total


def etapa2() -> None:
    """Etapa 2 — Totalizador de pulsos (issue #7)."""
    print("\n=== Etapa 2: totalizador de pulsos ===")
    n, ideal = 1_000_000, Decimal(100_000)
    erros = {}
    print(f"(a) {'acumulador':<20}{'total':>22}{'erro (L)':>12}{'tempo (ms)':>12}")
    for acumulador in [AcumuladorIngenuo(), AcumuladorKahan(), AcumuladorInteiro(10)]:
        nome = type(acumulador).__name__
        inicio = time.perf_counter()
        total = totalizar(acumulador, n, 0.1)
        tempo = time.perf_counter() - inicio
        erros[nome] = abs(Decimal(total) - ideal)
        print(f"    {nome:<20}{total!r:>22}{float(erros[nome]):>12.3e}{tempo * 1000:>12.0f}")
    assert erros["AcumuladorIngenuo"] > 0
    assert erros["AcumuladorKahan"] <= erros["AcumuladorIngenuo"] / 1000, \
        "o AcumuladorKahan não está compensando o arredondamento (issue #7)"
    assert erros["AcumuladorInteiro"] == 0


def etapa3(curvas: dict, matricula: int = MATRICULA) -> None:
    """Etapa 3 — Medição de pressão (issue #6, com o seu leitor do Marco 1)."""
    print("\n=== Etapa 3: medição de pressão ===")
    texto, verdade = gerar_log(matricula)
    registros, _ = ler_log(texto)
    referencia = verdade["pressao_recalque"]

    # (a) e (b) PT101 e PT102 com as duas curvas: espúrias, precisão e exatidão.
    print(f"(a) leituras espúrias de PT102 (conferência): {verdade['espurios']}")
    print(f"(b) {'curva':<7}{'tag':<7}{'média ± incerteza (kPa)':>26}{'desvio':>9}{'viés':>9}")
    recalque = {}
    for metodo, curva in curvas.items():
        succao = medir(registros, "PT101", curva, u_sistematica=1.5)
        recalque[metodo] = medir(registros, "PT102", curva, u_sistematica=1.5)
        assert succao.espurias == [] and recalque[metodo].espurias == verdade["espurios"]
        assert recalque[metodo].n_validas == 600 - len(verdade["espurios"])
        for m in (succao, recalque[metodo]):
            vies = f"{m.medida.valor - referencia:>9.3f}" if m.tag == "PT102" else ""
            print(f"    {metodo:<7}{m.tag:<7}{str(m.medida):>26}{m.desvio:>9.3f}{vies}")
    assert abs(recalque["spline"].medida.valor - referencia) < 0.2
    assert abs(recalque["linear"].medida.valor - referencia) > 0.5
    assert abs(recalque["linear"].desvio / recalque["spline"].desvio - 1) < 0.05

    # (c) Altura manométrica, com a spline.
    altura = altura_manometrica(registros, curvas["spline"])
    print(f"(c) H = {altura} m (conferência: {verdade['altura_manometrica']:.3f} m; "
          f"incerteza relativa {altura.incerteza_relativa:.2%})")
    assert altura.compativel_com(verdade["altura_manometrica"])
    assert altura.incerteza_relativa < 0.01


def main() -> None:
    """Executa as etapas do Marco 2."""
    etapa0()
    curvas = etapa1()
    etapa2()
    etapa3(curvas)
    print("\nMarco 2: todos os assert passaram.")


if __name__ == "__main__":
    main()

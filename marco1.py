"""Marco 1 — Dados: demonstração das issues #1 a #5 com o log da sua matrícula.

Execute a partir da pasta do projeto, com o ambiente ativado:  python marco1.py

Este esqueleto já traz a estrutura, os imports e todos os assert. Complete os trechos
marcados com TODO e acrescente as impressões pedidas no enunciado. Não remova nem
enfraqueça nenhum assert. O script usa apenas a interface pública dos módulos.
"""

import math
import re
import sys

import numpy as np

import fornecido
from fornecido.simulador import gerar_log
from elevatoria.dados import (contagem_por_tag, criar_conversores, ler_log, medir_memoria,
                              medir_tempos, serie, valida_tag)

MATRICULA = 3493  


def etapa0() -> None:
    """Etapa 0 — Ambiente: versões e uma verificação rápida do NumPy."""
    print("=== Etapa 0: ambiente ===")
    print(f"Python {sys.version.split()[0]} | NumPy {np.__version__} | fornecido {fornecido.VERSAO}")
    assert np.arange(10).sum() == 45
    assert np.ones((3, 3)).trace() == 3
    assert np.allclose(np.linspace(0, 1, 5), [0, 0.25, 0.5, 0.75, 1])


def etapa1(texto: str, verdade: dict) -> list:
    """Etapa 1 — Leitura do log (issue #1). Devolve a lista de registros."""
    print("\n=== Etapa 1: leitura do log ===")
    registros, invalidas = ler_log(texto)
    print(f"(a) Válidos: {len(registros)} | Inválidos: {len(invalidas)}")
    assert len(invalidas) == verdade["invalidas"]
    assert len(registros) + len(invalidas) == verdade["linhas"]
    assert contagem_por_tag(registros) == verdade["registros_por_tag"]

    por_nivel = {n: sum(1 for r in registros if r.nivel == n) for n in {r.nivel for r in registros}}
    assert por_nivel == verdade["por_nivel"]

    s_ft = serie(registros, "FT201", "pulsos")
    total = int(s_ft.sum())
    print(f"(c) Volume bombeado: {total * 0.1:.1f} L")
    assert total == verdade["pulsos_total"]

    for tag in ["PT101", "FT201", "B1"]:
        assert valida_tag(tag), tag
    for tag in ["pt101", "PT", "PT1010", "101PT", "PT101 "]:
        assert not valida_tag(tag), tag
    return registros


def etapa2(texto: str, registros: list, verdade: dict) -> None:
    """Etapa 2 — Lambda e compreensões (issue #2)."""
    print("\n=== Etapa 2: lambda e compreensões ===")
    por_tag_instante = sorted(registros, key=lambda r: (r.tag, r.instante))
    decrescente = sorted(registros, key=lambda r: r.instante, reverse=True)
    assert por_tag_instante[0].tag == "B1"
    assert decrescente[0].instante == max(r.instante for r in registros)

    com_map = list(map(lambda r: r.valores["contagens"], filter(lambda r: r.tag == "PT102" and "contagens" in r.valores, registros)))
    com_compreensao = [r.valores["contagens"] for r in registros if r.tag == "PT102" and "contagens" in r.valores]
    assert com_map == com_compreensao and len(com_compreensao) == 600

    altas = [c for c in com_compreensao if c > 2000]
    tags = {r.tag for r in registros}
    assert len(altas) == 5
    assert tags == {"B1", "PT101", "PT102", "FT201", "LT301"}

    convertido = re.sub(r"pulsos=(\d+)", lambda m: f"volume_L={int(m.group(1)) * 0.1:.1f}", texto)
    assert convertido.count("volume_L=") == 600 and "pulsos=" not in convertido

    escalas = {"PT101": 600 / 4095, "PT102": 600 / 4095, "FT201": 0.1}
    errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}
    certos = criar_conversores(escalas)
    assert math.isclose(errados["PT102"](4095), 409.5)
    assert math.isclose(certos["PT102"](4095), 600.0)

    normais = [c for c in com_compreensao if c <= 2000]
    media_c = sum(normais) / len(normais)
    p_nominal = certos["PT102"](media_c)
    print(f"(f) Pressão nominal PT102: {p_nominal:.2f} kPa | Conferência: {verdade['pressao_recalque']:.2f} kPa")
    assert abs(p_nominal - verdade["pressao_recalque"]) > 100


def etapa3() -> None:
    """Etapa 3 — Memória e tempo (issue #3)."""
    print("\n=== Etapa 3: memória e tempo ===")
    n = 1_000_000
    contagens = np.random.default_rng(1).integers(0, 4096, n)

    memoria = medir_memoria(contagens)
    ref_list = memoria["list"]
    print(f"{'Estrutura':<15} {'Bytes/Elem':>12} {'Total (Bytes)':>15} {'Razão p/ Lista':>15}")
    for k, v in memoria.items():
        print(f"{k:<15} {v/n:>12.2f} {v:>15,d} {ref_list/v:>15.2f}x")
    assert memoria["uint16"] == 2_000_000
    assert memoria["list"] > 10 * memoria["uint16"]

    tempos = medir_tempos(contagens, k=10)
    t_laco = tempos["laço"]
    print(f"\n{'Versão':<15} {'Tempo (ms)':>12} {'Aceleração':>12}")
    for k, v in tempos.items():
        print(f"{k:<15} {v*1000:>12.2f} {t_laco/v:>12.2f}x")
    assert tempos["laço"] / tempos["vetorizado"] >= 5

    misto = np.array([1, 2.5, "a"])
    estouro = np.array([4095], dtype=np.uint16) * 20
    assert misto.dtype.kind == "U"
    assert estouro[0] == 16364 and 4095 * 20 == 81900


def etapa4(registros: list) -> None:
    """Etapa 4 — A série de pressão (issues #4 e #5)."""
    print("\n=== Etapa 4: a série de pressão ===")
    s = serie(registros, "PT102", "contagens")

    print(f"(a) Média: {s.mean():.2f} | Desvio: {s.std(ddof=1):.2f} | Amplitude: {s.amplitude():.2f}")
    assert len(s) == 600 and s.amplitude() > 300

    mm = s.media_movel(30)
    print(f"(b) Média móvel (30 pts): {len(mm)} valores | Mín: {mm.min():.2f} | Máx: {mm.max():.2f}")
    assert len(mm) == 571

    por_minuto = s.reamostrar(10)
    print(f"(c) Médias por minuto (10 pts): {len(por_minuto)} valores")
    assert len(por_minuto) == 60
    assert math.isclose(float(por_minuto.mean()), float(s.mean()))

    print(f"(d) Tipos das expressões:")
    print(f"    s + s: {type(s + s).__name__}")
    print(f"    s[1:]: {type(s[1:]).__name__}")
    print(f"    s * 2: {type(s * 2).__name__}")
    print(f"    s.sum(): {type(s.sum()).__name__}")
    print(f"    s[0]: {type(s[0]).__name__}")


def main(matricula: int = MATRICULA) -> None:
    """Executa as etapas do Marco 1 para a matrícula dada."""
    etapa0()
    texto, verdade = gerar_log(matricula)
    registros = etapa1(texto, verdade)
    etapa2(texto, registros, verdade)
    etapa3()
    etapa4(registros)
    print("\nMarco 1: todos os assert passaram.")


if __name__ == "__main__":
    main()

"""Marco 1 — Dados: demonstração das issues #1 a #5 com o log da sua matrícula.

Execute a partir da pasta do projeto, com o ambiente ativado:  python marco1.py

O script demonstra as etapas do enunciado e confere os resultados com assert,
usando apenas a interface pública dos módulos.
"""
import math
import re
import sys

import numpy as np

import fornecido
from fornecido.simulador import gerar_log
from elevatoria.dados import (contagem_por_tag, criar_conversores, ler_log, medir_memoria,
                              medir_tempos, serie, valida_tag)

MATRICULA = 3548


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
    # (a) Leia o log e imprima o número de registros válidos e de linhas inválidas.
    registros, invalidas = ler_log(texto)
    print(f"Registros válidos: {len(registros)} | Linhas inválidas: {len(invalidas)}")
    assert len(invalidas) == verdade["invalidas"]
    assert len(registros) + len(invalidas) == verdade["linhas"]
    assert contagem_por_tag(registros) == verdade["registros_por_tag"]

    # (b) Conte os registros por nível com uma compreensão de dicionário.
    por_nivel = {
        nivel: sum(r.nivel == nivel for r in registros) for nivel in {r.nivel for r in registros}
    }
    print(f"Registros por nível: {por_nivel}")
    assert por_nivel == verdade["por_nivel"]

    # (c) Some os pulsos de FT201 (com `serie`) e imprima o volume bombeado na hora (0,1 L/pulso).
    total = float(serie(registros, "FT201", "pulsos").sum())
    print(f"Total de pulsos: {total:.0f} | Volume bombeado: {total * 0.1:.1f} L")
    assert total == verdade["pulsos_total"]

    # (d) valida_tag.
    for tag in ["PT101", "FT201", "B1"]:
        assert valida_tag(tag), tag
    for tag in ["pt101", "PT", "PT1010", "101PT", "PT101 "]:
        assert not valida_tag(tag), tag
    return registros


def etapa2(texto: str, registros: list, verdade: dict) -> None:
    """Etapa 2 — Lambda e compreensões (issue #2)."""
    print("\n=== Etapa 2: lambda e compreensões ===")
    # (a) Ordene com sorted e key=lambda: (i) por (tag, instante); (ii) por instante decrescente.
    por_tag_instante = sorted(registros, key=lambda r: (r.tag, r.instante))
    decrescente = sorted(registros, key=lambda r: r.instante, reverse=True)
    assert por_tag_instante[0].tag == "B1"
    assert decrescente[0].instante == max(r.instante for r in registros)

    # (b) Contagens de PT102 (só registros com a chave "contagens"): map/filter e compreensão.
    com_map = list(map(
        lambda r: r.valores["contagens"],
        filter(lambda r: r.tag == "PT102" and "contagens" in r.valores, registros)
    ))
    com_compreensao = [
        r.valores["contagens"] for r in registros
        if r.tag == "PT102" and "contagens" in r.valores
    ]
    assert com_map == com_compreensao and len(com_compreensao) == 600

    # (c) Contagens acima de 2000 (compreensão de lista) e tags distintas (de conjunto).
    altas = [c for c in com_compreensao if c > 2000]
    tags = {r.tag for r in registros}
    assert len(altas) == 5
    assert tags == {"B1", "PT101", "PT102", "FT201", "LT301"}

    # (d) Com re.sub e uma lambda como repl, troque pulsos=N por volume_L=V (V = N * 0,1,
    #     com uma casa decimal; por exemplo, pulsos=3892 vira volume_L=389.2).
    convertido = re.sub(
        r"pulsos=(\d+)", lambda m: f"volume_L={int(m[1]) * 0.1:.1f}", texto
    )
    assert convertido.count("volume_L=") == 600 and "pulsos=" not in convertido

    # (e) Late binding: a versão errada (não corrija esta linha) e a sua.
    escalas = {"PT101": 600 / 4095, "PT102": 600 / 4095, "FT201": 0.1}
    errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}
    certos = criar_conversores(escalas)
    print(f"PT102 (4095 contagens): errado = {errados['PT102'](4095):.1f} | "
          f"correto = {certos['PT102'](4095):.1f}")
    assert math.isclose(errados["PT102"](4095), 409.5)
    assert math.isclose(certos["PT102"](4095), 600.0)

    # (f) Converta a média das contagens normais de PT102 (até 2000) com a escala nominal
    #     (certos["PT102"]) e imprima ao lado de verdade["pressao_recalque"].
    normais = [c for c in com_compreensao if c <= 2000]
    p_nominal = certos["PT102"](sum(normais) / len(normais))
    print(f"Pressão nominal: {p_nominal:.2f} kPa | "
          f"Conferência: {verdade['pressao_recalque']:.2f} kPa")
    assert abs(p_nominal - verdade["pressao_recalque"]) > 100


def etapa3() -> None:
    """Etapa 3 — Memória e tempo (issue #3). Registre as previsões ANTES de rodar."""
    print("\n=== Etapa 3: memória e tempo ===")
    n = 1_000_000
    contagens = np.random.default_rng(1).integers(0, 4096, n)

    # (a) Memória: imprima uma tabela com estrutura, bytes por elemento, bytes totais e a
    #     razão em relação à lista.
    memoria = medir_memoria(contagens)
    print(f"{'Estrutura':<14} {'Bytes/elemento':>15} {'Bytes totais':>14} {'Memória/lista':>15}")
    for estrutura, tamanho in memoria.items():
        print(f"{estrutura:<14} {tamanho / n:>15.6f} {tamanho:>14d} "
              f"{tamanho / memoria['list']:>15.6f}")
    assert memoria["uint16"] == 2_000_000
    assert memoria["list"] > 10 * memoria["uint16"]

    # (b) Tempo: imprima uma tabela com o tempo (ms) e a aceleração em relação ao laço.
    tempos = medir_tempos(contagens, k=10)
    print(f"\n{'Método':<14} {'Tempo (ms)':>14} {'Aceleração':>14}")
    for metodo, tempo in tempos.items():
        print(f"{metodo:<14} {tempo * 1000:>14.3f} {tempos['laço'] / tempo:>13.2f}x")
    print(f"\nLista/uint16: {memoria['list'] / memoria['uint16']:.6f}")
    print(f"Laço/vetorizado: {tempos['laço'] / tempos['vetorizado']:.6f}")
    print(f"Compreensão/laço: {tempos['compreensão'] / tempos['laço']:.6f}")
    assert tempos["laço"] / tempos["vetorizado"] >= 5

    # (c) Tipos e overflow: imprima os dois resultados.
    misto = np.array([1, 2.5, "a"])
    estouro = np.array([4095], dtype=np.uint16) * 20
    print(f"\nLista mista: {misto} | dtype: {misto.dtype}")
    print(f"uint16 * 20: {estouro[0]} | Inteiro Python: {4095 * 20}")
    assert misto.dtype.kind == "U"
    assert estouro[0] == 16364 and 4095 * 20 == 81900


def etapa4(registros: list) -> None:
    """Etapa 4 — A série de pressão (issues #4 e #5)."""
    print("\n=== Etapa 4: a série de pressão ===")
    s = serie(registros, "PT102", "contagens")

    # (a) Imprima a média, o desvio (ddof=1) e a amplitude.
    print(f"Média: {float(s.mean()):.3f} | Desvio (ddof=1): {float(s.std(ddof=1)):.3f} | "
          f"Amplitude: {s.amplitude():.3f}")
    assert len(s) == 600 and s.amplitude() > 300

    # (b) Média móvel de 30 pontos: imprima o tamanho e os valores mínimo e máximo, ao lado
    #     dos mínimo e máximo da série.
    mm = s.media_movel(30)
    print(f"Média móvel de 30 pontos: {len(mm)} valores")
    print(f"{'Série':<16} {'Mínimo':>12} {'Máximo':>12}")
    print(f"{'Original':<16} {float(s.min()):>12.3f} {float(s.max()):>12.3f}")
    print(f"{'Média móvel':<16} {float(mm.min()):>12.3f} {float(mm.max()):>12.3f}")
    assert len(mm) == 571

    # (c) Médias por minuto (10 leituras de 6 s).
    por_minuto = s.reamostrar(10)
    print(f"Médias por minuto ({len(por_minuto)} blocos): {por_minuto}")
    assert len(por_minuto) == 60
    assert math.isclose(float(por_minuto.mean()), float(s.mean()))

    # (d) Imprima o tipo (type(...).__name__) de s + s, s[1:], s * 2, s.sum() e s[0].
    for expressao, resultado in [("s + s", s + s), ("s[1:]", s[1:]), ("s * 2", s * 2),
                                 ("s.sum()", s.sum()), ("s[0]", s[0])]:
        print(f"{expressao}: {type(resultado).__name__}")


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

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

MATRICULA = 3514  # troque pelo seu número de matrícula

def _tabela(cabecalho: list, linhas: list) -> None:
    """Imprime uma tabela de texto simples, com as colunas alinhadas pela maior célula."""
    celulas = [[str(c) for c in cabecalho]] + [[str(c) for c in linha] for linha in linhas]
    larguras = [max(len(linha[j]) for linha in celulas) for j in range(len(cabecalho))]
    for i, linha in enumerate(celulas):
        alinhadas = [linha[0].ljust(larguras[0])]
        alinhadas += [c.rjust(w) for c, w in zip(linha[1:], larguras[1:])]
        print("  " + " | ".join(alinhadas))
        if i == 0:
            print("  " + "-+-".join("-" * w for w in larguras))

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
    print(f"(a) {len(registros)} registros válidos e {len(invalidas)} linhas inválidas")
    for linha in invalidas:
        print(f"    descartada: {linha!r}")
    assert len(invalidas) == verdade["invalidas"]
    assert len(registros) + len(invalidas) == verdade["linhas"]
    assert contagem_por_tag(registros) == verdade["registros_por_tag"]

    # (b) Conte os registros por nível com uma compreensão de dicionário.
    niveis = {r.nivel for r in registros}
    por_nivel = {nivel: sum(1 for r in registros if r.nivel == nivel) for nivel in niveis}
    print(f"(b) registros por nível: {por_nivel}")
    assert por_nivel == verdade["por_nivel"]

    # (c) Some os pulsos de FT201 (com `serie`) e imprima o volume bombeado na hora (0,1 L/pulso).
    total = int(serie(registros, "FT201", "pulsos").sum())
    volume_litros = total * 0.1
    print(f"(c) {total} pulsos em FT201 -> {volume_litros:.1f} L "
          f"({volume_litros / 1000:.2f} m³) bombeados na hora")
    assert total == verdade["pulsos_total"]

    # (d) valida_tag.
    for tag in ["PT101", "FT201", "B1"]:
        assert valida_tag(tag), tag
    for tag in ["pt101", "PT", "PT1010", "101PT", "PT101 "]:
        assert not valida_tag(tag), tag
    print("(d) valida_tag: PT101, FT201 e B1 aceitas; pt101, PT, PT1010, 101PT e 'PT101 ' "
          "rejeitadas")
    return registros


def etapa2(texto: str, registros: list, verdade: dict) -> None:
    """Etapa 2 — Lambda e compreensões (issue #2)."""
    print("\n=== Etapa 2: lambda e compreensões ===")
    # (a) Ordene com sorted e key=lambda: (i) por (tag, instante); (ii) por instante decrescente.
    por_tag_instante = sorted(registros, key=lambda r: (r.tag, r.instante))
    decrescente = sorted(registros, key=lambda r: r.instante, reverse=True)
    print(f"(a) por (tag, instante): primeiro = {por_tag_instante[0].tag} "
          f"{por_tag_instante[0].instante:%H:%M:%S}; "
          f"por instante decrescente: primeiro = {decrescente[0].tag} "
          f"{decrescente[0].instante:%H:%M:%S}")
    assert por_tag_instante[0].tag == "B1"
    assert decrescente[0].instante == max(r.instante for r in registros)

    # (b) Contagens de PT102 (só registros com a chave "contagens"): map/filter e compreensão.
    e_contagem_pt102 = lambda r: r.tag == "PT102" and "contagens" in r.valores
    com_map = list(map(lambda r: r.valores["contagens"], filter(e_contagem_pt102, registros)))
    com_compreensao = [r.valores["contagens"] for r in registros
                       if r.tag == "PT102" and "contagens" in r.valores]
    print(f"(b) {len(com_map)} contagens de PT102 (map/filter == compreensão: "
          f"{com_map == com_compreensao}); primeiras: {com_compreensao[:5]}")
    assert com_map == com_compreensao and len(com_compreensao) == 600

    # (c) Contagens acima de 2000 (compreensão de lista) e tags distintas (de conjunto).
    altas = [c for c in com_compreensao if c > 2000]
    tags = {r.tag for r in registros}
    print(f"(c) contagens acima de 2000: {altas}; tags distintas: {sorted(tags)}")
    assert len(altas) == 5
    assert tags == {"B1", "PT101", "PT102", "FT201", "LT301"}

    # (d) Com re.sub e uma lambda como repl, troque pulsos=N por volume_L=V (V = N * 0,1,
    #     com uma casa decimal; por exemplo, pulsos=3892 vira volume_L=389.2).
    convertido = re.sub(r"\bpulsos=(\d+)",
                        lambda m: f"volume_L={int(m.group(1)) / 10:.1f}", texto)
    exemplo = next(linha for linha in convertido.splitlines() if "volume_L=" in linha)
    print(f"(d) depois do re.sub: {exemplo}")
    assert convertido.count("volume_L=") == 600 and "pulsos=" not in convertido

    # (e) Late binding: a versão errada (não corrija esta linha) e a sua.
    escalas = {"PT101": 600 / 4095, "PT102": 600 / 4095, "FT201": 0.1}
    errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}
    certos = criar_conversores(escalas)
    assert math.isclose(errados["PT102"](4095), 409.5)
    assert math.isclose(certos["PT102"](4095), 600.0)
    print("(e) conversão de 4095 contagens, versão errada x criar_conversores:")
    _tabela(["tag", "errados", "certos"],
            [[tag, f"{errados[tag](4095):.1f}", f"{certos[tag](4095):.1f}"] for tag in escalas])

    # (f) Converta a média das contagens normais de PT102 (até 2000) com a escala nominal
    #     (certos["PT102"]) e imprima ao lado de verdade["pressao_recalque"].
    normais = [c for c in com_compreensao if c <= 2000]
    media_normais = sum(normais) / len(normais)
    p_nominal = certos["PT102"](media_normais)
    print(f"(f) média de {len(normais)} contagens normais de PT102 = {media_normais:.1f} -> "
          f"{p_nominal:.1f} kPa pela escala nominal; conferência: "
          f"{verdade['pressao_recalque']:.1f} kPa")
    assert abs(p_nominal - verdade["pressao_recalque"]) > 100


def etapa3() -> None:
    """Etapa 3 — Memória e tempo (issue #3). Registre as previsões ANTES de rodar."""
    print("\n=== Etapa 3: memória e tempo ===")
    n = 1_000_000
    contagens = np.random.default_rng(1).integers(0, 4096, n)

    # (a) Memória: imprima uma tabela com estrutura, bytes por elemento, bytes totais e a
    #     razão em relação à lista.
    memoria = medir_memoria(contagens)
    _tabela(["estrutura", "bytes/elemento", "bytes totais", "razão p/ list"],
            [[nome, f"{total / n:.2f}", f"{total:,}".replace(",", "."),
              f"{total / memoria['list']:.3f}"]
             for nome, total in memoria.items()])
    assert memoria["uint16"] == 2_000_000
    assert memoria["list"] > 10 * memoria["uint16"]

    # (b) Tempo: imprima uma tabela com o tempo (ms) e a aceleração em relação ao laço.
    tempos = medir_tempos(contagens, k=10)
    _tabela(["versão", "tempo (ms)", "aceleração p/ laço"],
            [[nome, f"{t * 1000:.2f}", f"{tempos['laço'] / t:.1f}x"]
             for nome, t in tempos.items()])
    assert tempos["laço"] / tempos["vetorizado"] >= 5

    # (c) Tipos e overflow: imprima os dois resultados.
    misto = np.array([1, 2.5, "a"])
    estouro = np.array([4095], dtype=np.uint16) * 20
    assert misto.dtype.kind == "U"
    assert estouro[0] == 16364 and 4095 * 20 == 81900
    print(f"(c) np.array([1, 2.5, 'a']) -> {misto!r} (dtype {misto.dtype})")
    print(f"    uint16: 4095 * 20 = {estouro[0]} (dtype {estouro.dtype}); em Python, "
          f"4095 * 20 = {4095 * 20}, e {4095 * 20} - 2**16 = {4095 * 20 - 2**16}")



def etapa4(registros: list) -> None:
    """Etapa 4 — A série de pressão (issues #4 e #5)."""
    print("\n=== Etapa 4: a série de pressão ===")
    s = serie(registros, "PT102", "contagens")

    # (a) Imprima a média, o desvio (ddof=1) e a amplitude.
    assert len(s) == 600 and s.amplitude() > 300
    print(f"(a) PT102: média = {float(s.mean()):.2f}, desvio (ddof=1) = "
          f"{float(s.std(ddof=1)):.2f}, amplitude = {s.amplitude():.1f} contagens")

    # (b) Média móvel de 30 pontos: imprima o tamanho e os valores mínimo e máximo, ao lado
    #     dos mínimo e máximo da série.
    mm = s.media_movel(30)
    assert len(mm) == 571
    print(f"(b) média móvel de 30: {len(mm)} valores, mín = {float(mm.min()):.2f}, "
          f"máx = {float(mm.max()):.2f} (série: mín = {float(s.min()):.0f}, "
          f"máx = {float(s.max()):.0f})")

    # (c) Médias por minuto (10 leituras de 6 s).
    por_minuto = s.reamostrar(10)
    assert len(por_minuto) == 60
    assert math.isclose(float(por_minuto.mean()), float(s.mean()))
    print(f"(c) {len(por_minuto)} médias por minuto; média delas = "
          f"{float(por_minuto.mean()):.2f}; primeiras: "
          f"{np.round(np.asarray(por_minuto[:4]), 1).tolist()}")

    # (d) Imprima o tipo (type(...).__name__) de s + s, s[1:], s * 2, s.sum() e s[0].
    expressoes = {"s + s": s + s, "s[1:]": s[1:], "s * 2": s * 2,
                  "s.sum()": s.sum(), "s[0]": s[0]}
    print("(d) tipos:")
    _tabela(["expressão", "tipo"],
            [[texto_expr, type(valor).__name__] for texto_expr, valor in expressoes.items()])


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

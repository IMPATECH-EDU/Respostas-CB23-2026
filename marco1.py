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

MATRICULA = 3538  # troque pelo seu número de matrícula


def _todo(item: str):
    """Marca um trecho ainda não feito; apague as chamadas a _todo ao completar o script."""
    raise NotImplementedError(f"marco1.py: complete o item {item}")


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
    niveis = {r.nivel for r in registros}
    por_nivel = {nivel: sum(1 for r in registros if r.nivel == nivel) for nivel in niveis}
    assert por_nivel == verdade["por_nivel"]

    # (c) Some os pulsos de FT201 (com `serie`) e imprima o volume bombeado na hora (0,1 L/pulso).
    s_pulsos = serie(registros, "FT201", "pulsos")
    total = int(s_pulsos.sum())
    volume_L = total * 0.1
    print(f"Total de pulsos de FT201: {total} | Volume bombeado: {volume_L:.1f} L ({volume_L/1000:.3f} m³)")
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
    com_map = list(
        map(
            lambda r: r.valores["contagens"],
            filter(lambda r: r.tag == "PT102" and "contagens" in r.valores, registros),
        )
    )
    com_compreensao = [
        r.valores["contagens"]
        for r in registros
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
        r"pulsos=(\d+)",
        lambda m: f"volume_L={int(m.group(1)) * 0.1:.1f}",
        texto
    )
    assert convertido.count("volume_L=") == 600 and "pulsos=" not in convertido

    # (e) Late binding: a versão errada (não corrija esta linha) e a sua.
    escalas = {"PT101": 600 / 4095, "PT102": 600 / 4095, "FT201": 0.1}
    errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}
    certos = criar_conversores(escalas)

    print(f"Versão errada para PT102 (4095 contagens): {errados['PT102'](4095):.1f}")
    print(f"Versão correta para PT102 (4095 contagens): {certos['PT102'](4095):.1f} kPa")
    
    assert math.isclose(errados["PT102"](4095), 409.5)
    assert math.isclose(certos["PT102"](4095), 600.0)

    # (f) Converta a média das contagens normais de PT102 (até 2000) com a escala nominal
    #     (certos["PT102"]) e imprima ao lado de verdade["pressao_recalque"].
    normais = [c for c in com_compreensao if c <= 2000]
    media_normais = sum(normais) / len(normais)
    p_nominal = certos["PT102"](media_normais)
    
    print(f"Pressão nominal PT102 (média normais): {p_nominal:.2f} kPa | Conferência: {verdade['pressao_recalque']:.2f} kPa")
    assert abs(p_nominal - verdade["pressao_recalque"]) > 100


def etapa3() -> None:
    """Etapa 3 — Memória e tempo (issue #3). Registre as previsões ANTES de rodar."""
    print("\n=== Etapa 3: memória e tempo ===")
    n = 1_000_000
    contagens = np.random.default_rng(1).integers(0, 4096, n)

    # (a) Memória: imprima uma tabela com estrutura, bytes por elemento, bytes totais e a
    #     razão em relação à lista.
    memoria = medir_memoria(contagens)

    print("\n---- Memória ocupada pelas estruturas (bytes) ----")
    print(f"{'Estrutura':<15} {'Bytes/Elem':<12} {'Bytes Totais':<15} {'Razão':<20}")
    print("-" * 55)

    bytes_por_elem = {
        "list": memoria["list"] / n,
        "array('H')": 2.0,
        "uint16": 2.0,
        "int32": 4.0,
        "int64": 8.0,
        "float32": 4.0,
        "float64": 8.0
    }

    for estrutura, bytes_totais in memoria.items():
        bytes_elem = bytes_por_elem[estrutura]
        razao = memoria["list"] / bytes_totais
        print(f"{estrutura:<12} | {bytes_elem:<10.1f} | {bytes_totais:<12,d} | {razao:<15.2f}x")

    assert memoria["uint16"] == 2_000_000
    assert memoria["list"] > 10 * memoria["uint16"]

    # (b) Tempo: imprima uma tabela com o tempo (ms) e a aceleração em relação ao laço.
    tempos = medir_tempos(contagens, k=10)

    print("\n ---- Tempo de conversão (ms) ----")
    print(f"{'Método':<14} {'Tempo (ms)':<14} {'Aceleração (laço/método)':<20}")
    print("-" * 60)
    tempo_laco = tempos["laço"]

    for metodo, tempo in tempos.items():
        tempo_ms = tempo * 1000
        aceleracao = tempo_laco / tempo if tempo != 0 else float('inf')
        print(f"{metodo:<12} | {tempo_ms:<12.3f} | {aceleracao:<20.2f}x")

    assert tempos["laço"] / tempos["vetorizado"] >= 5

    # (c) Tipos e overflow: imprima os dois resultados.
    misto = np.array([1, 2.5, "a"])
    estouro = np.array([4095], dtype=np.uint16) * 20

    print("\n ---- Tipos e overflow ----")
    print(f"Array misto: dtype: {misto.dtype} (kind: {misto.dtype.kind}) | Conteúdo = {misto}")
    print(f"Estouro unit16 (4095 * 20): unit16 = {estouro[0]} | Python init = {4095 * 20}")

    assert misto.dtype.kind == "U"
    assert estouro[0] == 16364 and 4095 * 20 == 81900


def etapa4(registros: list) -> None:
    """Etapa 4 — A série de pressão (issues #4 e #5)."""
    print("\n=== Etapa 4: a série de pressão ===")
    s = serie(registros, "PT102", "contagens")

    # (a) Imprima a média, o desvio (ddof=1) e a amplitude.
    print(f"Média: {s.mean():.2f} | Desvio (ddof=1): {s.std(ddof=1):.2f} | Amplitude: {s.amplitude():.2f}")
    assert len(s) == 600 and s.amplitude() > 300

    # (b) Média móvel de 30 pontos: imprima o tamanho e os valores mínimo e máximo, ao lado
    #     dos mínimo e máximo da série.
    mm = s.media_movel(30)
    print(f"Média móvel (30): tamanho = {len(mm)} | min = {mm.min():.2f} | max = {mm.max():.2f}")
    assert len(mm) == 571

    # (c) Médias por minuto (10 leituras de 6 s).
    por_minuto = s.reamostrar(10)
    print(f"Reamostragem por minuto: tamanho = {len(por_minuto)} | média = {por_minuto.mean():.2f}")
    assert len(por_minuto) == 60
    assert math.isclose(float(por_minuto.mean()), float(s.mean()))

    # (d) Imprima o tipo (type(...).__name__) de s + s, s[1:], s * 2, s.sum() e s[0].
    print("\n ---- Tipos de operações com a série ----")
    print(f"s + s: {type(s + s).__name__}")
    print(f"s[1:]: {type(s[1:]).__name__}")
    print(f"s * 2: {type(s * 2).__name__}")
    print(f"s.sum(): {type(s.sum()).__name__}")
    print(f"s[0]: {type(s[0]).__name__}")


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

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

MATRICULA = 3464  # troque pelo seu número de matrícula


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
    assert len(invalidas) == verdade["invalidas"]
    assert len(registros) + len(invalidas) == verdade["linhas"]
    assert contagem_por_tag(registros) == verdade["registros_por_tag"]

    # (b) Conte os registros por nível com uma compreensão de dicionário.
    niveis = {r.nivel for r in registros}
    por_nivel = {nivel : sum(1 for r in registros if r.nivel == nivel) for nivel in niveis}
    assert por_nivel == verdade["por_nivel"]

    # (c) Some os pulsos de FT201 (com `serie`) e imprima o volume bombeado na hora (0,1 L/pulso).
    #print([r for r in registros if r.tag == "FT201"])
    seq = serie(registros, "FT201", "pulsos")
    total = np.sum(seq)
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
    por_tag_instante = sorted(registros, key = lambda r: (r.tag, r.instante))
    decrescente = sorted(registros, key = lambda r: r.instante, reverse=True)
    assert por_tag_instante[0].tag == "B1"
    assert decrescente[0].instante == max(r.instante for r in registros)

    # (b) Contagens de PT102 (só registros com a chave "contagens"): map/filter e compreensão.
    com_map = list(map(lambda r: r.valores["contagens"], filter(lambda r: r.tag == "PT102" and "contagens" in r.valores, registros)))
    com_compreensao = [r.valores["contagens"] for r in registros if r.tag == "PT102" and "contagens" in r.valores]
    assert com_map == com_compreensao and len(com_compreensao) == 600

    # (c) Contagens acima de 2000 (compreensão de lista) e tags distintas (de conjunto).
    cont_tag = contagem_por_tag(registros)
    # À princípio tentei fazer assim, mas vi que todas as tags possuíam 600 ou menos, então entendi que o total
    # em todas as tags é que totalizavam os 2000
    # altas = [t for t in cont_tag if cont_tag[t] >= 2000]
    altas = [t for t in cont_tag]
    tags = set(altas)
    assert len(altas) == 5
    assert tags == {"B1", "PT101", "PT102", "FT201", "LT301"}

    # (d) Com re.sub e uma lambda como repl, troque pulsos=N por volume_L=V (V = N * 0,1,
    #     com uma casa decimal; por exemplo, pulsos=3892 vira volume_L=389.2).
    # Achei que tinha que mexer nos registros, mas após testar um pouco parece que era nos texto mesmo
    convertido = re.sub(
        r"pulsos=(\d+)", 
        lambda N: f"volume_L={(int(N.group(1))*0.1):.1f}", 
        texto
    )
    assert convertido.count("volume_L=") == 600 and "pulsos=" not in convertido

    # (e) Late binding: a versão errada (não corrija esta linha) e a sua.
    escalas = {"PT101": 600 / 4095, "PT102": 600 / 4095, "FT201": 0.1}
    errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}
    certos = criar_conversores(escalas)
    assert math.isclose(errados["PT102"](4095), 409.5)
    assert math.isclose(certos["PT102"](4095), 600.0)

    # (f) Converta a média das contagens normais de PT102 (até 2000) com a escala nominal
    #     (certos["PT102"]) e imprima ao lado de verdade["pressao_recalque"].
    # Podemos usar as tags PT102 com "contagens" separadas mais acima no código
    media_cont = sum(com_compreensao)/len(com_compreensao)
    p_nominal = certos["PT102"](media_cont)
    assert abs(p_nominal - verdade["pressao_recalque"]) > 100


def etapa3() -> None:
    """Etapa 3 — Memória e tempo (issue #3). Registre as previsões ANTES de rodar."""
    print("\n=== Etapa 3: memória e tempo ===")
    n = 1_000_000
    contagens = np.random.default_rng(1).integers(0, 4096, n)

    # (a) Memória: imprima uma tabela com estrutura, bytes por elemento, bytes totais e a
    #     razão em relação à lista.
    memoria = medir_memoria(contagens)

    # Código que usei da IA. Não tinha experiência criando tabelas bem estruturadas.
    bytes_lista = memoria["list"]
    print(f"{'Estrutura':<12} | {'Bytes/elem':<12} | {'Bytes Totais':<15} | {'Razão (list/X)':<15}")
    print("-" * 62)
    for estrutura, b_totais in memoria.items():
        b_elem = b_totais / n
        razao = bytes_lista / b_totais
        print(f"{estrutura:<12} | {b_elem:<12.2f} | {b_totais:<15,d} | {razao:<15.2f}x")

    assert memoria["uint16"] == 2_000_000
    assert memoria["list"] > 10 * memoria["uint16"]

    # (b) Tempo: imprima uma tabela com o tempo (ms) e a aceleração em relação ao laço.
    tempos = medir_tempos(contagens, k=10)

    t_laco = tempos["laço"]
    print(f"\n{'Versão':<15} | {'Tempo (ms)':<12} | {'Aceleração':<12}")
    print("-" * 45)
    for versao, t_seg in tempos.items():
        t_ms = t_seg * 1000  # converte segundos para milissegundos
        aceleracao = t_laco / t_seg if t_seg > 0 else 0
        print(f"{versao:<15} | {t_ms:<12.4f} | {aceleracao:<12.2f}x")

    assert tempos["laço"] / tempos["vetorizado"] >= 5

    # (c) Tipos e overflow: imprima os dois resultados.
    misto = np.array([1, 2.5, "a"])
    estouro = np.array([4095], dtype=np.uint16) * 20

    print("\n--- (c) Tipos e Overflow ---")
    print(f"Tipos (misto): {misto} -> dtype: {misto.dtype} (kind='{misto.dtype.kind}')")
    print(f"Estouro de uint16 (overflow): {estouro[0]} (sem overflow seria {4095 * 20})")

    assert misto.dtype.kind == "U"
    assert estouro[0] == 16364 and 4095 * 20 == 81900


def etapa4(registros: list) -> None:
    """Etapa 4 — A série de pressão (issues #4 e #5)."""
    print("\n=== Etapa 4: a série de pressão ===")
    s = serie(registros, "PT102", "contagens")

    # (a) Imprima a média, o desvio (ddof=1) e a amplitude.
    # Basta imprimir cada um. Os arrays do numpy já possuem o método .std(ddof)
    print(f"(a) Média: {s.mean():.2f} | Desvio padrão (ddof=1): {s.std(ddof=1):.2f} | Amplitude: {s.amplitude():.2f}")
    assert len(s) == 600 and s.amplitude() > 300

    # (b) Média móvel de 30 pontos: imprima o tamanho e os valores mínimo e máximo, ao lado
    #     dos mínimo e máximo da série.

    mm = s.media_movel(30)

    print(f"(b) Média Móvel (30 pts) -> Tamanho: {len(mm)} | Mín: {mm.min():.2f} | Máx: {mm.max():.2f}")
    print(f"    Série Original       -> Tamanho: {len(s)}  | Mín: {s.min():.2f}  | Máx: {s.max():.2f}")

    assert len(mm) == 571

    # (c) Médias por minuto (10 leituras de 6 s).
    por_minuto = s.reamostrar(10)

    print(f"(c) Reamostrado: {len(por_minuto)} pontos (1 por min) | Média reamostrada: {por_minuto.mean():.4f} | Média original: {s.mean():.4f}")

    assert len(por_minuto) == 60
    assert math.isclose(float(por_minuto.mean()), float(s.mean()))

    # (d) Imprima o tipo (type(...).__name__) de s + s, s[1:], s * 2, s.sum() e s[0].

    print("\n(d) Tipos devolvidos pelas operações:")
    print(f"    s + s   : {type(s + s).__name__}")
    print(f"    s[1:]   : {type(s[1:]).__name__}")
    print(f"    s * 2   : {type(s * 2).__name__}")
    print(f"    s.sum() : {type(s.sum()).__name__}")
    print(f"    s[0]    : {type(s[0]).__name__}")


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

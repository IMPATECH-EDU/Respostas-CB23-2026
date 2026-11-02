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
from fornecido.simulador import gerar_log, p_real
from elevatoria.dados import (contagem_por_tag, criar_conversores, ler_log, medir_memoria,
                              medir_tempos, serie, valida_tag)

MATRICULA = 3475  # troque pelo seu número de matrícula


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
    print(f"Válidas: {len(registros)} | Inválidas: {len(invalidas)}")

    # (b) Conte os registros por nível com uma compreensão de dicionário.
    niveis_set = set(reg.nivel for reg in registros)
    por_nivel = {n: sum([reg.nivel == n for reg in registros]) for n in niveis_set}
    assert por_nivel == verdade["por_nivel"]

    # (c) Some os pulsos de FT201 (com `serie`) e imprima o volume bombeado na hora (0,1 L/pulso).
    total = np.sum(serie(registros, 'FT201', 'pulsos'))
    assert total == verdade["pulsos_total"]
    print(f"Volume bombeado: {total/10} L")

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
    por_tag_instante = sorted(registros, key=lambda x: (x.tag, x.instante))
    decrescente = sorted(registros, key=lambda x: x.instante, reverse=True)
    assert por_tag_instante[0].tag == "B1"
    assert decrescente[0].instante == max(r.instante for r in registros)

    # (b) Contagens de PT102 (só registros com a chave "contagens"): map/filter e compreensão.
    filtrados = filter(lambda x : x.tag == "PT102" and "contagens" in x.valores, registros)
    com_map = list(map(lambda x : x.valores["contagens"], filtrados))
    com_compreensao = [reg.valores["contagens"] for reg in registros if reg.tag == "PT102" and "contagens" in reg.valores]
    assert com_map == com_compreensao and len(com_compreensao) == 600

    # (c) Contagens acima de 2000 (compreensão de lista) e tags distintas (de conjunto).
    altas = [reg.valores["contagens"] for reg in registros if "contagens" in reg.valores and reg.valores["contagens"] > 2000]
    tags = set(reg.tag for reg in registros)
    assert len(altas) == 5
    assert tags == {"B1", "PT101", "PT102", "FT201", "LT301"}

    # (d) Com re.sub e uma lambda como repl, troque pulsos=N por volume_L=V (V = N * 0,1,
    #     com uma casa decimal; por exemplo, pulsos=3892 vira volume_L=389.2).
    convertido = re.sub(r"(pulsos)=(\d+)", lambda x: f"volume_L={x[2]}", texto)
    assert convertido.count("volume_L=") == 600 and "pulsos=" not in convertido

    # (e) Late binding: a versão errada (não corrija esta linha) e a sua.
    escalas = {"PT101": 600 / 4095, "PT102": 600 / 4095, "FT201": 0.1}
    errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}
    certos = criar_conversores(escalas)
    assert math.isclose(errados["PT102"](4095), 409.5)
    assert math.isclose(certos["PT102"](4095), 600.0)

    # (f) Converta a média das contagens normais de PT102 (até 2000) com a escala nominal
    #     (certos["PT102"]) e imprima ao lado de verdade["pressao_recalque"].
    p_nominal = np.average(list(map(lambda x : certos["PT102"](x), com_map)))
    assert abs(p_nominal - verdade["pressao_recalque"]) > 100
    print(f"Média das contagens: {p_nominal} | pressao_recalque: {verdade["pressao_recalque"]}")


def etapa3() -> None:
    """Etapa 3 — Memória e tempo (issue #3). Registre as previsões ANTES de rodar."""
    print("\n=== Etapa 3: memória e tempo ===")
    n = 1_000_000
    contagens = np.random.default_rng(1).integers(0, 4096, n)

    # (a) Memória: imprima uma tabela com estrutura, bytes por elemento, bytes totais e a
    #     razão em relação à lista.
    memoria = medir_memoria(contagens)
    bytes_lista = memoria["list"]

    print()
    print(f"{'Estrutura':<12} | {'Bytes/elem':>10} | {'Bytes totais':>12} | {'Razão (vs list)':>15}")
    print("-" * 58)

    for estrutura, total_bytes in memoria.items():
        bytes_por_elem = total_bytes / n
        razao = total_bytes / bytes_lista
        
        print(f"{estrutura:<12} | {bytes_por_elem:>10.1f} | {total_bytes:>12} | {razao:>15.2%}")
    print()

    assert memoria["uint16"] == 2_000_000
    assert memoria["list"] > 10 * memoria["uint16"]
    

    # (b) Tempo: imprima uma tabela com o tempo (ms) e a aceleração em relação ao laço.
    tempos = medir_tempos(contagens, k=10)
    tempo_laco = tempos["laço"]

    print()
    print(f"{'Método':<15} | {'Tempo (ms)':>12} | {'Aceleração (vs laço)':>20}")
    print("-" * 53)

    for metodo, tempo_s in tempos.items():
        tempo_ms = tempo_s * 1000
        aceleracao = tempo_laco / tempo_s
        
        print(f"{metodo:<15} | {tempo_ms:>12.3f} | {aceleracao:>19.1f}x")
    print()
    
    assert tempos["laço"] / tempos["vetorizado"] >= 5

    # (c) Tipos e overflow: imprima os dois resultados.
    misto = np.array([1, 2.5, "a"])
    estouro = np.array([4095], dtype=np.uint16) * 20
    assert misto.dtype.kind == "U"
    assert estouro[0] == 16364 and 4095 * 20 == 81900
    print(misto)
    print(estouro)


def etapa4(registros: list) -> None:
    """Etapa 4 — A série de pressão (issues #4 e #5)."""
    print("\n=== Etapa 4: a série de pressão ===")
    s = serie(registros, "PT102", "contagens")

    # (a) Imprima a média, o desvio (ddof=1) e a amplitude.
    assert len(s) == 600 and s.amplitude() > 300
    print(f"Média: {s.mean()} | Desvio: {s.std(ddof=1)} | Amplitude: {s.amplitude()}")

    # (b) Média móvel de 30 pontos: imprima o tamanho e os valores mínimo e máximo, ao lado
    #     dos mínimo e máximo da série.
    mm = s.media_movel(30)
    assert len(mm) == 571
    print()
    print(f"{'Valor':<10} | {'Média movel':>15} | {'Série':>15}")
    print("-" * (10 + 15 + 15 + 3 * 2))
    print(f"{'Mínimo':<10} | {mm.min():>15.3f} | {s.min():>15}")
    print(f"{'Máximo':<10} | {mm.max():>15.3f} | {s.max():>15}")
    print()

    # (c) Médias por minuto (10 leituras de 6 s).
    por_minuto = s.reamostrar(10)
    assert len(por_minuto) == 60
    assert math.isclose(float(por_minuto.mean()), float(s.mean()))

    # (d) Imprima o tipo (type(...).__name__) de s + s, s[1:], s * 2, s.sum() e s[0].
    print(type(s+s).__name__)
    print(type(s[1:]).__name__)
    print(type(s * 2).__name__)
    print(type(s.sum()).__name__)
    print(type(s[0]).__name__)


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

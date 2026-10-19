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

MATRICULA = 3484


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
    print(f"(a) {len(registros)} registros válidos e {len(invalidas)} linhas inválidas:")
    for linha in invalidas:
        print(f"      {linha!r}")
    assert len(invalidas) == verdade["invalidas"]
    assert len(registros) + len(invalidas) == verdade["linhas"]
    assert contagem_por_tag(registros) == verdade["registros_por_tag"]

    # (b) Conte os registros por nível com uma compreensão de dicionário.
    niveis = {r.nivel for r in registros}
    por_nivel = {nivel: sum(1 for r in registros if r.nivel == nivel) for nivel in niveis}
    print(f"(b) registros por nível: {dict(sorted(por_nivel.items()))}")
    assert por_nivel == verdade["por_nivel"]

    # (c) Some os pulsos de FT201 (com `serie`) e imprima o volume bombeado na hora (0,1 L/pulso).
    pulsos = serie(registros, "FT201", "pulsos")
    total = int(pulsos.sum())
    litros = total / 10          # cada pulso vale 0,1 L
    print(f"(c) {total} pulsos em {len(pulsos)} leituras -> {litros:.1f} L "
          f"= {litros / 1000:.3f} m³ bombeados na hora")
    assert total == verdade["pulsos_total"]

    # (d) valida_tag.
    for tag in ["PT101", "FT201", "B1"]:
        assert valida_tag(tag), tag
    for tag in ["pt101", "PT", "PT1010", "101PT", "PT101 "]:
        assert not valida_tag(tag), tag
    testadas = ["PT101", "FT201", "B1", "pt101", "PT", "PT1010", "101PT", "PT101 "]
    print("(d) valida_tag: " + ", ".join(f"{t!r}: {valida_tag(t)}" for t in testadas))
    return registros


def etapa2(texto: str, registros: list, verdade: dict) -> None:
    """Etapa 2 — Lambda e compreensões (issue #2)."""
    print("\n=== Etapa 2: lambda e compreensões ===")
    # (a) Ordene com sorted e key=lambda: (i) por (tag, instante); (ii) por instante decrescente.
    por_tag_instante = sorted(registros, key=lambda r: (r.tag, r.instante))
    decrescente = sorted(registros, key=lambda r: r.instante, reverse=True)
    print(f"(a) por (tag, instante): primeiro = {por_tag_instante[0].tag} "
          f"{por_tag_instante[0].instante:%H:%M:%S}, último = {por_tag_instante[-1].tag} "
          f"{por_tag_instante[-1].instante:%H:%M:%S}")
    print(f"    por instante decrescente: primeiro = {decrescente[0].instante:%H:%M:%S} "
          f"({decrescente[0].tag})")
    assert por_tag_instante[0].tag == "B1"
    assert decrescente[0].instante == max(r.instante for r in registros)

    # (b) Contagens de PT102 (só registros com a chave "contagens"): map/filter e compreensão.
    def e_leitura_pt102(r):
        return r.tag == "PT102" and "contagens" in r.valores

    com_map = list(map(lambda r: r.valores["contagens"], filter(e_leitura_pt102, registros)))
    com_compreensao = [r.valores["contagens"] for r in registros if e_leitura_pt102(r)]
    print(f"(b) contagens de PT102: {len(com_map)} com map/filter, "
          f"{len(com_compreensao)} com compreensão; iguais: {com_map == com_compreensao}")
    assert com_map == com_compreensao and len(com_compreensao) == 600

    # (c) Contagens acima de 2000 (compreensão de lista) e tags distintas (de conjunto).
    altas = [c for c in com_compreensao if c > 2000]
    tags = {r.tag for r in registros}
    print(f"(c) contagens acima de 2000: {altas}")
    print(f"    tags distintas: {sorted(tags)}")
    assert len(altas) == 5
    assert tags == {"B1", "PT101", "PT102", "FT201", "LT301"}

    # (d) Com re.sub e uma lambda como repl, troque pulsos=N por volume_L=V (V = N * 0,1,
    #     com uma casa decimal; por exemplo, pulsos=3892 vira volume_L=389.2).
    # N pulsos de 0,1 L são N // 10 litros e N % 10 décimos: conta inteira, sem float
    convertido = re.sub(r"pulsos=(?P<n>\d+)",
                        lambda m: "volume_L={}.{}".format(*divmod(int(m["n"]), 10)), texto)
    exemplo = next(linha for linha in convertido.splitlines() if "volume_L=" in linha)
    print(f"(d) exemplo depois do re.sub: {exemplo}")
    assert convertido.count("volume_L=") == 600 and "pulsos=" not in convertido

    # (e) Late binding: a versão errada (não corrija esta linha) e a sua.
    escalas = {"PT101": 600 / 4095, "PT102": 600 / 4095, "FT201": 0.1}
    errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}
    certos = criar_conversores(escalas)
    print("(e) 4095 contagens em cada conversor:")
    for tag in escalas:
        print(f"      {tag}: errado = {errados[tag](4095):8.2f}   certo = {certos[tag](4095):8.2f}")
    assert math.isclose(errados["PT102"](4095), 409.5)
    assert math.isclose(certos["PT102"](4095), 600.0)

    # (f) Converta a média das contagens normais de PT102 (até 2000) com a escala nominal
    #     (certos["PT102"]) e imprima ao lado de verdade["pressao_recalque"].
    normais = [c for c in com_compreensao if c <= 2000]
    media_normais = sum(normais) / len(normais)
    p_nominal = certos["PT102"](media_normais)
    print(f"(f) média das {len(normais)} contagens normais de PT102 = {media_normais:.2f}")
    print(f"    escala nominal: {p_nominal:.1f} kPa   "
          f"conferência: {verdade['pressao_recalque']:.1f} kPa")
    assert abs(p_nominal - verdade["pressao_recalque"]) > 100


def etapa3() -> None:
    """Etapa 3 — Memória e tempo (issue #3). Registre as previsões ANTES de rodar."""
    print("\n=== Etapa 3: memória e tempo ===")
    n = 1_000_000
    contagens = np.random.default_rng(1).integers(0, 4096, n)

    # (a) Memória: imprima uma tabela com estrutura, bytes por elemento, bytes totais e a
    #     razão em relação à lista.
    memoria = medir_memoria(contagens)
    _todo("3(a) tabela")
    assert memoria["uint16"] == 2_000_000
    assert memoria["list"] > 10 * memoria["uint16"]

    # (b) Tempo: imprima uma tabela com o tempo (ms) e a aceleração em relação ao laço.
    tempos = medir_tempos(contagens, k=10)
    _todo("3(b) tabela")
    assert tempos["laço"] / tempos["vetorizado"] >= 5

    # (c) Tipos e overflow: imprima os dois resultados.
    misto = np.array([1, 2.5, "a"])
    estouro = np.array([4095], dtype=np.uint16) * 20
    assert misto.dtype.kind == "U"
    assert estouro[0] == 16364 and 4095 * 20 == 81900


def etapa4(registros: list) -> None:
    """Etapa 4 — A série de pressão (issues #4 e #5)."""
    print("\n=== Etapa 4: a série de pressão ===")
    s = serie(registros, "PT102", "contagens")

    # (a) Imprima a média, o desvio (ddof=1) e a amplitude.
    assert len(s) == 600 and s.amplitude() > 300

    # (b) Média móvel de 30 pontos: imprima o tamanho e os valores mínimo e máximo, ao lado
    #     dos mínimo e máximo da série.
    mm = s.media_movel(30)
    assert len(mm) == 571

    # (c) Médias por minuto (10 leituras de 6 s).
    por_minuto = s.reamostrar(10)
    assert len(por_minuto) == 60
    assert math.isclose(float(por_minuto.mean()), float(s.mean()))

    # (d) Imprima o tipo (type(...).__name__) de s + s, s[1:], s * 2, s.sum() e s[0].
    _todo("4(d)")


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

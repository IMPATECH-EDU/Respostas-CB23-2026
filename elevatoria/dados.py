"""Leitura do log SCADA da estação elevatória e preparação dos dados.

Este módulo é a porta de entrada da aplicação: transforma o texto do log em registros
estruturados e em séries numéricas. As funções marcadas com `NotImplementedError` são as
issues abertas do Marco 1; as docstrings descrevem o contrato que cada uma deve cumprir.
Não mude nomes nem assinaturas públicas: outros módulos e os testes dependem deles.
"""
from __future__ import annotations

import array
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

import numpy as np

from elevatoria.serie import SerieTemporal
from fornecido.cronometro import cronometrar

# ---------------------------------------------------------------------------------------
# Issue #1: leitor do log
# ---------------------------------------------------------------------------------------


# Padrão LINHA com re.VERBOSE e grupos nomeados exigidos (data, hora, nivel, tag, resto)
LINHA = re.compile(
    r"""
    ^
    (?P<data>\d{4}-\d{2}-\d{2})    # Data no formato YYYY-MM-DD
    \s+
    (?P<hora>\d{2}:\d{2}:\d{2})    # Hora no formato HH:MM:SS
    \s+
    (?P<nivel>INFO|WARN|ALARME)    # Nível do log SCADA
    \s+
    (?P<tag>[A-Za-z0-9_]+)         # Identificador da tag
    \s+
    (?P<resto>.*)                  # Pares chave=valor restantes
    $
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class Registro:
    """Uma linha válida do log: instante, nível, tag e os pares chave=valor convertidos."""

    instante: datetime
    nivel: str
    tag: str
    valores: dict[str, float | str]


def valida_tag(tag: str) -> bool:
    """Verifica se a string é uma tag válida (1 a 2 letras maiúsculas e 1 a 3 dígitos)."""
    return bool(re.fullmatch(r"[A-Z]{1,2}\d{1,3}", tag))


def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Lê o texto do log e devolve os registros válidos e a lista de linhas inválidas."""
    registros = []
    invalidas = []

    if not texto.strip():
        return registros, invalidas

    for linha in texto.splitlines():
        m = LINHA.fullmatch(linha)
        if not m or not valida_tag(m["tag"]):
            invalidas.append(linha)
            continue

        instante = datetime.strptime(f"{m['data']} {m['hora']}", "%Y-%m-%d %H:%M:%S")

        valores = {}
        if m["resto"].strip():
            for item in m["resto"].split():
                if "=" in item:
                    chave, val_str = item.split("=", 1)
                    try:
                        valores[chave] = float(val_str)
                    except ValueError:
                        valores[chave] = val_str

        registros.append(
            Registro(
                instante=instante,
                nivel=m["nivel"],
                tag=m["tag"],
                valores=valores,
            )
        )

    return registros, invalidas


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Conta os registros por tag usando compreensão de dicionário sobre um conjunto."""
    tags = {r.tag for r in registros}
    return {tag: sum(1 for r in registros if r.tag == tag) for tag in tags}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """Extrai os valores de uma chave para a tag especificada e retorna uma SerieTemporal."""
    valores = [
        r.valores[chave]
        for r in registros
        if r.tag == tag and chave in r.valores
    ]
    return SerieTemporal.de_lista(valores)


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Devolve um dicionário {tag: função} onde cada função multiplica a contagem pelo fator da própria tag.
    
    Evita o late binding definindo f=fator como argumento padrão na lambda.
    """
    return {tag: (lambda c, f=fator: c * f) for tag, fator in escalas.items()}


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Bytes ocupados pelas `contagens` (ndarray 1D de inteiros de 0 a 4095) em cada estrutura.

    Devolve um dicionário com exatamente estas chaves:

    - `"list"`: a lista `contagens.tolist()`; o total é `sys.getsizeof(lista)` mais a soma de
      `sys.getsizeof(x)` para cada elemento `x`;
    - `"array('H')"`: um `array.array("H", ...)`; conte só os dados (`itemsize * len`);
    - `"uint16"`, `"int32"`, `"int64"`, `"float32"`, `"float64"`: o `ndarray` convertido para
      esse `dtype`; conte só os dados (atributo `.nbytes`).

    Levanta `ValueError` se `contagens` não for um ndarray 1D de inteiros.
    """
    raise NotImplementedError("issue #3: medir_memoria")


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    raise NotImplementedError("issue #3: converter_laco")


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    raise NotImplementedError("issue #3: converter_compreensao")


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    raise NotImplementedError("issue #3: converter_map")


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    raise NotImplementedError("issue #3: converter_vetorizado")


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).
    """
    raise NotImplementedError("issue #3: medir_tempos")

"""Leitura do log SCADA da estação elevatória e preparação dos dados.

Este módulo é a porta de entrada da aplicação: transforma o texto do log em registros
estruturados e em séries numéricas.
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

#: Padrão de uma linha válida do log, compilado com `re.compile(..., re.VERBOSE)`
LINHA: re.Pattern = re.compile(
    r"""
    ^(?P<data>\d{4}-\d{2}-\d{2})        # Data no formato AAAA-MM-DD
    \s+                                 # Separador de espaço
    (?P<hora>\d{2}:\d{2}:\d{2})         # Hora no formato HH:MM:SS
    \s+                                 # Separador de espaço
    (?P<nivel>INFO|WARN|ALARME)         # Nível de log
    \s+                                 # Separador de espaço
    (?P<tag>[A-Z]{1,2}\d{1,3})          # Tag: 1-2 letras maiúsculas e 1-3 dígitos
    (?:\s+(?P<resto>\S.*))?             # Restante da linha com pares chave=valor
    $
    """,
    re.VERBOSE,
)

PADRAO_TAG: re.Pattern = re.compile(r"^[A-Z]{1,2}\d{1,3}$")
PARES_RE: re.Pattern = re.compile(r"(\w+)=(\S+)")


@dataclass(frozen=True)
class Registro:
    """Uma linha válida do log: instante, nível, tag e os pares chave=valor convertidos."""

    instante: datetime
    nivel: str
    tag: str
    valores: dict[str, float | str]


def valida_tag(s: str) -> bool:
    """`True` se a string inteira for uma tag válida (1 ou 2 maiúsculas e 1 a 3 dígitos)."""
    return bool(PADRAO_TAG.fullmatch(s))


def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Lê o texto do log e devolve `(registros, invalidas)`."""
    registros: list[Registro] = []
    invalidas: list[str] = []

    if not texto:
        return [], []

    for linha in texto.splitlines():
        if not linha.strip():
            continue

        match = LINHA.fullmatch(linha)
        if not match:
            invalidas.append(linha)
            continue

        dados = match.groupdict()
        data_str, hora_str = dados["data"], dados["hora"]

        try:
            instante = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            invalidas.append(linha)
            continue

        resto = dados.get("resto")
        if not resto:
            invalidas.append(linha)
            continue

        pares = PARES_RE.findall(resto)
        if not pares:
            invalidas.append(linha)
            continue

        valores: dict[str, float | str] = {}
        for k, v in pares:
            try:
                valores[k] = float(v)
            except ValueError:
                valores[k] = v

        registros.append(
            Registro(
                instante=instante,
                nivel=dados["nivel"],
                tag=dados["tag"],
                valores=valores,
            )
        )

    return registros, invalidas


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros."""
    tags = {r.tag for r in registros}
    return {tag: sum(1 for r in registros if r.tag == tag) for tag in tags}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave."""
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
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag."""
    return {tag: (lambda c, f=fator: c * f) for tag, fator in escalas.items()}


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Bytes ocupados pelas `contagens` em cada estrutura."""
    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("contagens deve ser um ndarray 1D de inteiros.")

    lista = contagens.tolist()
    bytes_lista = sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)

    arr_h = array.array("H", lista)
    bytes_array_h = arr_h.itemsize * len(arr_h)

    return {
        "list": bytes_lista,
        "array('H')": bytes_array_h,
        "uint16": contagens.astype("uint16").nbytes,
        "int32": contagens.astype("int32").nbytes,
        "int64": contagens.astype("int64").nbytes,
        "float32": contagens.astype("float32").nbytes,
        "float64": contagens.astype("float64").nbytes,
    }


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    res = []
    for c in contagens:
        res.append(c * 600 / 4095)
    return res


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    return [c * 600 / 4095 for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    return list(map(lambda c: c * 600 / 4095, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    return contagens * 600 / 4095


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições."""
    lista = contagens.tolist()
    return {
        "laço": cronometrar(converter_laco, lista, k=k),
        "compreensão": cronometrar(converter_compreensao, lista, k=k),
        "map+lambda": cronometrar(converter_map, lista, k=k),
        "vetorizado": cronometrar(converter_vetorizado, contagens, k=k),
    }
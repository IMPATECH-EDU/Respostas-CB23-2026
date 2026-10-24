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

LINHA: re.Pattern = re.compile(r"""
    (?P<data>\d{4}-\d{2}-\d{2})  # AAAA-MM-DD
    \s+
    (?P<hora>\d{2}:\d{2}:\d{2})  # HH:MM:SS
    \s+
    (?P<nivel>INFO|WARN|ALARME)  # INFO, WARN ou ALARME
    \s+
    (?P<tag>[A-Z]{1,2}\d{1,3})   # 1 ou 2 letras maiúsculas seguidas de 1 a 3 dígitos
    \s+
    (?P<resto>\S.*)              # o restante da linha, começando por um caractere que não é espaço
""", re.VERBOSE)


@dataclass(frozen=True)
class Registro:
    """Uma linha válida do log: instante, nível, tag e os pares chave=valor convertidos."""

    instante: datetime
    nivel: str
    tag: str
    valores: dict[str, float | str]


def valida_tag(s: str) -> bool:
    """`True` se a string inteira for uma tag válida (1 ou 2 maiúsculas e 1 a 3 dígitos)."""
    padrao = re.compile(r"[A-Z]{1,2}\d{1,3}")
    return bool(padrao.fullmatch(s))


def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Lê o texto do log e devolve `(registros, invalidas)`."""
    if not texto:
        return [], []

    registros = []
    invalidas = []
    padrao_pares = re.compile(r"(\w+)=(\S+)")

    for linha in texto.splitlines():
        if not linha.strip():
            continue

        match = LINHA.fullmatch(linha)
        if not match:
            invalidas.append(linha)
            continue

        try:
            instante = datetime.strptime(f"{match.group('data')} {match.group('hora')}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            invalidas.append(linha)
            continue

        pares = padrao_pares.findall(match.group('resto'))
        if not pares:
            invalidas.append(linha)
            continue

        valores = {}
        for k, v in pares:
            try:
                valores[k] = float(v)
            except ValueError:
                valores[k] = v

        registros.append(Registro(
            instante=instante,
            nivel=match.group('nivel'),
            tag=match.group('tag'),
            valores=valores
        ))

    return registros, invalidas


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros."""
    return {tag: len([r for r in registros if r.tag == tag]) for tag in {r.tag for r in registros}}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave."""
    valores = [r.valores[chave] for r in registros if r.tag == tag and chave in r.valores]
    return SerieTemporal.de_lista(valores)


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag."""
    return {tag: (lambda c, fator=fator: c * fator) for tag, fator in escalas.items()}


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Bytes ocupados pelas `contagens` em cada estrutura."""
    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("contagens deve ser um ndarray 1D de inteiros")

    lista = contagens.tolist()
    bytes_list = sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)

    arr_h = array.array("H", contagens)
    bytes_arr_h = arr_h.itemsize * len(arr_h)

    return {
        "list": bytes_list,
        "array('H')": bytes_arr_h,
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
        res.append(c * 600.0 / 4095.0)
    return res


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    return [c * 600.0 / 4095.0 for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    return list(map(lambda c: c * 600.0 / 4095.0, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    return contagens * 600.0 / 4095.0


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições."""
    lista = contagens.tolist()
    return {
        "laço": cronometrar(converter_laco, lista, k=k),
        "compreensão": cronometrar(converter_compreensao, lista, k=k),
        "map+lambda": cronometrar(converter_map, lista, k=k),
        "vetorizado": cronometrar(converter_vetorizado, contagens, k=k),
    }
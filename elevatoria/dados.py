"""Leitura do log SCADA e preparação dos dados da estação elevatória."""
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

LINHA: re.Pattern = re.compile(
    r"""
    (?P<data>\d{4}-\d{2}-\d{2})\s+    # Data AAAA-MM-DD
    (?P<hora>\d{2}:\d{2}:\d{2})\s+    # Hora HH:MM:SS
    (?P<nivel>INFO|WARN|ALARME)\s+    # Nível do registro
    (?P<tag>[A-Z]{1,2}\d{1,3})\s+     # Identificador do instrumento
    (?P<resto>\S.*)                   # Conteúdo após a tag
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


def valida_tag(s: str) -> bool:
    """Verifica se a string inteira identifica um instrumento."""
    padrao = r"[A-Z]{1,2}\d{1,3}"
    return re.fullmatch(padrao, s) is not None


def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Devolve os registros válidos e as linhas inválidas originais, em ordem."""
    invalidas = []
    registros = []

    for linha in texto.splitlines():
        if linha.strip() == "":
            continue

        resultado = LINHA.fullmatch(linha)
        if resultado is None:
            invalidas.append(linha)
            continue

        data = resultado.group("data")
        horas = resultado.group("hora")

        try:
            instante = datetime.strptime(
                f"{data} {horas}", "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            invalidas.append(linha)
            continue

        resto = resultado.group("resto")
        pares = re.findall(r"(\w+)=(\S+)", resto)

        if not pares:
            invalidas.append(linha)
            continue

        valores: dict[str, float | str] = {}
        for chave, valor in pares:
            try:
                valores[chave] = float(valor)
            except ValueError:
                valores[chave] = valor

        nivel = resultado.group("nivel")
        tag = resultado.group("tag")

        registro = Registro(instante=instante, nivel=nivel, tag=tag, valores=valores)
        registros.append(registro)

    return registros, invalidas



def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Conta quantos registros existem para cada tag presente."""
    tags = {r.tag for r in registros}
    contagem = {tag: sum(1 for r in registros if r.tag == tag) for tag in tags}
    return contagem

def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """Extrai, em ordem, os valores da chave presentes nos registros da tag."""
    valores = [r.valores[chave] for r in registros if r.tag == tag and chave in r.valores]
    return SerieTemporal.de_lista(valores)


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Cria um conversor para cada tag, fixando o fator individual."""
    conversores = {}
    for tag, fator in escalas.items():
        conversores[tag] = lambda c, fator=fator: fator * c
    return conversores


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Mede em bytes as representações de um vetor de contagens inteiras de 12 bits.

    Levanta ValueError para uma entrada fora desse domínio.
    """
    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1:
        raise ValueError("contagens deve ser um ndarray unidimensional")
    if not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("as contagens devem ser inteiras")
    if contagens.size and (contagens.min() < 0 or contagens.max() > 4095):
        raise ValueError("as contagens devem estar entre 0 e 4095")

    lista = contagens.tolist()
    compacto = array.array("H", lista)
    memoria = {
        "list": sys.getsizeof(lista) + sum(map(sys.getsizeof, lista)),
        "array('H')": compacto.itemsize * len(compacto),
    }
    for tipo in ("uint16", "int32", "int64", "float32", "float64"):
        memoria[tipo] = contagens.astype(tipo, copy=False).nbytes
    return memoria


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    resultado = []
    for i in contagens:
        resultado.append(i * 600 / 4095)
    return resultado


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte as contagens em kPa por compreensão de lista."""
    return [i * 600 / 4095 for i in contagens]

def converter_map(contagens: list[int]) -> list[float]:
    """Converte as contagens em kPa aplicando map a uma lambda."""
    return list(map(lambda x: x * 600 / 4095, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte um vetor de contagens em kPa usando operações do NumPy."""
    return contagens * (600 / 4095)


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).
    """
    lista = contagens.tolist()
    tempo_laco = cronometrar(converter_laco, lista, k=k)
    tempo_compreensão = cronometrar(converter_compreensao, lista, k=k)
    tempo_maplambda = cronometrar(converter_map, lista, k=k)
    tempo_vetorizado = cronometrar(converter_vetorizado, contagens, k=k)
    dicionario_tempo = {}
    dicionario_tempo["laço"] = tempo_laco
    dicionario_tempo["compreensão"] = tempo_compreensão
    dicionario_tempo["map+lambda"] = tempo_maplambda
    dicionario_tempo["vetorizado"] = tempo_vetorizado
    return dicionario_tempo

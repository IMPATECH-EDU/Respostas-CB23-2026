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

#: Padrão de uma linha válida do log, compilado com `re.compile(..., re.VERBOSE)` e com um
#: comentário em cada parte. Grupos nomeados: `data` (AAAA-MM-DD), `hora` (HH:MM:SS),
#: `nivel` (INFO, WARN ou ALARME), `tag` (1 ou 2 letras maiúsculas seguidas de 1 a 3
#: dígitos) e `resto` (o restante da linha, começando por um caractere que não é espaço).
#: As partes são separadas por um ou mais espaços. A linha inteira deve casar: o padrão é
#: aplicado com `LINHA.fullmatch(linha)`.
LINHA: re.Pattern = re.compile(
    r"""
    (?P<data>\d{4}-\d{2}-\d{2})     #Data, separado com um numero de 4 digitos, e dois de 2 digitos
    \s+                             #Espaço uma ou mais vezes
    (?P<hora>\d{2}:\d{2}:\d{2})     #Hora, separado em hora, minuto e segundos cada um com dois digitos
    \s+
    (?P<nivel>INFO|WARN|ALARME)     #Um dos três possíveis níveis
    \s+
    (?P<tag>[A-Z]{1,2}\d{1,3})      #Duas letras maiusculas e digitos de 1 a 3
    \s+
    (?P<resto>\S.*)                  #Começa por caracter não espaço, pega as chaves e os valores
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
    """`True` se a string inteira for uma tag válida (1 ou 2 maiúsculas e 1 a 3 dígitos).

    Use `fullmatch`. Válidas: `"PT101"`, `"FT201"`, `"B1"`. Inválidas: `"pt101"`, `"PT"`,
    `"PT1010"`, `"101PT"` e `"PT101 "` (sobra de caracteres).
    """
    
    return bool(re.fullmatch(r"[A-Z]{1,2}\d{1,3}", s))

def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Lê o texto do log e devolve `(registros, invalidas)`."""
    registros: list[Registro] = []
    invalidas: list[str] = []

    for linha in texto.splitlines(): 
        if not linha.strip():
            continue

        match = LINHA.fullmatch(linha)
        if not match:
            invalidas.append(linha)
            continue

        data = match.group("data")
        hora = match.group("hora")
        nivel = match.group("nivel")
        tag = match.group("tag")
        resto = match.group("resto")


        try: # Tenta converter data e hora em datetime
            instante = datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            invalidas.append(linha)
            continue

        pares = re.findall(r"(\w+)=(\S+)", resto) # Extrai os pares de chave = valor do resto
        if not pares:
            invalidas.append(linha)
            continue

        valores: dict[str, float | str] = {}
        for chave, val_str in pares:
            try:
                valores[chave] = float(val_str)
            except ValueError:
                valores[chave] = val_str

        registros.append(
            Registro(
                instante=instante,
                nivel=nivel,
                tag=tag,
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
    return {tag: len(por_tag(registros, tag)) for tag in tags}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave."""
    return SerieTemporal.de_lista([r.valores[chave] for r in por_tag(registros, tag)if chave in r.valores])


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag."""

    return {tag: lambda c, f=fator: c * f for tag, fator in escalas.items()} 

# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Bytes ocupados pelas `contagens` (ndarray 1D de inteiros de 0 a 4095) em cada estrutura."""

    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("contagens deve ser um ndarray 1D de inteiros")

    lista = contagens.tolist()
    tamanho_lista = sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)

    arr_python = array.array("H", lista)
    tamanho_array =arr_python.itemsize * len(arr_python)
    resultados = {"list":tamanho_lista,
                  "array('H')":tamanho_array}

    for i in ["uint16", "int32", "int64", "float32", "float64"]:
        resultados[i] = contagens.astype(i).nbytes

    return resultados

def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    resultado = []
    for c in contagens:
        resultado.append(c*600/4095)
    return resultado


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    return [c*600/4095 for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    return list(map(lambda c: c*600/4095, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    return contagens * 600 / 4095


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições."""
    lista = contagens.tolist()
    return {"laço": cronometrar(lambda: converter_laco(lista), k=k),
            "compreensão": cronometrar(lambda: converter_compreensao(lista), k=k),
            "map+lambda": cronometrar(lambda: converter_map(lista), k=k),
            "vetorizado": cronometrar(lambda: converter_vetorizado(contagens), k=k),
             }

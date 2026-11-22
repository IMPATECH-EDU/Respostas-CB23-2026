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
LINHA: re.Pattern = re.compile(r"""
    (?P<data>\d{4}-\d{2}-\d{2})  # AAAA-MM-DD
    \s+
    (?P<hora>\d{2}:\d{2}:\d{2})  # HH:MM:SS
    \s+
    (?P<nivel>INFO|WARN|ALARME)
    \s+
    (?P<tag>[A-Z]{1,2}\d{1,3})   # 1 ou 2 letras maiúsculas seguidas de 1 a 3 dígitos
    \s+
    (?P<resto>\S.*)
""", re.VERBOSE)

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
    """Lê o texto do log e devolve `(registros, invalidas)`.

    - `registros`: lista de `Registro`, na ordem em que as linhas aparecem no texto;
    - `invalidas`: lista das linhas descartadas, exatamente como estavam no texto.

    Regras:

    - linhas vazias (ou só com espaços) são ignoradas e não contam como inválidas;
    - uma linha é inválida se não casar com `LINHA` (com `fullmatch`), se a data ou a hora
      forem impossíveis (por exemplo, mês 13) ou se o `resto` não tiver nenhum par
      chave=valor;
    - `instante` vem de `datetime.strptime` aplicado a `data` e `hora`;
    - os pares são extraídos do grupo `resto` com o padrão `(\\w+)=(\\S+)`; cada valor vira
      `float` quando a conversão é possível e continua `str` nos demais casos
      (`contagens=1623` vira `1623.0`; `evento=partida` continua `"partida"`);
    - texto vazio devolve `([], [])`.
    """
    registros: list[Registro] = []
    invalidas: list[str] = []

    if not texto:
        return registros, invalidas

    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha:
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

        pares = re.findall(r"(\w+)=(\S+)", match.group("resto"))
        if not pares:
            invalidas.append(linha)
            continue

        valores = {}
        for chave, valor in pares:
            try:
                valores[chave] = float(valor)
            except ValueError:
                valores[chave] = valor

        registros.append(Registro(instante = instante, nivel = match.group("nivel"), tag = match.group("tag"), valores = valores))

    return registros, invalidas

def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """
    quant_tag = {}
    for r in registros:
        if r.tag not in quant_tag:
            quant_tag[r.tag] = 1
        else:
            quant_tag[r.tag] += 1
    return quant_tag 


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave."""
    # Filtra os registros da tag que possuem a chave e extrai o valor
    valores = [r.valores[chave] for r in registros if r.tag == tag and chave in r.valores]
    return SerieTemporal.de_lista(valores)


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag."""
    # O default argument (f=fator) resolve o problema de late binding do Python
    return {tag: (lambda c, f=fator: c * f) for tag, fator in escalas.items()}


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Bytes ocupados pelas `contagens` em cada estrutura."""
    if getattr(contagens, "ndim", 0) != 1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("contagens deve ser um ndarray 1D de inteiros")

    lista = contagens.tolist()
    # Soma o tamanho da estrutura lista com o tamanho de cada inteiro dentro dela
    tamanho_lista = sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)
    
    arr = array.array('H', lista)
    tamanho_array = arr.itemsize * len(arr)

    return {
        "list": tamanho_lista,
        "array('H')": tamanho_array,
        "uint16": contagens.astype(np.uint16).nbytes,
        "int32": contagens.astype(np.int32).nbytes,
        "int64": contagens.astype(np.int64).nbytes,
        "float32": contagens.astype(np.float32).nbytes,
        "float64": contagens.astype(np.float64).nbytes,
    }

def converter_laco(contagens: list[int]) -> list[float]:
    resultado = []
    for c in contagens:
        resultado.append(c * 600 / 4095)
    return resultado

def converter_compreensao(contagens: list[int]) -> list[float]:
    return [c * 600 / 4095 for c in contagens]

def converter_map(contagens: list[int]) -> list[float]:
    return list(map(lambda c: c * 600 / 4095, contagens))

def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    return contagens * 600 / 4095

def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    lista = contagens.tolist()
    return {
        "laço": cronometrar(converter_laco, lista, k=k),
        "compreensão": cronometrar(converter_compreensao, lista, k=k),
        "map+lambda": cronometrar(converter_map, lista, k=k),
        "vetorizado": cronometrar(converter_vetorizado, contagens, k=k)
    }
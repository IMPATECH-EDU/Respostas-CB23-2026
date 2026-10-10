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
# 2026-10-05 08:45:00 WARN B1 evento=vibracao corrente=49.8
#: Padrão de uma linha válida do log, compilado com `re.compile(..., re.VERBOSE)` e com um
#: comentário em cada parte. Grupos nomeados: `data` (AAAA-MM-DD), `hora` (HH:MM:SS),
#: `nivel` (INFO, WARN ou ALARME), `tag` (1 ou 2 letras maiúsculas seguidas de 1 a 3
#: dígitos) e `resto` (o restante da linha, começando por um caractere que não é espaço).
#: As partes são separadas por um ou mais espaços. A linha inteira deve casar: o padrão é
#: aplicado com `LINHA.fullmatch(linha)`.
LINHA = re.compile(r"""
\s*(?P<data>\d{4}-\d{2}-\d{2})\s+ # 'data' AAAA-MM-DD com espaços opcionais antes e depois 
(?P<hora>\d{2}:\d{2}:\d{2})\s+ # 'hora' AAAA-MM-DD com espaços opcionais antes e depois
(?P<nivel>INFO|WARN|ALARME)\s+ # 'nivel' INFO, WARN ou ALARME com espaços opcionais antes e depois
(?P<tag>[A-Z]{1,2}\d{1,3})\s+ # 'tag' 1 ou 2 letras maiúsculas seguidas de 1 a 3 dígitos com espaços opcionais antes e depois
(?P<resto>\S.*) # 'resto' o restante da linha  com espaços opcionais antes
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
    return bool(re.fullmatch(r"[A-Z]{1,2}\d{1,3}", s)) #feito


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
    registros=[]
    invalidas=[]
    for linha in texto.splitlines():
        corresponde=LINHA.fullmatch(linha)
        if bool(corresponde):
            data = corresponde.group("data")
            hora = corresponde.group("hora")
            instante = f"{data} {hora}"
            try:
                instante = datetime.strptime(instante, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                invalidas.append(linha)
                continue
            resto=corresponde.group("resto")
            pares=re.findall(r"(\w+)=(\S+)", resto)
            if not pares:
                invalidas.append(linha)
                continue
            valores=dict(pares)
            for x in valores:
                try:
                    valores[x]=float(valores[x])
                except ValueError:
                    pass
            nivel =corresponde.group("nivel")
            tag =corresponde.group("tag")
            reg=Registro(instante=instante, nivel=nivel, tag=tag, valores=valores)
            registros.append(reg)
        elif not bool(re.fullmatch(r"\s*",linha)):
            invalidas.append(linha)
    return (registros,invalidas)


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """
    tags = {r.tag for r in registros}
    return {tag: len(por_tag(registros, tag)) for tag in tags}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave.

    Os registros da tag sem essa chave (por exemplo, os alarmes de PT102, que não têm
    `contagens`) são ignorados. Crie a série com `SerieTemporal.de_lista`.
    """
    sequencia=[]
    for registro in (r for r in registros if r.tag == tag):
        try:
            sequencia.append(registro.valores[chave])
        except KeyError:
            pass
    return SerieTemporal.de_lista(sequencia)


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag.

    Cada `f` é uma lambda. Cuidado com o *late binding*: cada função deve usar o fator da
    sua tag, e não o último fator do dicionário (veja a issue #2 no enunciado).
    """
    funcoes={}
    for tag in escalas:
        funcoes[tag]= lambda c, fator=escalas[tag]: c*fator
    return funcoes


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
    if contagens.ndim!=1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError
    lista=contagens.tolist()
    dict_memoria={
        "list": (sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)),
        "array('H')": array.array('H',contagens).itemsize * len(contagens),
        "uint16": contagens.astype(np.uint16).nbytes,
        "int32": contagens.astype(np.int32).nbytes,
        "int64": contagens.astype(np.int64).nbytes,
        "float32": contagens.astype(np.float32).nbytes,
        "float64": contagens.astype(np.float64).nbytes
    }
    return dict_memoria


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    resultado=[]
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
    return contagens*(600/4095)


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).
    """
    lista = contagens.tolist()
    return {
        "laço": cronometrar(converter_laco, lista, k=k),
        "compreensão": cronometrar(converter_compreensao, lista, k=k),
        "map+lambda": cronometrar(converter_map, lista, k=k),
        "vetorizado": cronometrar(converter_vetorizado, contagens, k=k)
    }
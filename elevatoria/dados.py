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
    (?P<data>\d{4}-\d{2}-\d{2})   # Data no formato AAAA-MM-DD
    \s+                           # Separador: um ou mais espaços
    (?P<hora>\d{2}:\d{2}:\d{2})   # Hora no formato HH:MM:SS
    \s+                           # Separador: um ou mais espaços
    (?P<nivel>INFO|WARN|ALARME)   # Nível de severidade permitido
    \s+                           # Separador: um ou mais espaços
    (?P<tag>[A-Z]{1,2}\d{1,3})    # Identificador do instrumento (tag)
    \s+                           # Separador: um ou mais espaços
    (?P<resto>\S.*)               # Pares chave=valor restantes
    """,
    re.VERBOSE,
)

_PADRAO_TAG: re.Pattern = re.compile(r"[A-Z]{1,2}\d{1,3}")
_PADRAO_PARES: re.Pattern = re.compile(r"(\w+)=(\S+)")

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
    return bool(_PADRAO_TAG.fullmatch(s))


def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Lê o texto do log e devolve `(registros, invalidas)`.

    - `registros`: lista de `Registro`, na ordem em que as linhas aparecem no texto;
    - `invalidas`: lista das linhas descartadas, exatamente como estavam no texto.
    """
    if not texto:
        return [], []

    registros: list[Registro] = []
    invalidas: list[str] = []

    for linha in texto.splitlines():
        # Linhas em branco ou só espaços são ignoradas sem contar como inválidas
        if not linha.strip():
            continue

        casamento = LINHA.fullmatch(linha)
        if casamento is None:
            invalidas.append(linha)
            continue

        dados_linha = casamento.groupdict()

        # Validação do instante temporal
        try:
            instante = datetime.strptime(
                f"{dados_linha['data']} {dados_linha['hora']}",
                "%Y-%m-%d %H:%M:%S",
            )
        except ValueError:
            invalidas.append(linha)
            continue

        # Extração e conversão dos pares chave=valor
        pares = _PADRAO_PARES.findall(dados_linha["resto"])
        if not pares:
            invalidas.append(linha)
            continue

        valores: dict[str, float | str] = {}
        for chave, valor_str in pares:
            try:
                valores[chave] = float(valor_str)
            except ValueError:
                valores[chave] = valor_str

        registros.append(
            Registro(
                instante=instante,
                nivel=dados_linha["nivel"],
                tag=dados_linha["tag"],
                valores=valores,
            )
        )

    return registros, invalidas



def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Usa compreensão de dicionário sobre um conjunto obtido por compreensão de conjunto.
    """
    tags_unicas = {r.tag for r in registros}
    return {tag: sum(1 for r in registros if r.tag == tag) for tag in tags_unicas}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave."""
    dados_chave = [
        float(r.valores[chave])
        for r in registros
        if r.tag == tag and chave in r.valores
    ]
    return SerieTemporal.de_lista(dados_chave)



# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag.

    O argumento padrão `k=fator` na lambda evita o late binding.
    """
    return {tag: (lambda c, k=fator: c * k) for tag, fator in escalas.items()}


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
    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("contagens deve ser um ndarray unidimensional de inteiros")

    lista = contagens.tolist()
    bytes_lista = sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)

    arr_h = array.array("H", lista)
    bytes_array_h = arr_h.itemsize * len(arr_h)

    return {
        "list": bytes_lista,
        "array('H')": bytes_array_h,
        "uint16": contagens.astype(np.uint16).nbytes,
        "int32": contagens.astype(np.int32).nbytes,
        "int64": contagens.astype(np.int64).nbytes,
        "float32": contagens.astype(np.float32).nbytes,
        "float64": contagens.astype(np.float64).nbytes,
    }


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    resultado: list[float] = []
    fator = 600.0 / 4095.0
    for c in contagens:
        resultado.append(c * fator)
    return resultado


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    fator = 600.0 / 4095.0
    return [c * fator for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    fator = 600.0 / 4095.0
    return list(map(lambda c: c * fator, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    return contagens * (600.0 / 4095.0)


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
        "vetorizado": cronometrar(converter_vetorizado, contagens, k=k),
    }

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

#: Trecho de regex de uma tag (1 ou 2 maiúsculas e 1 a 3 dígitos), usado em `LINHA` e em
#: `valida_tag` para que as duas regras nunca divirjam.
_TAG = r"[A-Z]{1,2}[0-9]{1,3}"

#: Padrão de uma linha válida do log, compilado com `re.compile(..., re.VERBOSE)` e com um
#: comentário em cada parte. Grupos nomeados: `data` (AAAA-MM-DD), `hora` (HH:MM:SS),
#: `nivel` (INFO, WARN ou ALARME), `tag` (1 ou 2 letras maiúsculas seguidas de 1 a 3
#: dígitos) e `resto` (o restante da linha, começando por um caractere que não é espaço).
#: As partes são separadas por um ou mais espaços. A linha inteira deve casar: o padrão é
#: aplicado com `LINHA.fullmatch(linha)`.
LINHA: re.Pattern = re.compile(
    rf"""
    (?P<data> [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}} )  # data AAAA-MM-DD (validada depois)
    [ ]+                                          # separador: um ou mais espaços
    (?P<hora> [0-9]{{2}}:[0-9]{{2}}:[0-9]{{2}} )  # hora HH:MM:SS (validada depois)
    [ ]+
    (?P<nivel> INFO | WARN | ALARME )             # só os três níveis conhecidos
    [ ]+
    (?P<tag> {_TAG} )                             # tag do instrumento, ex.: PT102, B1
    [ ]+
    (?P<resto> \S.* )                             # o resto começa por um não espaço
    """,
    re.VERBOSE,
)

#: Padrão de uma tag isolada, aplicado com `fullmatch` em `valida_tag`.
_PADRAO_TAG: re.Pattern = re.compile(_TAG)

#: Um par `chave=valor` dentro do grupo `resto` de `LINHA`.
_PAR: re.Pattern = re.compile(r"(\w+)=(\S+)")

_FORMATO_INSTANTE = "%Y-%m-%d %H:%M:%S"


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
    return _PADRAO_TAG.fullmatch(s) is not None


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
    for linha in texto.splitlines():
        if not linha.strip():
            continue
        try:
            registros.append(_registro_da_linha(linha))
        except ValueError:
            invalidas.append(linha)
    return registros, invalidas

def _numero_ou_texto(bruto: str) -> float | str:
    """Converte `bruto` em `float` quando possível; caso contrário, devolve-o intacto."""
    try:
        return float(bruto)
    except ValueError:
        return bruto


def _registro_da_linha(linha: str) -> Registro:
    """Interpreta uma linha não vazia do log.

    Levanta `ValueError` se a linha não casar com `LINHA`, se a data ou a hora forem
    impossíveis, ou se o `resto` não tiver nenhum par chave=valor.
    """
    casamento = LINHA.fullmatch(linha)
    if casamento is None:
        raise ValueError(f"linha fora do formato do log: {linha!r}")
    # strptime levanta ValueError para datas e horas impossíveis (mês 13, 25:00:00...).
    instante = datetime.strptime(f"{casamento['data']} {casamento['hora']}", _FORMATO_INSTANTE)
    pares = _PAR.findall(casamento["resto"])
    if not pares:
        raise ValueError(f"linha sem pares chave=valor: {linha!r}")
    valores = {chave: _numero_ou_texto(bruto) for chave, bruto in pares}
    return Registro(instante, casamento["nivel"], casamento["tag"], valores)

def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """
    tags_presentes = {r.tag for r in registros}
    return {tag: sum(1 for r in registros if r.tag == tag) for tag in sorted(tags_presentes)}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave.

    Os registros da tag sem essa chave (por exemplo, os alarmes de PT102, que não têm
    `contagens`) são ignorados. Crie a série com `SerieTemporal.de_lista`.

    Levanta `ValueError` se algum valor de `chave` não for numérico (por exemplo,
    `serie(registros, "B1", "evento")`).
    """
    brutos = [r.valores[chave] for r in por_tag(registros, tag) if chave in r.valores]
    nao_numericos = [v for v in brutos if isinstance(v, str)]
    if nao_numericos:
        raise ValueError(f"a chave {chave!r} de {tag} não é numérica: {nao_numericos[0]!r}")
    return SerieTemporal.de_lista([float(v) for v in brutos])


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag.

    Cada `f` é uma lambda. Cuidado com o *late binding*: cada função deve usar o fator da
    sua tag, e não o último fator do dicionário (veja a issue #2 no enunciado).
    """
    return {tag: _multiplicador(fator) for tag, fator in escalas.items()}

def _multiplicador(fator: float) -> Callable[[float], float]:
    """Lambda `c -> c * fator`, com `fator` fixado no momento desta chamada.

    Cada chamada cria um escopo novo, então a lambda devolvida guarda o seu próprio `fator`
    e não enxerga a variável do laço de `criar_conversores` (que é o que causa o *late
    binding* na versão com a lambda escrita direto dentro da compreensão).
    """
    return lambda c: c * fator

# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
_CONTAGEM_MAXIMA = 4095   # maior contagem do conversor A/D de 12 bits
_FUNDO_ESCALA_KPA = 600   # pressão (kPa) da escala nominal em 4095 contagens
_DTYPES_MEDIDOS = ("uint16", "int32", "int64", "float32", "float64")
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
    if not isinstance(contagens, np.ndarray):
        raise ValueError(f"contagens deve ser um numpy.ndarray; recebi {type(contagens).__name__}")
    if contagens.ndim != 1:
        raise ValueError(f"contagens deve ser 1D; recebi ndim={contagens.ndim}")
    if not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError(f"contagens deve ter dtype inteiro; recebi {contagens.dtype}")
    if contagens.size and (contagens.min() < 0 or contagens.max() > _CONTAGEM_MAXIMA):
        raise ValueError(f"contagens deve estar entre 0 e {_CONTAGEM_MAXIMA}")

    como_lista = contagens.tolist()
    bytes_lista = sys.getsizeof(como_lista) + sum(sys.getsizeof(x) for x in como_lista)
    compacto = array.array("H", como_lista)
    bytes_por_estrutura = {"list": bytes_lista,
                           "array('H')": compacto.itemsize * len(compacto)}
    for nome_dtype in _DTYPES_MEDIDOS:
        bytes_por_estrutura[nome_dtype] = contagens.astype(nome_dtype).nbytes
    return bytes_por_estrutura


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    pressoes: list[float] = []
    for c in contagens:
        pressoes.append(c * _FUNDO_ESCALA_KPA / _CONTAGEM_MAXIMA)
    return pressoes


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    return [c * _FUNDO_ESCALA_KPA / _CONTAGEM_MAXIMA for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    return list(map(lambda c: c * _FUNDO_ESCALA_KPA / _CONTAGEM_MAXIMA, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    # Converte para float antes de multiplicar: com dtype uint16, `c * 600` estouraria
    # (4095 * 600 = 2_457_000 > 65_535) antes da divisão.
    return np.asarray(contagens, dtype=np.float64) * _FUNDO_ESCALA_KPA / _CONTAGEM_MAXIMA


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).
    """
    como_lista = contagens.tolist()  # criada uma vez, fora das medições
    return {
        "laço": cronometrar(converter_laco, como_lista, k=k),
        "compreensão": cronometrar(converter_compreensao, como_lista, k=k),
        "map+lambda": cronometrar(converter_map, como_lista, k=k),
        "vetorizado": cronometrar(converter_vetorizado, contagens, k=k),
    }

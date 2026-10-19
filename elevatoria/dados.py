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
    (?P<data>\d{4}-\d{2}-\d{2})  # Data no formato AAAA-MM-DD
    \s+                          # Um ou mais espaços separadores
    (?P<hora>\d{2}:\d{2}:\d{2})  # Hora no formato HH:MM:SS
    \s+                          # Um ou mais espaços separadores
    (?P<nivel>INFO|WARN|ALARME)  # Nível do log (INFO, WARN ou ALARME)
    \s+                          # Um ou mais espaços separadores
    (?P<tag>[A-Z]{1,2}\d{1,3})   # Tag (1 ou 2 letras maiúsculas e 1 a 3 dígitos)
    \s+                          # Um ou mais espaços separadores
    (?P<resto>\S.*)              # Restante da linha, iniciando sem espaço
    """,
    re.VERBOSE,
)

# Mesma regra da tag que está dentro de LINHA, mas sozinha (usada em valida_tag).
_TAG = re.compile(r"[A-Z]{1,2}\d{1,3}")

# Um par chave=valor dentro do grupo `resto`.
_PAR = re.compile(r"(\w+)=(\S+)")


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
    # fullmatch exige que o padrão cubra a string do primeiro ao último caractere;
    # com match, "PT1010" passaria (casa "PT101" e ignora o resto).
    return _TAG.fullmatch(s) is not None


def _numero_ou_texto(valor: str) -> float | str:
    """Converte `valor` para `float` quando dá; senão devolve a própria string."""
    try:
        return float(valor)
    except ValueError:
        return valor


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

        match = LINHA.fullmatch(linha)
        if match is None:
            invalidas.append(linha)
            continue

        # O padrão só confere o formato (2 dígitos para o mês, por exemplo); quem sabe
        # que não existe mês 13 nem 25 horas é o strptime.
        data_str, hora_str = match["data"], match["hora"]
        try:
            instante = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            invalidas.append(linha)
            continue

        pares = _PAR.findall(match["resto"])
        if not pares:
            invalidas.append(linha)
            continue

        valores = {chave: _numero_ou_texto(v) for chave, v in pares}
        registros.append(Registro(instante=instante, nivel=match["nivel"],
                                  tag=match["tag"], valores=valores))

    return registros, invalidas


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """
    tags = {r.tag for r in registros}
    return {t: sum(1 for r in registros if r.tag == t) for t in tags}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave.

    Os registros da tag sem essa chave (por exemplo, os alarmes de PT102, que não têm
    `contagens`) são ignorados. Crie a série com `SerieTemporal.de_lista`.

    Levanta `ValueError` se algum dos valores encontrados não for numérico (por exemplo,
    `serie(registros, "B1", "evento")`).
    """
    valores = [r.valores[chave] for r in por_tag(registros, tag) if chave in r.valores]
    numeros = [v for v in valores if isinstance(v, float)]
    if len(numeros) != len(valores):
        textos = sorted({str(v) for v in valores if not isinstance(v, float)})
        raise ValueError(f"a chave {chave!r} da tag {tag!r} tem valores não numéricos: {textos}")
    return SerieTemporal.de_lista(numeros)


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def _multiplicador(fator: float) -> Callable[[float], float]:
    """Lambda que multiplica a contagem por `fator`, fixado no momento da chamada."""
    # Cada chamada cria um escopo novo, com o seu próprio `fator`; a lambda guarda esse
    # escopo (closure). Não há uma variável compartilhada que mude depois.
    return lambda c: c * fator


def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag.

    Cada `f` é uma lambda. Cuidado com o *late binding*: cada função deve usar o fator da
    sua tag, e não o último fator do dicionário (veja a issue #2 no enunciado).
    """
    # A versão `{tag: lambda c: c * fator for ...}` leria `fator` só na hora da chamada,
    # quando o laço já acabou e `fator` vale o último fator do dicionário.
    return {tag: _multiplicador(fator) for tag, fator in escalas.items()}


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
_DTYPES = ("uint16", "int32", "int64", "float32", "float64")


def _exige_vetor_de_inteiros(contagens: np.ndarray) -> None:
    """Levanta `ValueError` se `contagens` não for um `ndarray` 1D de inteiros."""
    if not isinstance(contagens, np.ndarray):
        raise ValueError(f"esperava um numpy.ndarray; recebi {type(contagens).__name__}")
    if contagens.ndim != 1:
        raise ValueError(f"esperava um vetor 1D; recebi ndim={contagens.ndim}")
    if not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError(f"esperava inteiros; recebi dtype={contagens.dtype}")


def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Bytes ocupados pelas `contagens` (ndarray 1D de inteiros de 0 a 4095) em cada estrutura.

    Devolve um dicionário com exatamente estas chaves:

    - `"list"`: a lista `contagens.tolist()`; o total é `sys.getsizeof(lista)` mais a soma de
      `sys.getsizeof(x)` para cada elemento `x`;
    - `"array('H')"`: um `array.array("H", ...)`; conte só os dados (`itemsize * len`);
    - `"uint16"`, `"int32"`, `"int64"`, `"float32"`, `"float64"`: o `ndarray` convertido para
      esse `dtype`; conte só os dados (atributo `.nbytes`).

    Levanta `ValueError` se `contagens` não for um ndarray 1D de inteiros, ou se tiver
    valores que não cabem no typecode `"H"` (de 0 a 65535).
    """
    _exige_vetor_de_inteiros(contagens)

    lista = contagens.tolist()   # ints do Python, não escalares do NumPy
    # a lista guarda só ponteiros (8 bytes cada); cada int é um objeto separado no heap
    memoria = {"list": sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)}

    try:
        compacto = array.array("H", lista)
    except OverflowError as erro:
        raise ValueError("as contagens precisam caber em 16 bits sem sinal (0 a 65535)") from erro
    memoria["array('H')"] = compacto.itemsize * len(compacto)

    memoria.update({nome: contagens.astype(nome).nbytes for nome in _DTYPES})
    return memoria


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    kpa = []
    for c in contagens:
        kpa.append(c * 600 / 4095)
    return kpa


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    return [c * 600 / 4095 for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    return list(map(lambda c: c * 600 / 4095, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy.

    O fator é escrito como float (`600.0`) de propósito: com `contagens` em `uint16`,
    `contagens * 600` estouraria os 16 bits antes da divisão.
    """
    return np.asarray(contagens) * 600.0 / 4095.0


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).

    Levanta `ValueError` se `contagens` não for um ndarray 1D de inteiros ou se `k` não for
    um inteiro positivo (esse último vem de `cronometrar`).
    """
    _exige_vetor_de_inteiros(contagens)
    lista = contagens.tolist()
    versoes_com_lista = {"laço": converter_laco, "compreensão": converter_compreensao,
                         "map+lambda": converter_map}
    tempos = {nome: cronometrar(f, lista, k=k) for nome, f in versoes_com_lista.items()}
    tempos["vetorizado"] = cronometrar(converter_vetorizado, contagens, k=k)
    return tempos

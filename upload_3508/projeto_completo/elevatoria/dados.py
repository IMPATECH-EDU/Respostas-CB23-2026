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
    (?P<data>[0-9]{4}-[0-9]{2}-[0-9]{2})   # data AAAA-MM-DD (só dígitos ASCII)
    [ ]+                                   # um ou mais espaços entre as partes
    (?P<hora>[0-9]{2}:[0-9]{2}:[0-9]{2})   # hora HH:MM:SS
    [ ]+
    (?P<nivel>INFO|WARN|ALARME)            # nível: só os três previstos
    [ ]+
    (?P<tag>[A-Z]{1,2}[0-9]{1,3})          # tag: 1 ou 2 maiúsculas e 1 a 3 dígitos
    [ ]+
    (?P<resto>\S.*)                        # resto: começa por um caractere que não é espaço
    """,
    re.VERBOSE,
)

#: Padrão de uma tag isolada; usado com `fullmatch` em `valida_tag`.
_PADRAO_TAG = re.compile(r"[A-Z]{1,2}[0-9]{1,3}")

#: Um par chave=valor dentro do grupo `resto`.
_PAR_CHAVE_VALOR = re.compile(r"(\w+)=(\S+)")

#: Formato de `data` + " " + `hora`, para `datetime.strptime`.
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
    # fullmatch, e não match: com match, "PT1010" passaria, porque o prefixo "PT101" casa.
    return _PADRAO_TAG.fullmatch(s) is not None


def _numero_ou_texto(bruto: str) -> float | str:
    """Converte `bruto` em `float` quando possível; caso contrário, devolve o próprio texto."""
    try:
        return float(bruto)
    except ValueError:
        return bruto


def _interpretar_linha(linha: str) -> Registro:
    """Transforma uma linha do log em `Registro`.

    Levanta `ValueError`, com o motivo, se a linha não casar com `LINHA`, se a data ou a hora
    forem impossíveis ou se o `resto` não tiver nenhum par chave=valor.
    """
    casamento = LINHA.fullmatch(linha)
    if casamento is None:
        raise ValueError(f"linha fora do formato do log: {linha!r}")
    # strptime levanta ValueError para datas impossíveis (mês 13, 31/02, 25:00:00...).
    instante = datetime.strptime(f"{casamento['data']} {casamento['hora']}", _FORMATO_INSTANTE)
    pares = _PAR_CHAVE_VALOR.findall(casamento["resto"])
    if not pares:
        raise ValueError(f"linha sem nenhum par chave=valor: {linha!r}")
    valores = {chave: _numero_ou_texto(bruto) for chave, bruto in pares}
    return Registro(instante, casamento["nivel"], casamento["tag"], valores)


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
        if linha.strip() == "":
            continue                      # linha em branco: nem registro, nem inválida
        try:
            registros.append(_interpretar_linha(linha))
        except ValueError:
            invalidas.append(linha)       # guardada sem alteração, para quem quiser auditar
    return registros, invalidas


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """
    tags_distintas = {r.tag for r in registros}
    # Somar booleanos conta quantos são True: cada registro da tag vale 1.
    return {tag: sum(r.tag == tag for r in registros) for tag in tags_distintas}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave.

    Os registros da tag sem essa chave (por exemplo, os alarmes de PT102, que não têm
    `contagens`) são ignorados. Crie a série com `SerieTemporal.de_lista`.

    Levanta `ValueError` se algum dos valores encontrados não for numérico (por exemplo,
    `chave="evento"`). Se nenhum registro tiver a chave, devolve uma série vazia.
    """
    valores = [r.valores[chave] for r in por_tag(registros, tag) if chave in r.valores]
    textos = [v for v in valores if isinstance(v, str)]
    if textos:
        raise ValueError(f"a chave {chave!r} de {tag} tem valores não numéricos: {textos[:3]}")
    return SerieTemporal.de_lista(valores)


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
    """Lambda que multiplica pelo `fator` recebido.

    Cada chamada cria um escopo novo, e a lambda fica presa ao `fator` daquela chamada. Na
    versão com defeito, a lambda era criada direto na compreensão e lia a variável do laço
    só quando era chamada, ou seja, depois do fim do laço, quando ela valia o último fator.
    """
    return lambda c: c * fator


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

    Levanta `ValueError` se `contagens` não for um ndarray 1D de inteiros, ou se algum valor
    estiver fora de 0 a 4095 (o `array('H')` não aceitaria negativos).
    """
    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1:
        raise ValueError("contagens deve ser um ndarray unidimensional")
    if not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError(f"contagens deve ter dtype inteiro; recebi {contagens.dtype}")
    if contagens.size and (contagens.min() < 0 or contagens.max() > 4095):
        raise ValueError("as contagens de um A/D de 12 bits vão de 0 a 4095")

    como_lista = contagens.tolist()
    # A lista guarda ponteiros; cada int é um objeto separado, contado à parte.
    bytes_lista = sys.getsizeof(como_lista) + sum(sys.getsizeof(x) for x in como_lista)
    compacto = array.array("H", como_lista)
    memoria = {"list": bytes_lista, "array('H')": compacto.itemsize * len(compacto)}
    for nome_dtype in ("uint16", "int32", "int64", "float32", "float64"):
        memoria[nome_dtype] = int(contagens.astype(nome_dtype).nbytes)
    return memoria


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    pressoes = []
    for c in contagens:
        pressoes.append(c * 600 / 4095)
    return pressoes


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    return [c * 600 / 4095 for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    return list(map(lambda c: c * 600 / 4095, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy.

    As contagens passam para `float64` antes da conta: com um `uint16`, `c * 600` estouraria
    em silêncio (4095 * 600 não cabe em 16 bits).
    """
    return np.asarray(contagens, dtype=np.float64) * 600 / 4095


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).
    """
    lista = contagens.tolist()     # criada uma vez só, para não entrar no tempo medido
    versoes_com_lista = {"laço": converter_laco, "compreensão": converter_compreensao,
                         "map+lambda": converter_map}
    tempos = {nome: cronometrar(funcao, lista, k=k) for nome, funcao in versoes_com_lista.items()}
    tempos["vetorizado"] = cronometrar(converter_vetorizado, contagens, k=k)
    return tempos

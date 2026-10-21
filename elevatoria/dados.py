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


# Padrão LINHA com re.VERBOSE e grupos nomeados exigidos (data, hora, nivel, tag, resto)
LINHA = re.compile(
    r"""
    ^
    (?P<data>\d{4}-\d{2}-\d{2})    # Data no formato YYYY-MM-DD
    \s+
    (?P<hora>\d{2}:\d{2}:\d{2})    # Hora no formato HH:MM:SS
    \s+
    (?P<nivel>INFO|WARN|ALARME)    # Nível do log SCADA
    \s+
    (?P<tag>[A-Z]{1,2}\d{1,3})     # Identificador da tag
    \s+
    (?P<resto>.*)                  # Pares chave=valor restantes
    $
    """,
    re.VERBOSE
    )

@dataclass(frozen=True)
class Registro:
    """Representa uma linha válida do log SCADA.

    Attributes:
        instante: Data e hora da leitura, como `datetime`.
        nivel: Nível registrado no log (`INFO`, `WARN` ou `ALARME`).
        tag: Identificador do instrumento ou equipamento.
        valores: Pares chave-valor; valores numéricos são `float` e os demais, `str`.
    """

    instante: datetime
    nivel: str
    tag: str
    valores: dict[str, float | str]


def valida_tag(tag: str) -> bool:
    """Verifica se `tag` inteira segue o formato de identificador SCADA.

    Args:
        tag: Texto a validar.

    Returns:
        `True` para uma ou duas letras maiúsculas seguidas de um a três dígitos;
        `False` para qualquer outro texto.

    Raises:
        TypeError: Se `tag` não for uma string.
    """
    return bool(re.fullmatch(r"[A-Z]{1,2}\d{1,3}", tag))


def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Converte as linhas reconhecidas do log em registros e separa as inválidas.

    Args:
        texto: Conteúdo do log, com uma linha por registro.

    Returns:
        Tupla `(registros, invalidas)`. `registros` contém as linhas com formato e tag
        válidos; `invalidas` contém, sem alteração, as linhas que não correspondem ao
        formato ou cuja tag é inválida. Linhas sem pares `chave=valor` continuam válidas.

    Raises:
        TypeError: Se `texto` não for uma string.
        ValueError: Se uma linha tiver formato reconhecido, mas contiver data ou hora
            impossível de converter em `datetime`.
    """
    registros = []
    invalidas = []

    if not texto.strip():
        return registros, invalidas

    for linha in texto.splitlines():
        m = LINHA.fullmatch(linha)
        if not m or not valida_tag(m["tag"]):
            invalidas.append(linha)
            continue

        instante = datetime.strptime(f"{m['data']} {m['hora']}", "%Y-%m-%d %H:%M:%S")

        valores = {}
        if m["resto"].strip():
            for item in m["resto"].split():
                if "=" in item:
                    chave, val_str = item.split("=", 1)
                    try:
                        valores[chave] = float(val_str)
                    except ValueError:
                        valores[chave] = val_str

        registros.append(
            Registro(
                instante=instante,
                nivel=m["nivel"],
                tag=m["tag"],
                valores=valores
            )
        )

    return registros, invalidas


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Seleciona os registros de uma tag, preservando a ordem de entrada.

    Args:
        registros: Registros a pesquisar.
        tag: Identificador a selecionar.

    Returns:
        Nova lista com os registros cujo atributo `tag` é igual a `tag`; vazia se não
        houver correspondências.
    """
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Conta quantos registros existem para cada tag.

    Args:
        registros: Registros a agrupar.

    Returns:
        Dicionário `{tag: quantidade}` para as tags presentes; vazio se a entrada for vazia.
    """
    tags = {r.tag for r in registros}
    return {tag: sum(1 for r in registros if r.tag == tag) for tag in tags}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """Extrai valores de uma chave dos registros de uma tag.

    Args:
        registros: Registros a consultar.
        tag: Identificador dos registros selecionados.
        chave: Chave cujo valor será extraído.

    Returns:
        `SerieTemporal` com os valores encontrados, na ordem original; registros sem a chave
        são ignorados.

    Raises:
        ValueError: Se os valores encontrados não puderem ser convertidos para uma série
            unidimensional de números.
    """
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
    """Cria uma função de conversão para cada fator associado a uma tag.

    Args:
        escalas: Dicionário de tags e fatores multiplicativos.

    Returns:
        Dicionário `{tag: conversor}`. Cada conversor recebe uma contagem e devolve seu
        produto pelo fator da tag, capturado no momento da criação.
    """
    return {tag: (lambda c, f=fator: c * f) for tag, fator in escalas.items()}


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Mede os bytes usados por representações comuns de contagens.

    Args:
        contagens: `ndarray` unidimensional de inteiros, esperado no intervalo de 0 a 4095.

    Returns:
        Dicionário com exatamente estas chaves e o número de bytes correspondente:

    - `"list"`: a lista `contagens.tolist()`; o total é `sys.getsizeof(lista)` mais a soma de
      `sys.getsizeof(x)` para cada elemento `x`;
    - `"array('H')"`: um `array.array("H", ...)`; conte só os dados (`itemsize * len`);
    - `"uint16"`, `"int32"`, `"int64"`, `"float32"`, `"float64"`: o `ndarray` convertido para
      esse `dtype`; conte só os dados (atributo `.nbytes`).

    Raises:
        ValueError: Se `contagens` não for um `ndarray` unidimensional de inteiros.
        OverflowError: Se algum elemento não puder ser representado pelo tipo `array('H')`.
    """
    if (not isinstance(contagens, np.ndarray)
        or contagens.ndim != 1
        or not np.issubdtype(contagens.dtype, np.integer)
    ):
        raise ValueError("contagens deve ser um ndarray 1D de inteiros")
    
    lista = contagens.tolist()
    mem_list = sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)

    arr_h = array.array('H', contagens)
    mem_arr_h = arr_h.itemsize * len(arr_h)

    return {
        "list": mem_list,
        "array('H')": mem_arr_h,
        "uint16": contagens.astype(np.uint16).nbytes,
        "int32": contagens.astype(np.int32).nbytes,
        "int64": contagens.astype(np.int64).nbytes,
        "float32": contagens.astype(np.float32).nbytes,
        "float64": contagens.astype(np.float64).nbytes
    }


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte uma lista de contagens em pressões nominais usando um laço.

    Args:
        contagens: Contagens inteiras do conversor A/D.

    Returns:
        Nova lista com `c * 600 / 4095` para cada contagem, em kPa.
    """
    resultado = []
    for c in contagens:
        resultado.append(c * 600 / 4095)
    return resultado


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte uma lista de contagens em pressões nominais por compreensão.

    Args:
        contagens: Contagens inteiras do conversor A/D.

    Returns:
        Nova lista com `c * 600 / 4095` para cada contagem, em kPa.
    """
    return [c * 600 / 4095 for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte uma lista de contagens em pressões nominais usando `map`.

    Args:
        contagens: Contagens inteiras do conversor A/D.

    Returns:
        Nova lista com `c * 600 / 4095` para cada contagem, em kPa.
    """
    return list(map(lambda c: c * 600 / 4095, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em pressões nominais com uma operação vetorizada.

    Args:
        contagens: Array NumPy de contagens.

    Returns:
        Novo array com `c * 600 / 4095` aplicado elemento a elemento, em kPa.
    """
    return contagens * 600 / 4095


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Mede o tempo médio das quatro implementações de conversão.

    Args:
        contagens: Array NumPy fornecido à conversão vetorizada; uma lista correspondente
            é criada uma única vez para as outras implementações.
        k: Número de execuções cronometradas para cada implementação.

    Returns:
        Dicionário de tempos médios em segundos, com as chaves `"laço"`, `"compreensão"`,
        `"map+lambda"` e `"vetorizado"`.

    Raises:
        ValueError: Se `contagens` não for um `ndarray` ou se `k` não for positivo.
    """
    if not isinstance(contagens, np.ndarray):
        raise ValueError("contagens deve ser um ndarray 1D")
    
    lista = contagens.tolist()

    return {
        "laço": cronometrar(converter_laco, lista, k=k),
        "compreensão": cronometrar(converter_compreensao, lista, k=k),
        "map+lambda": cronometrar(converter_map, lista, k=k),
        "vetorizado": cronometrar(converter_vetorizado, contagens, k=k),
    }
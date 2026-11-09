""""Leitura do log SCADA da estação elevatória e preparação dos dados.

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
    ^ # início da linha
    (?P<data>\d{4}-\d{2}-\d{2}) # AAAA-MM-DD
    \s+ # um ou mais espaços
    (?P<hora>\d{2}:\d{2}:\d{2}) # HH:MM:SS
    \s+ # um ou mais espaços
    (?P<nivel>INFO|WARN|ALARME) # nível
    \s+ # um ou mais espaços
    (?P<tag>[A-Z]{1,2}\d{1,3}) # tag
    \s+ # um ou mais espaços
    (?P<resto>\S.*) # resto da linha, começando por um caractere que não é espaço
    $ # fim da linha
    """,
    re.VERBOSE
)

@dataclass(frozen=True)
class Registro:
    """Uma linha válida do log: instante, nível, tag e os pares chave=valor convertidos."""

    instante: datetime
    nivel: str
    tag: str
    valores: dict[str, float | str]


def valida_tag(s: str) -> bool:
    """Verifica se a string segue o padrão de tag esperado.

    Args:
        s: String candidata a tag.

    Returns:
        `True` quando a string contém 1 ou 2 letras maiúsculas seguidas de
        1 a 3 dígitos; caso contrário, `False`.
    """

    resposta: re.Match | None = re.fullmatch(r"^[A-Z]{1,2}\d{1,3}$", s)
    return resposta is not None

def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Lê o log e separa linhas válidas das inválidas.

    Args:
        texto: Conteúdo completo do log em texto.

    Returns:
        Tupla `(registros, invalidas)`, em que:
            - `registros` contém os objetos `Registro` construídos a partir
              das linhas válidas;
            - `invalidas` contém as linhas rejeitadas, na ordem original.
    """
    registros = []
    invalidas = []
    linhas = texto.splitlines()
    for linha in linhas:
        if not linha.strip():
            continue  # ignora linhas vazias

        match: re.Match | None = re.fullmatch(LINHA, linha)

        if match is None:
            invalidas.append(linha)
            continue

        if not valida_tag(match.group('tag')):
            invalidas.append(linha)
            continue

        grupo: dict[str, str] = match.groupdict()

        parPattern = re.compile(r"(\w+)=(\S+)")
        pares = parPattern.findall(grupo['resto'])

        valores = {
            chave: float(valor) if valor.replace('.', '', 1).isdigit() else valor
            for chave, valor in pares
        }

        registros.append(
            Registro(
                instante=datetime.strptime(f"{grupo['data']} {grupo['hora']}", "%Y-%m-%d %H:%M:%S"),
                nivel=grupo['nivel'],
                tag=grupo['tag'],
                valores=valores,
            )
        )

    return registros, invalidas

def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Filtra os registros de uma tag específica.

    Args:
        registros: Lista de registros de entrada.
        tag: Tag a ser mantida no resultado.

    Returns:
        Lista contendo apenas os registros cuja tag é igual a `tag`.
    """
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Conta registros por tag.

    Args:
        registros: Lista de registros a ser agregada.

    Returns:
        Dicionário no formato `{tag: quantidade}`.
    """

    setTags = {r.tag for r in registros}
    return {tag: len(por_tag(registros, tag)) for tag in setTags}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """Extrai uma série temporal de uma chave para uma tag.

    Args:
        registros: Lista de registros de entrada.
        tag: Tag que seleciona os registros relevantes.
        chave: Chave cujo valor será coletado em cada registro selecionado.

    Returns:
        `SerieTemporal` com os valores encontrados para `chave` na tag
        informada, preservando a ordem de aparição.
    """

    valores = [r.valores[chave] for r in registros if r.tag == tag and chave in r.valores]
    serie = SerieTemporal.de_lista(valores)

    return serie


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Cria funções de conversão por tag.

    Args:
        escalas: Dicionário no formato `{tag: fator}`.

    Returns:
        Dicionário no formato `{tag: f}` em que cada função aplica
        `f(c) = c * fator` usando o fator da própria tag.
    """
    conversores = {}
    for tag, fator in escalas.items():
        conversores[tag] = lambda c, f=fator: c * f
    return conversores


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------

def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Mede o uso de memória de contagens em diferentes representações.

    Args:
            contagens: `ndarray` 1D de inteiros com valores de contagem.

    Returns:
            Dicionário com os bytes ocupados por cada representação, com as chaves:
            `"list"`, `"array('H')"`, `"uint16"`, `"int32"`, `"int64"`,
            `"float32"` e `"float64"`.

    Raises:
            ValueError: Se `contagens` não for um `ndarray` 1D de inteiros.
    """
    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("contagens deve ser um ndarray 1D de inteiros")

    lista = contagens.tolist()
    array_h = array.array('H', contagens)
    return {
        "list": sum(sys.getsizeof(x) for x in lista) + sys.getsizeof(lista),
        "array('H')": array_h.itemsize * len(array_h),
        "uint16": np.array(contagens, dtype=np.uint16).nbytes,
        "int32": np.array(contagens, dtype=np.int32).nbytes,
        "int64": np.array(contagens, dtype=np.int64).nbytes,
        "float32": np.array(contagens, dtype=np.float32).nbytes,
        "float64": np.array(contagens, dtype=np.float64).nbytes
    }

def converter_laco(contagens: list[int]) -> list[float]:
   """Converte contagens em kPa com laço explícito.

   Args:
       contagens: Lista de contagens inteiras.

   Returns:
       Lista de pressões em kPa calculadas por `c * 600 / 4095`.
   """
   contagens_kpa = []
   for c in contagens:
       contagens_kpa.append(c * 600/4095)
   return contagens_kpa

def converter_compreensao(contagens: list[int]) -> list[float]:
   """Converte contagens em kPa com compreensão de lista.

   Args:
       contagens: Lista de contagens inteiras.

   Returns:
       Lista de pressões em kPa calculadas por `c * 600 / 4095`.
   """
   return [c * 600 / 4095 for c in contagens]

def converter_map(contagens: list[int]) -> list[float]:
   """Converte contagens em kPa com `map` e `lambda`.

   Args:
       contagens: Lista de contagens inteiras.

   Returns:
       Lista de pressões em kPa calculadas por `c * 600 / 4095`.
   """
   contagens_kpa = list(map(lambda c: c*600/4095, contagens))
   return contagens_kpa

def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
   """Converte contagens em kPa com operação vetorizada do NumPy.

   Args:
       contagens: `ndarray` com contagens.

   Returns:
       `ndarray` com pressões em kPa calculadas por `c * 600 / 4095`.
   """
   contagens_kpa = contagens*600/4095
   return contagens_kpa

def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
   """Mede o tempo médio de cada estratégia de conversão.

   Args:
       contagens: `ndarray` com as contagens de entrada.
       k: Número de repetições usadas em cada medição.

   Returns:
       Dicionário de tempos médios em segundos com as chaves `"laço"`,
       `"compreensão"`, `"map+lambda"` e `"vetorizado"`.
   """
   ret = {}
  
   listContagens = contagens.tolist()
  
   ret["laço"] = cronometrar(converter_laco, listContagens, k=k)
   ret["compreensão"] = cronometrar(converter_compreensao, listContagens, k=k)
   ret["map+lambda"] = cronometrar(converter_map, listContagens, k=k)
   ret["vetorizado"] = cronometrar(converter_vetorizado, contagens, k=k)
  
   return ret



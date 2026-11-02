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
    (?P<data>\d{4}-\d{2}-\d{2})\s+ #0000-00-00
    (?P<hora>\d{2}:\d{2}:\d{2})\s+ #00-00-00
    (?P<nivel>INFO|WARN|ALARME)\s+
    (?P<tag>[A-Z]{1,2}[0-9]{1,3})\s+ #AA-000
    (?P<resto>.+)
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
    """Verifica se uma tag é válida ou não.
    Args:
        Linha: Uma string que é a tag.
    Returns:
        Retorna True se a tag for válida e False caso contrário.
    """
    PADRAO_TAG = r"[A-Z]{1,2}[0-9]{1,3}"
    b = re.fullmatch(PADRAO_TAG,s)
    if b is None:
        return False
    else:
        return True

def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Essa função lê o log e separa ele em duas listas.
    Args:
        Texto do Log: Uma string que foi gerado pelo sistema que contém as informações
        de data, hora, nivel, tag.
    Returns:
        Registro: Uma lista que contém todos os logs válidos.
        Invalidas: Uma lista que contém logs que não passaram por alguma condição de validade
        EX: log vazio, data impossível, tag invalida.
    """
    registro = []
    invalidas = []
    PADRAO_RESTO = re.compile(r"\w+=\S+(?:\s+\w+=\S+)*")
    for linha in texto.split("\n"):
        if not linha.strip():
            continue
        ver = re.fullmatch(LINHA, linha)
        if ver is None:
            invalidas.append(linha)
            continue
        data = ver.group("data")
        hora = ver.group("hora")
        nivel = ver.group("nivel")
        tag = ver.group("tag")
        resto = ver.group("resto")
        if not valida_tag(tag):
            invalidas.append(linha)
            continue
        try:
            instante = datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            invalidas.append(linha)
            continue
        if not PADRAO_RESTO.fullmatch(resto):
            invalidas.append(linha)
            continue
        valores = {}
        for chave, valor in re.findall(r"(\w+)=(\S+)", resto):
            try:
                valores[chave] = float(valor)
            except ValueError:
                valores[chave] = valor
        registro.append(Registro(instante, nivel, tag, valores))
    return registro, invalidas
        
def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """A partir dos registros conta quantas vezez cada tag apareceu no registro.
    Args:
        Registros: Contém todos os registro válidos.
    Returns:
        Retorna um dicionário que tem como chave as tags e como valores quantas vezes cada tag apareceu no registro."""
    tags = {r.tag for r in registros}
    dicionario = {tag:sum(1 for i in registros if i.tag == tag) for tag in tags}
    return dicionario



def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """Cria uma série temporal com os valores de chave dos registros da tag."""
    valores = [r.valores[chave] for r in registros if r.tag == tag and chave in r.valores]
    return SerieTemporal.de_lista(valores)

# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """A função criar conversores retorna, a partir de uma escalas que contém as tags e seus respectivos fatores de conversão,
    retorna um dicionário que tem como chaves as tags e suas respectivas funções de conversão.
    Essas funções foram implementadas usando a compreensão para criar o dicionário e usando também funções lambdas."""
    return {tag: (lambda c, fator = fat: c * fator) for tag, fat in escalas.items()}


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Essa função mede a memória de uma contagem.
    Args:
        Recebe como parâmetro uam nparray.
    Returns:
        Retorna um dicionario [str,float] onde a chave representa a estrutura que a contagem esta armazenada internamente e a
        memória que ela ocupa."""
    if isinstance(contagens, np.ndarray) and contagens.ndim == 1 and np.issubdtype(contagens.dtype,np.integer):
        contagemArr = array.array("H",contagens)
        lista = contagens.tolist()
        dicionario = {"list": sys.getsizeof(lista)+sum([sys.getsizeof(x) for x in lista]),
                    "array('H')": contagemArr.itemsize*len(contagemArr),
                    "uint16": contagens.astype(np.uint16).nbytes,
                    "int32": contagens.astype(np.int32).nbytes,
                    "int64": contagens.astype(np.int64).nbytes,
                    "float32": contagens.astype(np.float32).nbytes,
                    "float64": contagens.astype(np.float64).nbytes}
        return dicionario
    raise ValueError("Contagens não é 1D de inteiros.")

def converter_laco(contagens: list[int]) -> list[float]:
    """Para converter a lista de inteiros em kPa (floats)
    essa função cria uma lista vazia e adiciona item por item da lista original.
    Args:
        List: Uma lista de inteiros.
    Returns:
        List: Uma lista de float"""
    lista = []
    for c in contagens:
        lista.append(float(c*600/4095))
    return lista


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Usando compreensão de lista, essa função retorna uma lista com os valores
    convertidos.
    Args:
        List: Uma lista de inteiros.
    Returns:
        List: Uma lista de float"""
    return [float(c*600/4095) for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte a lista original usando o map() e função lambda.
    Args:p
        List: Uma lista de inteiros.
    Returns:
        List: Uma lista de float"""
    return list(map(lambda c: c*600/4095, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte uma array de inteiros em uma array de floats (kPa)
    Args:
        List:Uma array de inteiros.
    Returns:
        List: Uma arrat de float"""
    return contagens * 600/4095


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Essa função cria um dicionário [nome da função, tempo médio de execução]
    para cada tipo de conversão.
    Args:
        Uma array e um parametro k que é quantas vezes realizamos a chamada da função.
    Returns:
        """
    lista = contagens.tolist()
    dicionario = {}
    metodos = {"laço": converter_laco,"compreensão": converter_compreensao,"map+lambda": converter_map}
    for nome, função in metodos.items():
        dicionario[nome] = cronometrar(função,lista,k=k)
    dicionario["vetorizado"] = cronometrar(converter_vetorizado,contagens,k=k)
    return dicionario
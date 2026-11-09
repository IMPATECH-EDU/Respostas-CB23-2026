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

LINHA: re.Pattern = re.compile(
    r"""
    ^(?P<data>\d{4}-\d{2}-\d{2}) # Data no formato AAAA-MM-DD
    \s+  # Um ou mais espaços
    (?P<hora>\d{2}:\d{2}:\d{2}) # Hora no formato HH:MM:SS
    \s+  # Um ou mais espaços
    (?P<nivel>INFO|WARN|ALARME) # Nível do registro
    \s+  # Um ou mais espaços
    (?P<tag>[A-Z]{1,2}\d{1,3}) # Tag: 1 ou 2 letras maiúsculas seguidas de 1 a 3 dígitos
    \s+  # Um ou mais espaços
    (?P<resto>\S.*)$ # O restante da linha
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
    """`True` se a string inteira for uma tag válida (1 ou 2 maiúsculas e 1 a 3 dígitos).
    """
    return re.fullmatch(r"[A-Z]{1,2}\d{1,3}",s) is not None


def ler_log(texto: str) -> tuple[list[Registro], list[str]]:
    """Lê o texto do log e devolve `(registros, invalidas)`.
    - `registros`: lista de `Registro`, na ordem em que as linhas aparecem no texto;
    - `invalidas`: lista das linhas descartadas, exatamente como estavam no texto.
    """
    if not texto:
        return ([], [])

    registros : list[Registro] = []
    invalidas : list[str] = []

    for linha in texto.splitlines():
        linha_strip = linha.strip()

        if not linha_strip:
            continue #linha com somente espaços vazios ou vazia

        m = LINHA.fullmatch(linha)

        if not m:
            invalidas.append(linha)
            continue

        data_str = m.group("data")
        hora_str = m.group("hora")
        nivel_str = m.group("nivel")
        tag_str = m.group("tag")
        resto_str = m.group("resto")

        #Validação de data e hora
        
        try:
            instante = datetime.strptime(f"{data_str} {hora_str}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            invalidas.append(linha)
            continue

        #Pares de chave e valor

        pares = re.findall(r"(\w+)=(\S+)", resto_str)

        if not pares:
            invalidas.append(linha)
            continue

        valores : dict[str, float | str] = {}

        for chave, vlr_str in pares:
            try:
                valores[chave] = float(vlr_str)
            except ValueError:
                valores[chave] = vlr_str

        registros.append(Registro(instante=instante,nivel=nivel_str,tag=tag_str,valores=valores))

    return (registros,invalidas)


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros."""
    tags = {r.tag for r in registros}
    return {t: sum(1 for r in registros if r.tag == t) for t in tags}
    


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave."""

    valores = [
        float(r.valores[chave])
        for r in registros
        if r.tag == tag and chave in r.valores
    ]
    return SerieTemporal.de_lista(valores)


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag."""
    return {tag: (lambda c, f=fator: c * f) for tag, fator in escalas.items()}


# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]:
    """Bytes ocupados pelas `contagens` (ndarray 1D de inteiros de 0 a 4095) em cada estrutura."""

    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("contagens deve ser um ndarray 1D de inteiros")

    lst = contagens.tolist()
    bytes_list =  sys.getsizeof(lst) + sum(sys.getsizeof(x) for x in lst)

    arr_h = array.array("H", contagens)
    bytes_arr_h = arr_h.itemsize * len(arr_h)

    dict_res = {
        "list" : bytes_list,
        "array('H')" : bytes_arr_h,
    }

    dtypes = ["uint16","int32","int64","float32","float64"]

    for dt in dtypes:
        dict_res[dt] = contagens.astype(dt).nbytes

    return dict_res



def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""

    list_res = []

    for c in contagens:
        list_res.append(c * 600.0 / 4095.0)

    return list_res


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""

    return [c * 600.0 / 4095.0 for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""

    return list(map(lambda c: c * 600.0 / 4095.0, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""

    return contagens * 600.0 / 4095.0


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições."""

    lst = contagens.tolist()

    t_laco = sum(cronometrar(converter_laco, lst) for _ in range(k)) / k
    t_comp = sum(cronometrar(converter_compreensao, lst) for _ in range(k)) / k
    t_map = sum(cronometrar(converter_map, lst) for _ in range(k)) / k
    t_vet = sum(cronometrar(converter_vetorizado,contagens) for _ in range(k)) / k

    return {
        "laço": t_laco,
        "compreensão": t_comp,
        "map+lambda": t_map,
        "vetorizado": t_vet,
    }

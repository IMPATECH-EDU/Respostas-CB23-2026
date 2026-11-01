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

# vamos alterar essa linha debaixo para atender ao padrão pedido acima.


LINHA: re.Pattern = re.compile(
    r"""
    (?P<data>\d{4}-\d{2}-\d{2})    # Data no formato AAAA-MM-DD para ANO-MêS-DIA
    [ ]+                           # Espaço 1+
    (?P<hora>\d{2}:\d{2}:\d{2})    # Hora no formato HH:MM:SS para HORA-MINUTO-SEGUNDO
    [ ]+                           # Espaço 1+
    (?P<nivel>INFO|WARN|ALARME)    # Nível
    [ ]+                           # Espaço 1+
    (?P<tag>[A-Z]{1,2}\d{1,3})     # Tag: 1 ou 2 letras maiúsculas e 1 a 3 dígitos
    [ ]+                           # Espaço 1+
    (?P<resto>\S.*)                # Resto da linha, iniciando com um não-espaço
    """,
    re.VERBOSE,
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

    Use `fullmatch`. Válidas: `"PT101"`, `"FT201"`, `"B1"`. Inválidas: `"pt101"`, `"PT"`,
    `"PT1010"`, `"101PT"` e `"PT101 "` (sobra de caracteres).
    """
    return bool(re.fullmatch(r"[A-Z]{1,2}\d{1,3}", s)) # Vamos testar assim, lembrando que o antigo era:
    # raise NotImplementedError("issue #1: valida_tag")
    # O que está sendo feito agora? Basicamente, se utilizássemos o re.match, ele verificaria apenas o início da string.
    # Então, se a string fosse inválida, mas começasse com uma tag válida, o re.match ainda assim retornaria um match. Dessa forma, utilizaremos
    # o re.fullmatch, que verifica se toda a string corresponde ao padrão esperado. 


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
        if not linha.strip(): # Se a linha estiver vazia, só com espaços em branco, pularemos para a próxima linha.
            continue
        if not (linha_boa:= LINHA.fullmatch(linha)): # Se a linha não casar com o padrão, adicionamos ela à lista de inválidas e pulamos para a próxima.
            invalidas.append(linha)
            continue
        instante_log = datetime.strptime(f"{linha_boa['data']} {linha_boa['hora']}", "%Y-%m-%d %H:%M:%S") # Montado o instante com a data e hora linha válida.
        try:
            instante_log = datetime.strptime(
                f"{linha_boa['data']} {linha_boa['hora']}", "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            invalidas.append(linha)
            continue
        if not (pares:= re.findall(r"(\w+)=(\S+)", linha_boa['resto'])): # Aqui vamos mapear pares chave=valor no grupo 'resto'. Se não tiver nenhum, a linha é inválida.
            invalidas.append(linha)
            continue
        valores: dict[str, float | str] = {} 
        for chave, valor in pares:
            try:
                valores[chave] = float(valor) # Convertendo para float quando possível.
            except ValueError:
                valores[chave] = valor 
        registros.append(Registro(instante_log, linha_boa["nivel"], linha_boa["tag"], valores))
    return registros, invalidas


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """
    # Primeiro, a compreensão de conjunto para obter todas as tags:
    conjunto_tags = {r.tag for r in registros} 
    # Segundo, a compreensão de dicionário para contar os registros por tag:
    return{tag: len(por_tag(registros, tag)) for tag in conjunto_tags}


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave.

    Os registros da tag sem essa chave (por exemplo, os alarmes de PT102, que não têm
    `contagens`) são ignorados. Crie a série com `SerieTemporal.de_lista`.
    """
    registros_com_tag = por_tag(registros,tag) 
    registros_com_chave = [r for r in registros_com_tag if chave in r.valores] 
    return SerieTemporal.de_lista([r.valores[chave] for r in registros_com_chave])


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag.

    Cada `f` é uma lambda. Cuidado com o *late binding*: cada função deve usar o fator da
    sua tag, e não o último fator do dicionário (veja a issue #2 no enunciado).
    """
    # Cada lambda guarda o seu fator como valor padrão no momento em que é criada. Senão fosse
    # dessa forma, todas iriam usar o último fator, o que causaria late binding.
    return {tag: (lambda c, fator = fator: c * fator) for tag,fator in escalas.items()} 



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
    raise NotImplementedError("issue #3: medir_memoria")


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    raise NotImplementedError("issue #3: converter_laco")


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    raise NotImplementedError("issue #3: converter_compreensao")


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    raise NotImplementedError("issue #3: converter_map")


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    raise NotImplementedError("issue #3: converter_vetorizado")


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).
    """
    raise NotImplementedError("issue #3: medir_tempos")

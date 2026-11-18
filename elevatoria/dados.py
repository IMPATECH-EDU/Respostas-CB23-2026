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
LINHA: re.Pattern = re.compile(r"""
    (?P<data>\d{4}-\d{2}-\d{2})           \s+#data
    (?P<hora>\d{2}:\d{2}:\d{2})           \s+#hora
    (?P<nivel>\b(INFO|WARN|ALARME)\b)     \s+#nivel
    (?P<tag>[A-Z]{1,2}\d{1,3})            \s*#tag                                 #Remove espaços
    (?P<resto>.*)                         #resto
    """,
    re.VERBOSE
) # type: ignore[assignment]  # TODO issue #1


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

    ref = re.compile('[A-Z]{1,2}\d{1,3}')
    return(re.fullmatch(ref, s))

    raise NotImplementedError("issue #1: valida_tag")

def bissexto(ano:int):
    if (ano//4==0 and ano//100!=0) or ano//400==0:
        return(True)
    return(False)


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

    if texto == '':
        return([], [])
    
    registros = []
    invalidas = []

    linhas = texto.split('\n')

    for linha in linhas:
        match = re.fullmatch(LINHA,linha)


        if match:

            if int(match.group('data')[5:7])<1 or int(match.group('data')[5:7])>12:
                invalidas.append(linha)

                
            elif int(match.group('data')[8:10])<1 or int(match.group('data')[8:10])>32:
                invalidas.append(linha)
                break

            elif bissexto(int(match.group('data')[0:4])):
                if int(match.group('data')[5:7])==2 and int(match.group('data')[8:10])>29:
                    invalidas.append(linha)
                    
            elif int(match.group('data')[5:7])==2 and int(match.group('data')[8:10])>28:
                invalidas.append(linha)
                
            elif int(match.group('data')[5:7]) in [4, 6, 9, 11] and int(match.group('data')[8:10])>30:
                invalidas.append(linha)


            elif int(match.group('hora')[0:2])>23 or int(match.group('hora')[3:5])>60 or int(match.group('hora')[6:8])>60:
                invalidas.append(linha)


            elif not re.fullmatch(r"((\w+)=(\S+)\s*)+", match.group('resto')):
                invalidas.append(linha)

            else:

                string = match.group('data') + ' ' + match.group('hora')
                datahora = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

                items = match.group('resto').split('=')
                dicionario = {}
                instante = datahora
                nivel = match.group('nivel')  
                tag = match.group('tag')
                for i in range (int(len(items)/2)):
                    dicionario[items[2*i].strip()] = items[2*i+1].strip()
                valores = dicionario

                registro = Registro(instante, nivel, tag, valores)

                registros.append(registro)
                    

        elif re.fullmatch(r'^\s*$', linha):
            pass
        else:
            invalidas.append(linha)

    return(registros, invalidas)


    raise NotImplementedError("issue #1: ler_log")


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """

    if not registros:
        return({})

    tags = {registro.tag for registro in registros}
    qtd = {tag: sum(1 for registro in registros if registro.tag==tag) for tag in tags}
    return(qtd)

    raise NotImplementedError("issue #1: contagem_por_tag")

def contagem_por_nivel(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """

    if not registros:
        return({})

    niveis = {registro.nivel for registro in registros}
    qtd = {nivel: sum(1 for registro in registros if registro.nivel==nivel) for nivel in niveis}
    return(qtd)

def total(registros: list[Registro]):

    vetor = serie(registros, 'FT201', 'pulsos')
    soma = sum(vetor)
    return(soma)

def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave.

    Os registros da tag sem essa chave (por exemplo, os alarmes de PT102, que não têm
    `contagens`) são ignorados. Crie a série com `SerieTemporal.de_lista`.
    """
    lista = [(registro.valores[chave]) for registro in registros if registro.tag == tag and chave in registro.valores ]
    serie = SerieTemporal.de_lista(lista)
    return(serie)
    raise NotImplementedError("issue #1: serie")


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag.
    Cada `f` é uma lambda. Cuidado com o *late binding*: cada função deve usar o fator da
    sua tag, e não o último fator do dicionário (veja a issue #2 no enunciado).
    """

    retorno = {}

    for key in escalas:
        f = lambda x: x*escalas[key]
        retorno[key: f]

    return retorno

def por_tag_instante(registros):
    return(sorted(registros, key=lambda x:(x.tag, x.instante)))

def decrescente(registros):
    return(sorted(registros, reverse=True,key=lambda x: x.instante))

    raise NotImplementedError("issue #2: criar_conversores")


def com_map(registros):
    return(list(filter(lambda x: x.tag == 'PT102' and 'contagens' in x.valores , registros )))

def com_compreensao(registros):
    return([registro for registro in registros if(registro.tag=='PT102' and 'contagens' in registro.valores)])


def altas(registros):
    return(list(filter(lambda x: int(x.valores['contagens'])>2000, com_map(registros))))

def tags(registros):
    return({registro.tag for registro in registros})

def conversao(texto):
    return(re.sub(r'(pulsos=)(\d+)', lambda x: 'volume_L='+str(int(x.group(2))*0.1), texto))



def criar_conversores(escalas):
    retorno = {}
    for tag in escalas:
        retorno[tag] =  lambda x, tag=tag: x*escalas[tag]

    return(retorno)


def media_convert(registros, fator):
    vetor=serie(list(filter(lambda x: int(x.valores['contagens'])<=2000, com_map(registros))), 'PT102', 'contagens')
    return(sum(list(map(fator, vetor)))/len(vetor))



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

    if not (isinstance(contagens, np.ndarray) and contagens.ndim == 1 and np.issubdtype(contagens.dtype, np.integer)):
        raise ValueError

    lista = contagens.tolist()
    size_lista = sys.getsizeof(lista) + sum(sys.getsizeof(i) for i in lista)

    arr = array.array('H', (i for i in contagens))
    size_arr = sys.getsizeof(arr[0])*len(arr)

    i_16 = np.array(arr)
    sizei_16 = i_16.nbytes

    i_32 = i_16.astype(np.int32)
    sizei_32 = i_32.nbytes

    i_64 = i_16.astype(np.int64)
    sizei_64 = i_64.nbytes


    f_32 = i_16.astype(np.float32)
    sizef_32 = f_32.nbytes
    
    f_64 = i_16.astype(np.float64)
    sizef_64 = f_64.nbytes
    
    dici = {'list':size_lista, 'array':size_arr, 'uint16': sizei_16,  'int32':sizei_32, 
            'int64': sizei_64, 'float32': sizef_32, 'float64': sizef_64}

    print()
    print(f"{'Tipo / dtype':<12} | {'Tamanho (Bytes)':<15}")
    print("-" * 32)
    for tipo in dici:
        print(f"{tipo:<12} | {dici[tipo]:<15,}".replace(",", "."))

    return(dici)
    raise NotImplementedError("issue #3: medir_memoria")


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    lista = []
    for i in contagens:
        lista.append(i*600/4095)

    return(lista)
    raise NotImplementedError("issue #3: converter_laco")


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""

    lista = [i*600/4095 for i in contagens]
    return(lista)
    raise NotImplementedError("issue #3: converter_compreensao")


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""

    lista = list(map(lambda x: x*600/4095, contagens))
    return(lista)
    raise NotImplementedError("issue #3: converter_map")


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    lista = contagens*(600/4095)
    return(lista)

    raise NotImplementedError("issue #3: converter_vetorizado")


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).
    """
    lista = contagens.tolist()
    t_laco = cronometrar(converter_laco, (lista))
    t_comp = cronometrar(converter_compreensao, (lista))
    t_map = cronometrar(converter_map, (lista))
    t_arr = cronometrar(converter_vetorizado, (contagens))

    dici = {'laço':t_laco, 'compreensão':t_comp, 'map+lambda':t_map, 'vetorizado':t_arr}

    print()
    print(f"{'Conversão':<12} | {'Tempo(s)':<15}")
    print("-" * 32)
    for tipo in dici:
        print(f"{tipo:<12} | {dici[tipo]:<15,}".replace(",", "."))
    
    return(dici)
    
    raise NotImplementedError("issue #3: medir_tempos")

def print_types(s: SerieTemporal) -> None:

    dici = {'s+s':type(s).__name__, 's[1:]':type(s[1:]).__name__, 's*2':type(s*2).__name__,
            's.sum()':type(s.sum()).__name__, 's[0]':type(s[0]).__name__}

    print()
    print(f"{'Objeto':<12} | {'Tipo':<15}")
    print("-" * 32)
    for objeto in dici:
        print(f"{objeto:<12} | {dici[objeto]:<15}".replace(",", "."))
        
    return()
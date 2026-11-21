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


LINHA = re.compile(
    # Criando o padrão da linha que procuramos com data, hora, nível, tag e resto através de Regex
    
    r"""
    ^
    (?P<data>[0-9]{4}-[0-9]{2}-[0-9]{2})\s+
    (?P<hora>[0-9]{2}:[0-9]{2}:[0-9]{2})\s+
    (?P<nivel>INFO|AVISO|ALARME|ERRO)\s+
    (?P<tag>[A-Z]{1,2}[0-9]{1,3})\s+
    (?P<resto>.+)
    $
    """,
    re.VERBOSE)


@dataclass(frozen=True)
class Registro:
    """Uma linha válida do log: instante, nível, tag e os pares chave=valor convertidos."""

    instante: datetime
    nivel: str
    tag: str
    valores: dict[str, float | str]


def valida_tag(s: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]{1,2}[0-9]{1,3}",s))
    

def ler_log(texto: str) -> tuple[list[Registro], list[str]]:    
    # Criando duas listas para a fuynção devolver
    
    registros = [] # Registros que passaram 
    invalidas = [] # Registros que não passaram

    for linha in texto.splitlines(): # SplitLines quebra todas as linhas e transforma em uma única linha
        if not linha.strip(): # Se a linha for vazia, não ocorre nada, strip quebra os espações
            continue
        match = LINHA.fullmatch(linha) # Se o indice linha, estar no padrão LINHA, então deu match conferido pela função fullmatch
        if match:
            dados = match.groupdict() # Cria um dicionário com os dados que match pega
            if valida_tag(dados["tag"]): # Analisa se a tag está nos padrões desejados
                valores = {}
                data_hora_str = f"{dados['data']} {dados['hora']}"
                instante_dt = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S") # Após converter a string data_hora_str colocamos no padrão dia/hora com datetime
            
                for par in dados["resto"].split(): 
                    chave, valor_raw = par.split('=', 1) #Resto pode estar com algo = string ou algo = float, separa ambos os casos em uma lista
                    try:
                        valor = float(valor_raw)
                    except ValueError:
                        valor = valor_raw 
                    valores[chave] = valor    

                reg = Registro( #Cria a classe Registro para os indices que estão passando
                    instante = instante_dt,
                    nivel = dados["nivel"],
                    tag = dados["tag"],
                    valores = valores
                )
                registros.append(reg)

            else:
                invalidas.append(linha)
        else:
            invalidas.append(linha) # Registrando apenas em invalidas os que não passaram
            
    return registros, invalidas



    

def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    tags = {}
    for r in registros: #Salva a frequência que determinado índice passou na contagem
        if r.tag in tags:
            tags[r.tag] += 1
        else:
            tags[r.tag] = 1
    return tags


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    valores = []
    for i in registros: # Se a tag referente for igual ao Registro correspondente e a chave ja tiver na list valores, salva os valores das tags 
        if i.tag == tag and chave in i.valores:
            valores.append(i.valores[chave])

    return SerieTemporal.de_lista(valores) # Retorna uma Serie Temporal (lista) com os valores contidos na list valores
            

# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    conversores = {}
    for tag, fator in escalas.items(): # Cria um dicionário com tag = função(valor) * c , onde c é escolhido na chamada da função
        conversores[tag] = lambda c, f=fator: c*f 
    return conversores

# ---------------------------------------------------------------------------------------
# Issue #3: memória e tempo
# ---------------------------------------------------------------------------------------
def medir_memoria(contagens: np.ndarray) -> dict[str, int]: 
    # Verificação de ndarray, dimensão = 1 e tipos de elementos na lista 
    if not isinstance(contagens, np.ndarray) or contagens.ndim !=1 or not np.issubdtype(contagens.dtype, np.integer):
        raise ValueError("contagens deve ser um ndarray 1D de inteiros")
    # Converte a ndarray para lista comum do python e armezena a quantidade de memória da lista
    lista = contagens.tolist()
    tamanho_list = sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)
    
    lista_h = array.array("H", contagens)
    tamanho_lista_h = lista_h.itemsize*len(lista_h)

    # Retorna um dicionário com as memórias em bytes de cada tipo
    return {
        "list": tamanho_list,
        "array('H')": tamanho_lista_h,
        "uint16": contagens.astype("uint16").nbytes,
        "int32": contagens.astype("int32").nbytes,
        "int64": contagens.astype("int64").nbytes,
        "float32": contagens.astype("float32").nbytes,
        "float64": contagens.astype("float64").nbytes,
        }
  


def converter_laco(contagens: list[int]) -> list[float]:
    # Conversão com FOR 
    lista_pressao = []
    for valor in contagens:
        lista_pressao.append(float(valor*600/4095))
    return lista_pressao



def converter_compreensao(contagens: list[int]) -> list[float]:
    # Conversão com COMPREENSÃO
    return [float(i*600/4095) for i in contagens]



def converter_map(contagens: list[int]) -> list[float]:
    # Conversão com função map
    return list(map(lambda c: c*600/4095, contagens))
   

def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    # Conversão direta como ndarray é um vetor
    return contagens * 600.0 /4095.0


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    # Tempo para cada método com a importação de cronometrar
    lista_int = contagens.tolist()
    dist = {} 
    dist["laço"] = cronometrar(converter_laco, lista_int, k=k)
    dist["compreensão"] = cronometrar(converter_compreensao, lista_int, k=k)
    dist["map+lambda"] = cronometrar(converter_map, lista_int,k=k)
    dist["vetorizado"] = cronometrar(converter_vetorizado, contagens, k=k)
    
    return dist

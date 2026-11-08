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
    ^                        # Início da linha
    (?P<data>\d{4}-\d{2}-\d{2})  # Data no formato AAAA-MM-DD
    \s+                      # Um ou mais espaços de separação
    (?P<hora>\d{2}:\d{2}:\d{2})  # Hora no formato HH:MM:SS
    \s+                      # Um ou mais espaços de separação
    (?P<nivel>INFO|WARN|ALARME)  # Nível de log (INFO, WARN ou ALARME)
    \s+                      # Um ou mais espaços de separação
    (?P<tag>[A-Z]{1,2}\d{1,3})   # Tag: 1-2 letras maiúsculas + 1-3 dígitos
    \s+                      # Um ou mais espaços de separação
    (?P<resto>\S.*)          # Resto da linha, começando por um caractere não-espaço
    $                        # Fim da linha
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

    # Criamos um novo pattern para as tags
    TAG: re.Pattern = re.compile(r"^[A-Z]{1,2}\d{1,3}$")
    return TAG.fullmatch(s) is not None

def _dict_resto(resto: str) -> dict[str, float | str]:
    """Auxiliar para converter a string do 'resto' em dicionário."""
    resultado: dict[str, float | str] = {}
    
    # Separa por pares chave=valor (lidando com múltiplos espaços entre eles)
    for par in resto.strip().split():
        if "=" in par:
            chave, valor_str = par.split("=", 1)
            # Tenta converter para float; se falhar, mantém como string
            try:
                resultado[chave] = float(valor_str)
            except ValueError:
                resultado[chave] = valor_str
                
    return resultado

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

    # Removemos as linhas vazias ou com espaços
    texto_limpo = re.sub(r"^[^\S\r\n]*\r?\n", "", texto, flags=re.MULTILINE)

    # Listas com as linhas válidas e inválidas
    registros = []
    invalidas = []

    for linha in texto_limpo.splitlines():
        match = LINHA.fullmatch(linha)

        if match:
            # Pega os dados de cada linha
            dados = match.groupdict()

            # Salva no registro
            str_instante = f"{dados['data']} {dados['hora']}"
            instante = datetime.strptime(str_instante, "%Y-%m-%d %H:%M:%S")
            nivel = dados['nivel']
            tag = dados['tag']
            valores = _dict_resto(dados["resto"])

            novo_registro = Registro(
                instante = instante,
                nivel = nivel,
                tag = tag,
                valores = valores
            )
            registros.append(novo_registro)
        else:
            invalidas.append(linha)

    return (registros, invalidas)


def por_tag(registros: list[Registro], tag: str) -> list[Registro]:
    """Registros da `tag`, na ordem original."""
    return [r for r in registros if r.tag == tag]


def contagem_por_tag(registros: list[Registro]) -> dict[str, int]:
    """Dicionário tag -> número de registros.

    Use uma compreensão de dicionário sobre o conjunto das tags, obtido por uma compreensão
    de conjunto. Lista vazia devolve `{}`.
    """

    # Pegamos as tags no registro
    tags = {r.tag for r in registros}

    # Para cada tag em 'tags' comparamos com todas as outras. É meio ineficiente, mas obedece a ideia de dict comprehension
    cont = {tag : sum(1 for r in registros if r.tag == tag) for tag in tags}
    return cont


def serie(registros: list[Registro], tag: str, chave: str) -> SerieTemporal:
    """`SerieTemporal` com o valor de `chave` dos registros da `tag` que têm essa chave.

    Os registros da tag sem essa chave (por exemplo, os alarmes de PT102, que não têm
    `contagens`) são ignorados. Crie a série com `SerieTemporal.de_lista`.
    """

    # Podemos usar list comprehension para fazer a lista otimizada e depois converter em np.array

    valores = [
        r.valores[chave]
        for r in registros
        if r.tag == tag and chave in r.valores
    ]
    return SerieTemporal.de_lista(np.array(valores))


# ---------------------------------------------------------------------------------------
# Issue #2: conversores por tag
# ---------------------------------------------------------------------------------------
def criar_conversores(escalas: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Dado `{tag: fator}`, devolve `{tag: f}`, em que `f(c) = c * fator` da própria tag.

    Cada `f` é uma lambda. Cuidado com o *late binding*: cada função deve usar o fator da
    sua tag, e não o último fator do dicionário (veja a issue #2 no enunciado).
    """

    # Vamos usar dict comprehension. Para evitar o late binding, podemos definir fator = escalas[tag] como default da função
    conv = {
        tag : lambda c, fator = escalas[tag] : c * fator
        for tag in escalas
    }
    return conv


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

    # Verifica se contagens não é um ndarray 1D de inteiros
    if not isinstance(contagens, np.ndarray) or contagens.ndim != 1 or contagens.dtype.kind not in ("i", "u"):
        raise ValueError("contagens deve ser um np.ndarray 1D com elementos inteiros.")
    
    # Processamos os componentes do dicionário:
    lista = contagens.tolist()
    t_lista = sys.getsizeof(lista) + sum(sys.getsizeof(x) for x in lista)

    array_h = array.array("H", contagens)
    t_array_h = array_h.itemsize * len(array_h)

    d_types = ['uint16', 'int32', 'int64', 'float32', 'float64']

    # Criamos o dicionário:

    dict_final = {
        "list" : t_lista,
        "array('H')" : t_array_h
    }

    # Adicionando os tipos restantes usando dict comprehension:
    dict_final.update({dt : contagens.astype(dt).nbytes for dt in d_types})

    return dict_final


def converter_laco(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `for` e `append`."""
    cont_final = []
    for c in contagens:
        cont_final.append(c * 600.0 / 4095.0)

    return cont_final


def converter_compreensao(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma compreensão de lista."""
    return [c * 600.0 / 4095.0 for c in contagens]


def converter_map(contagens: list[int]) -> list[float]:
    """Converte contagens em kPa (`c * 600 / 4095`) com `map` e uma lambda."""
    return list(map(lambda c : c * 600.0 / 4095.0, contagens))


def converter_vetorizado(contagens: np.ndarray) -> np.ndarray:
    """Converte contagens em kPa (`c * 600 / 4095`) com uma operação vetorizada do NumPy."""
    return contagens * 600 / 4095


def medir_tempos(contagens: np.ndarray, k: int = 10) -> dict[str, float]:
    """Tempo médio (s) de cada versão da conversão, em `k` repetições.

    Use `cronometrar` (de `fornecido.cronometro`). Chaves: `"laço"`, `"compreensão"` e
    `"map+lambda"` (que recebem a lista `contagens.tolist()`, criada uma única vez, fora da
    medição) e `"vetorizado"` (que recebe o próprio `ndarray`).
    """

    # Criamos a lista contagens.tolist() antes do laço
    lista = contagens.tolist()

    # Inserimos cada um no dicionário com os parâmetros certos
    dict_final = {
        "laço" : cronometrar(converter_laco, lista, k=k),
        "compreensão" : cronometrar(converter_compreensao, lista, k=k),
        "map+lambda" : cronometrar(converter_map, lista, k=k),
        "vetorizado" : cronometrar(converter_vetorizado, contagens, k=k)
    }

    return dict_final

"""Ponto de operação da bomba e diagnóstico dos métodos de raiz (issue #8).

Este módulo junta peças que já existem na base:

- `CurvaCalibracao` (de `elevatoria/calibracao.py`, Marco 2): a curva da bomba, interpolada
  a partir do ensaio;
- `Tubulacao` (de `fornecido/hidraulica.py`, da equipe de hidráulica): a curva do sistema;
- `Bisseccao` e `Newton` (de `elevatoria/raizes.py`, escritos por um colega): os métodos de
  raiz, que devolvem um `ResultadoRaiz`.

As funções marcadas com `NotImplementedError` são a issue #8; as docstrings descrevem o
contrato. Não mude nomes nem assinaturas públicas: o `marco3.py` e os testes dependem deles.
Funções auxiliares privadas (`_nome`) são permitidas.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from elevatoria.calibracao import CurvaCalibracao
from elevatoria.raizes import MetodoRaiz, ResultadoRaiz
from fornecido.hidraulica import Tubulacao


@dataclass(frozen=True)
class PontoOperacao:
    """Resultado do cálculo do ponto em que a bomba e o sistema se equilibram.

    Attributes:
        vazao: Vazão de operação, em L/s.
        altura: Altura fornecida pela bomba nessa vazão, em metros.
        resultado: Resultado completo retornado pelo método de raiz.
    """

    vazao: float              # L/s
    altura: float             # m
    resultado: ResultadoRaiz  # o que o resolvedor devolveu (iterações, histórico...)


def ponto_operacao(bomba: CurvaCalibracao, tubulacao: Tubulacao, resolvedor: MetodoRaiz,
                   a: float = 10.0, b: float = 100.0) -> PontoOperacao:
    """Encontra a vazão em que a altura da bomba iguala a altura exigida pelo sistema.

    Args:
        bomba: Curva calibrada que fornece a altura da bomba em função da vazão.
        tubulacao: Modelo hidráulico que calcula a altura exigida pelo sistema.
        resolvedor: Método de raiz usado para resolver a diferença entre as alturas.
        a: Limite inferior do intervalo de busca, em L/s.
        b: Limite superior do intervalo de busca, em L/s.

    Returns:
        `PontoOperacao` com a vazão encontrada, a altura da bomba nessa vazão e o resultado
        completo do resolvedor.

    Raises:
        ValueError: Se `a >= b`, se o intervalo estiver fora do domínio da bomba ou se o
            resolvedor retornar sem convergir. Erros do próprio resolvedor também são
            propagados.
    """
    if a >= b:
        raise ValueError(f"a ({a}) deve ser menor que b ({b})")
    if not (bomba.dominio[0] <= a and b <= bomba.dominio[1]):
        raise ValueError(f"[a,b] = [{a}, {b}] não está dentro do domínio da bomba {bomba.dominio}")

    f_Q = lambda Q: bomba(Q) - tubulacao.altura_sistema(Q)
    resultado = resolvedor.encontrar(f_Q, a, b)
    if not resultado.convergiu:
        raise ValueError(f"o resolvedor não convergiu: {resultado}")
    Q = resultado.raiz
    return PontoOperacao(vazao=Q, altura=bomba(Q), resultado=resultado)



def ordem_convergencia(historico: Sequence[float], raiz: float, piso: float = 1e-14) -> float:
    """Estima a ordem de convergência usando as últimas aproximações acima do piso.

    Args:
        historico: Aproximações sucessivas do método, em ordem cronológica.
        raiz: Valor de referência usado para calcular os erros absolutos.
        piso: Limite relativo para ignorar erros dominados por arredondamento.

    Returns:
        Estimativa de `p` a partir dos três últimos erros considerados e da relação

        `p ≈ log(e_{k+1} / e_k) / log(e_k / e_{k-1})`.

        Erros menores que `piso * max(1, abs(raiz))` são ignorados por estarem no nível de
        arredondamento.

    Raises:
        ValueError: Se houver menos de três erros acima do piso.
    """
    e = [abs(x - raiz) for x in historico]
    piso *= max(1.0, abs(raiz))
    e = [e for e in e if e > piso]
    if len(e) < 3:
        raise ValueError(f"menos de 3 erros acima do piso {piso:.1e}: {e}")
    return math.log(e[-1] / e[-2]) / math.log(e[-2] / e[-3])

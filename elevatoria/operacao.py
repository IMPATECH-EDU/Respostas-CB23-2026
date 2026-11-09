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
    """O ponto em que a bomba opera: vazão, altura e o resultado do método de raiz."""

    vazao: float              # L/s
    altura: float             # m
    resultado: ResultadoRaiz  # o que o resolvedor devolveu (iterações, histórico...)


def ponto_operacao(bomba: CurvaCalibracao, tubulacao: Tubulacao, resolvedor: MetodoRaiz,
                   a: float = 10.0, b: float = 100.0) -> PontoOperacao:
    """Ponto de operação: a vazão `Q` em `[a, b]` (L/s) em que a bomba e o sistema se igualam.
    Aplica o resolvedor númerico em [a,b], para encontrar as raizes da função f(Q) = bomba(Q) - tubulacao.altura_sistema(Q).
    Levanta valueError com a>=b, intervalo [a, b] não contido no dominio da bomba, e qunado o resolvedor não converge.
    """

    if a >= b:
        raise ValueError("O intervalo deve ser [a, b], logo a deve ser menor que a b.")

    dominio_bomba = bomba.dominio

    if dominio_bomba[0] > a or dominio_bomba[1] < b:
        raise ValueError("O intervalo [a, b], deve estar contido no domínio da bomba.")

    f = lambda Q: bomba(Q) - tubulacao.altura_sistema(Q)

    resultado = resolvedor.encontrar(f, a, b)
    if not resultado.convergiu:
        raise ValueError("O resolvedor não convergiu para o ponto de operação.")

    Q = resultado.raiz

    return PontoOperacao(Q, bomba(Q), resultado)


def ordem_convergencia(historico: Sequence[float], raiz: float, piso: float = 1e-14) -> float:
    """Estimativa da ordem de convergência `p` de uma sequência de aproximações.
    Utiliza os últimos 3 valores do historico, onde seus erros (|x - raiz|) seja maior que piso · max(1, |raiz|), do historico.
    Usando a ordem deles no historico calculamos a convergencia p, levantando Value error quando o numero de erros acima do piso é menor que 3.
    """
    
    historico_invertido = tuple(reversed(historico))
    erros_acima = []

    for x in historico_invertido:
      erro = abs(x - raiz)
      if erro > piso * max(1, abs(raiz)):
        erros_acima.append(erro)
        if len(erros_acima) == 3:
          break

    if len(erros_acima) < 3:
       raise ValueError("Número insuficientes de erros acima do piso.")

    return math.log(erros_acima[0] / erros_acima[1]) / math.log(erros_acima[1] / erros_acima[2])
        

    
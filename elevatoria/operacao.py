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

    A bomba opera onde a altura que ela fornece, `bomba(Q)`, é igual à altura que o sistema
    exige, `tubulacao.altura_sistema(Q)`. Esta função:

    1. define `f(Q) = bomba(Q) - tubulacao.altura_sistema(Q)`;
    2. resolve `f(Q) = 0` com `resolvedor.encontrar(f, a, b)`;
    3. devolve `PontoOperacao(vazao=Q, altura=bomba(Q), resultado=...)`, com `Q` a raiz
       encontrada e `resultado` o `ResultadoRaiz` devolvido pelo resolvedor.

    Levanta `ValueError` se `a >= b`, se `[a, b]` não estiver dentro do domínio da bomba
    (`bomba.dominio`) ou se o resolvedor não convergir (`resultado.convergiu` falso). Um
    `ValueError` do próprio resolvedor (por exemplo, sem troca de sinal na bissecção) não é
    tratado: ele chega a quem chamou `ponto_operacao`.
    """

    # Verificações de erro:
    if a >= b:
        raise ValueError(f"{a} >= {b} não é uma entrada válida.")

    # bomba (CurvaCalibracao) já possui uma função que possibilita verificar o domínio e levantar erro, mas não vamos usá-la porque tem o underscore '_'
    dominio = bomba.dominio
    if a < dominio[0] or b > dominio[1]:
        raise ValueError(f"[{a}, {b}] não está contido no domínio da bomba [{dominio}]")

    # Definimos a função f com base no contrato
    f = lambda Q : bomba(Q) - tubulacao.altura_sistema(Q)

    # Usamos o resolvedor, que retorna um MetodoRaiz
    resultado = resolvedor.encontrar(f, a, b)

    if not resultado.convergiu:
        raise ValueError(f"O resolvedor não convergiu.")

    Q = resultado.raiz

    return PontoOperacao(
        vazao = Q,
        altura = bomba(Q),
        resultado = resultado
    )


def ordem_convergencia(historico: Sequence[float], raiz: float, piso: float = 1e-14) -> float:
    """Estimativa da ordem de convergência `p` de uma sequência de aproximações.

    Com os erros `e_k = |x_k - raiz|`, se `e_{k+1} ≈ C·e_k^p`, então

        p ≈ log(e_{k+1} / e_k) / log(e_k / e_{k-1}).

    Use os **três últimos** erros, na ordem do `historico`, que forem maiores que
    `piso · max(1, |raiz|)`: erros menores estão no nível do arredondamento e não dizem nada
    sobre o método. Exemplos: erros 1e-1, 1e-2, 1e-4, 1e-8 dão `p = 2` (convergência
    quadrática); erros 0.5, 0.25, 0.125 dão `p = 1` (convergência linear).

    Levanta `ValueError` se houver menos de 3 erros acima do piso.
    """

    # Vamos usar o map e filter para pegar os erros que estão acima do piso
    erros_validos = list(filter(lambda e : e > piso, map(lambda e : abs(e - raiz), historico)))

    # Verificamos o tamanho
    if len(erros_validos) < 3:
        raise ValueError(f"Apenas {len(erros_validos)} erros estão acima do piso.")

    e = erros_validos[-3:]

    # Aplicando a fórmula para p:
    p = math.log( e[2] / e[1] ) / math.log( e[1] / e[0])

    return p

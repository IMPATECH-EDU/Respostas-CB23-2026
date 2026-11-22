"""Ponto de operação da bomba e diagnóstico dos métodos de raiz (issue #8).

Este módulo junta peças que já existem na base:

- `CurvaCalibracao` (de `elevatoria/calibracao.py`, Marco 2): a curva da bomba, interpolada
  a partir do ensaio;
- `Tubulacao` (de `fornecido/hidraulica.py`, da equipe de hidráulica): a curva do sistema;
- `Bisseccao` e `Newton` (de `elevatoria/raizes.py`, escritos por um colega): os métodos de
  raiz, que devolvem um `ResultadoRaiz`.

A vazão encontrada e o histórico do resolvedor permitem conferir a convergência.
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
    tratado: ele chega a quem chamou `ponto_operacao`. Uma raiz fora de [a, b] também é rejeitada
    com `ValueError`.
    """
    if a >= b:
        raise ValueError("o intervalo de vazões deve ter a < b")
    minimo, maximo = bomba.dominio
    if a < minimo or b > maximo:
        raise ValueError(f"[{a}, {b}] fora do domínio da bomba [{minimo}, {maximo}]")

    def diferenca_de_altura(q: float) -> float:
        """Devolve a altura fornecida menos a exigida quando a vazão é q."""
        return bomba(q) - tubulacao.altura_sistema(q)

    resultado = resolvedor.encontrar(diferenca_de_altura, a, b)
    if not resultado.convergiu:
        raise ValueError(f"o método não convergiu após {resultado.iteracoes} iterações")
    q = resultado.raiz
    if not a <= q <= b:
        raise ValueError(f"a vazão encontrada ({q}) está fora de [{a}, {b}]")
    return PontoOperacao(q, bomba(q), resultado)


def ordem_convergencia(historico: Sequence[float], raiz: float, piso: float = 1e-14) -> float:
    """Estimativa da ordem de convergência `p` de uma sequência de aproximações.

    Com os erros `e_k = |x_k - raiz|`, se `e_{k+1} ≈ C·e_k^p`, então

        p ≈ log(e_{k+1} / e_k) / log(e_k / e_{k-1}).

    Use os **três últimos** erros, na ordem do `historico`, que forem maiores que
    `piso · max(1, |raiz|)`: erros menores estão no nível do arredondamento e não dizem nada
    sobre o método. Exemplos: erros 1e-1, 1e-2, 1e-4, 1e-8 dão `p = 2` (convergência
    quadrática); erros 0.5, 0.25, 0.125 dão `p = 1` (convergência linear).

    Levanta `ValueError` para piso negativo, menos de 3 erros acima dele ou denominador nulo.
    """
    if piso < 0:
        raise ValueError("o piso do erro deve ser não negativo")
    limite = piso * max(1.0, abs(raiz))
    erros = (abs(x - raiz) for x in historico)
    utilizaveis = [erro for erro in erros if erro > limite]
    if len(utilizaveis) < 3:
        raise ValueError("a estimativa exige três erros acima do piso")
    anterior, atual, proximo = map(math.log, utilizaveis[-3:])
    if atual == anterior:
        raise ValueError("erros consecutivos iguais não definem a ordem")
    return (proximo - atual) / (atual - anterior)

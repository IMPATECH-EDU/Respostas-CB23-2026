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
    tratado: ele chega a quem chamou `ponto_operacao`. Também levanta `ValueError` se a raiz
    cair fora de `[a, b]`: o Newton não fica preso ao intervalo e, num `[a, b]` sem raiz, pode
    convergir para uma raiz de fora, onde a bissecção recusaria o mesmo intervalo.
    """
    if a >= b:
        raise ValueError(f"o intervalo deve ter a < b; recebi [{a}, {b}]")
    inicio, fim = bomba.dominio
    if a < inicio or b > fim:
        raise ValueError(f"[{a}, {b}] sai do domínio da bomba, [{inicio}, {fim}]")
    resultado = resolvedor.encontrar(lambda q: bomba(q) - tubulacao.altura_sistema(q), a, b)
    if not resultado.convergiu:
        raise ValueError(f"{type(resolvedor).__name__} não convergiu em "
                         f"{resultado.iteracoes} iterações")
    q = resultado.raiz
    if not a <= q <= b:
        raise ValueError(f"a raiz {q:.3f} L/s caiu fora de [{a}, {b}]")
    return PontoOperacao(vazao=q, altura=bomba(q), resultado=resultado)


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
    corte = piso * max(1.0, abs(raiz))
    erros = [e for e in (abs(x - raiz) for x in historico) if e > corte]
    if len(erros) < 3:
        raise ValueError(f"preciso de 3 erros acima de {corte:.1e}; o histórico tem {len(erros)}")
    e0, e1, e2 = erros[-3:]
    try:
        return math.log(e2 / e1) / math.log(e1 / e0)
    except ZeroDivisionError:
        raise ValueError("os erros pararam de mudar; a ordem não está definida") from None

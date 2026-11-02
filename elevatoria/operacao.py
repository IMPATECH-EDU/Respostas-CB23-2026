"""Ponto de operação da bomba e diagnóstico dos métodos de raiz (issue #8).

Este módulo junta peças que já existem na base:

- `CurvaCalibracao` (de `elevatoria/calibracao.py`, Marco 2): a curva da bomba, interpolada
  a partir do ensaio;
- `Tubulacao` (de `fornecido/hidraulica.py`, da equipe de hidráulica): a curva do sistema;
- `Bisseccao` e `Newton` (de `elevatoria/raizes.py`, escritos por um colega): os métodos de
  raiz, que devolvem um `ResultadoRaiz`.
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
    """Ponto de operação: a vazão `Q` em `[a, b]` (L/s) em que a bomba e o sistema se igualam."""
    if a >= b:
        raise ValueError(f"a ({a}) deve ser estritamente menor que b ({b})")

    q_min, q_max = bomba.dominio
    if a < q_min or b > q_max:
        raise ValueError(f"intervalo [{a}, {b}] fora do domínio da bomba [{q_min}, {q_max}]")

    def f(q: float) -> float:
        return bomba(q) - tubulacao.altura_sistema(q)

    resultado = resolvedor.encontrar(f, a, b)
    if not resultado.convergiu:
        raise ValueError("o resolvedor de raiz não convergiu")

    vazao_opt = resultado.raiz
    altura_opt = bomba(vazao_opt)

    return PontoOperacao(vazao=vazao_opt, altura=altura_opt, resultado=resultado)


def ordem_convergencia(historico: Sequence[float], raiz: float, piso: float = 1e-14) -> float:
    """Estimativa da ordem de convergência `p` de uma sequência de aproximações."""
    limite = piso * max(1.0, abs(raiz))
    erros_validos = [abs(x - raiz) for x in historico if abs(x - raiz) > limite]

    if len(erros_validos) < 3:
        raise ValueError("há menos de 3 erros acima do piso de tolerância")

    e1, e2, e3 = erros_validos[-3], erros_validos[-2], erros_validos[-1]
    return math.log(e3 / e2) / math.log(e2 / e1)
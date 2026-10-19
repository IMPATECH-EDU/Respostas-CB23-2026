"""Modelo hidráulico da adutora (código fornecido pela equipe de hidráulica; NÃO ALTERE).

O modelo precisa resolver a equação de Colebrook, que é implícita no fator de atrito. A
equipe de hidráulica não escreveu um método de raiz: cada `Tubulacao` recebe um
**resolvedor**, que é qualquer objeto que siga o protocolo `Resolvedor` abaixo. Assim, o
método numérico pode ser trocado sem mexer no modelo (composição).

Unidades: vazão `Q` em L/s; as demais grandezas no SI (m, m/s, m²/s).
"""
from __future__ import annotations

import math
from typing import Any, Callable, Protocol

#: Viscosidade cinemática da água a 20 °C (m²/s).
VISCOSIDADE = 1.004e-6

#: Aceleração da gravidade (m/s²).
GRAVIDADE = 9.81


class Resolvedor(Protocol):
    """Protocolo de um método de raiz.

    Qualquer objeto com um método `encontrar(f, a, b)` serve, desde que o resultado tenha o
    atributo `raiz`: um `x` em `[a, b]` com `f(x) ≈ 0`. Não é preciso herdar desta classe.
    """

    def encontrar(self, f: Callable[[float], float], a: float, b: float) -> Any:
        """Uma raiz de `f` no intervalo `[a, b]`, no atributo `raiz` do resultado."""


def fator_atrito_colebrook(reynolds: float, rugosidade_relativa: float,
                           resolvedor: Resolvedor) -> tuple[float, Any]:
    """Fator de atrito de Darcy pela equação de Colebrook.

    A equação de Colebrook,

        1/√f = −2·log10( ε/(3,7·D) + 2,51/(Re·√f) ),

    é implícita em `f`. Com `x = 1/√f` (e `rugosidade_relativa = ε/D`), ela vira

        g(x) = x + 2·log10( (ε/D)/3,7 + 2,51·x/Re ) = 0,

    uma função crescente de `x`, com uma única raiz no intervalo `[2, 15]`. Esta função
    resolve `g(x) = 0` com o `resolvedor` e devolve `(f, resultado)`, com `f = 1/x²` e
    `resultado` o que o resolvedor devolveu.

    Levanta `ValueError` se `reynolds <= 0` ou `rugosidade_relativa < 0`.
    """
    if reynolds <= 0:
        raise ValueError(f"o número de Reynolds deve ser positivo; recebi {reynolds}")
    if rugosidade_relativa < 0:
        raise ValueError(f"a rugosidade relativa não pode ser negativa; recebi {rugosidade_relativa}")

    def g(x: float) -> float:
        return x + 2.0 * math.log10(rugosidade_relativa / 3.7 + 2.51 * x / reynolds)

    resultado = resolvedor.encontrar(g, 2.0, 15.0)
    return 1.0 / resultado.raiz ** 2, resultado


class Tubulacao:
    """Adutora: diâmetro, comprimento, rugosidade e desnível, mais um resolvedor para Colebrook.

    `Tubulacao(diametro, comprimento, rugosidade, desnivel, resolvedor)`, com os quatro
    primeiros em metros. Levanta `ValueError` se o diâmetro ou o comprimento não forem
    positivos, ou se a rugosidade ou o desnível forem negativos.

    A **curva do sistema** é a altura que a bomba precisa fornecer para bombear a vazão `Q`:
    o desnível mais a perda de carga na adutora (Darcy–Weisbach),

        H_sis(Q) = desnível + f · (L/D) · v²/(2g).
    """

    def __init__(self, diametro: float, comprimento: float, rugosidade: float,
                 desnivel: float, resolvedor: Resolvedor) -> None:
        if diametro <= 0 or comprimento <= 0:
            raise ValueError("o diâmetro e o comprimento devem ser positivos")
        if rugosidade < 0 or desnivel < 0:
            raise ValueError("a rugosidade e o desnível não podem ser negativos")
        self._diametro = float(diametro)
        self._comprimento = float(comprimento)
        self._rugosidade = float(rugosidade)
        self._desnivel = float(desnivel)
        self._resolvedor = resolvedor

    @property
    def desnivel(self) -> float:
        """Desnível geométrico entre os reservatórios (m)."""
        return self._desnivel

    def velocidade(self, Q: float) -> float:
        """Velocidade média da água (m/s) para a vazão `Q` (L/s)."""
        return 4.0 * (Q / 1000.0) / (math.pi * self._diametro ** 2)

    def reynolds(self, Q: float) -> float:
        """Número de Reynolds para a vazão `Q` (L/s)."""
        return self.velocidade(Q) * self._diametro / VISCOSIDADE

    def fator_atrito(self, Q: float) -> float:
        """Fator de atrito de Colebrook para a vazão `Q` (L/s); `ValueError` se `Q <= 0`."""
        if Q <= 0:
            raise ValueError(f"a vazão deve ser positiva para calcular o atrito; recebi {Q}")
        f, _ = fator_atrito_colebrook(self.reynolds(Q), self._rugosidade / self._diametro,
                                      self._resolvedor)
        return f

    def perda_de_carga(self, Q: float) -> float:
        """Perda de carga na adutora (m); `0.0` se `Q == 0` e `ValueError` se `Q < 0`."""
        if Q < 0:
            raise ValueError(f"a vazão não pode ser negativa; recebi {Q}")
        if Q == 0:
            return 0.0
        v = self.velocidade(Q)
        return self.fator_atrito(Q) * (self._comprimento / self._diametro) * v ** 2 / (2.0 * GRAVIDADE)

    def altura_sistema(self, Q: float) -> float:
        """Altura exigida pelo sistema (m) para a vazão `Q` (L/s): desnível + perda de carga."""
        return self._desnivel + self.perda_de_carga(Q)

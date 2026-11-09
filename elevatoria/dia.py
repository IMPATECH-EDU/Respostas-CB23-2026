"""Curvas da bomba por mínimos quadrados e o balanço do dia de operação (issue #10).

Este módulo junta peças que já existem na base:

- o registro de vazão do dia, a potência e as faixas tarifárias (de `fornecido/energia.py`,
  da equipe de energia);
- as regras de integração `Trapezio` e `Simpson` (de `elevatoria/integracao.py`, escritas por
  um colega);
- o NumPy ou o SciPy, para o ajuste de curvas (há mais de um caminho: veja `ajustar_polinomio`).

As funções marcadas com `NotImplementedError` são a issue #10; as docstrings descrevem o
contrato. Não mude nomes nem assinaturas públicas: o `marco4.py` e os testes dependem deles.
Funções auxiliares privadas (`_nome`) são permitidas.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from elevatoria.integracao import Integrador
from fornecido.energia import FAIXAS_TARIFARIAS, potencia_eletrica


def ajustar_polinomio(x: np.ndarray, y: np.ndarray, grau: int) -> np.ndarray:
    """
    Calcula os coeficientes atraves de np.polynomial.polynomial.polyfit(x,y,grau);
    Levanta index error caso x e y tenham dimensões diferentes de 1D ou tenham tamanhos diferentes entre si,
    se grau > 0, se o número de elementos de x for menor que grau mais 1, ou seja se houver menos 
    """
    x, y = np.asarray(x), np.asarray(y) # vi que nos codigos de aceitação são passadas listas no lugar de arrays do numpy, coloquei essa linha para assegurar que os métodos no np possam ser usados

    if grau < 0 or len(x) < grau + 1 or x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("x e y devem ser vetores 1d do mesmo tamanho, com grau > 0 e ter mais ou o mesmo número de pontos que coenficientes.")

    coeficientes = np.polynomial.polynomial.polyfit(x, y, grau)
    return coeficientes


@dataclass(frozen=True)
class ResumoDia:
    """Balanço do dia de operação."""

    volume_m3: float                    # volume bombeado (m³)
    energia_kwh: float                  # energia consumida (kWh)
    custo_reais: float                  # custo da energia (R$): a soma de custo_por_faixa
    custo_por_faixa: tuple[float, ...]  # custo de cada faixa, na ordem de FAIXAS_TARIFARIAS


def dia_de_operacao(t: np.ndarray, vazao: np.ndarray, coef_altura: np.ndarray,
                    coef_rendimento: np.ndarray, integrador: Integrador) -> ResumoDia:
    """
    Calcula altura e rendimento a partir dos coeficientes dados e os utiliza para calcular a potencia;
    Calcula volume e energia a partir de integrador.integrar_tabela, usando (vazao,t) e (potencia,t), respectivamente;
    A partir de FAIXAS_TARIFARIAS calcula o custo total do dia e separa o custo de cada faixa;
    Retorna um objeto da Classe Resumo do Dia;
    Levanta Index Error caso t e vazao tenham tamanhos diferentes, e caso algum dos limites da faixa (0, 18, 21, 24) não sejam instantes de t.
    """
    t, vazao, coef_altura, coef_rendimento = np.asarray(t), np.asarray(vazao), np.asarray(coef_altura), np.asarray(coef_rendimento)

    limites_faixa = np.array([0,18,21,24])

    if t.size != vazao.size or np.any(~np.isin(limites_faixa,t)):
        raise ValueError('O número de registros de tempo e vazão devem ser os mesmos, e todos os limites de faixa devem estar em t')

    altura = np.polynomial.polynomial.polyval(vazao, coef_altura)
    rendimento = np.polynomial.polynomial.polyval(vazao, coef_rendimento)
    potencia = potencia_eletrica(vazao,altura,rendimento)
    volume = 3.6 * integrador.integrar_tabela(t, vazao)
    energia = integrador.integrar_tabela(t, potencia)

    custo_total = 0
    custo_por_faixa = []

    for faixa in FAIXAS_TARIFARIAS:
        inicio, fim, tarifa = faixa

        mascara = (t >= inicio) & (t <= fim)
        t_novo = t[mascara]
        potencia_nova = potencia[mascara]
        custo_faixa = tarifa * integrador.integrar_tabela(t_novo,potencia_nova)
        custo_por_faixa.append(custo_faixa)
        custo_total += custo_faixa

    return ResumoDia(volume, energia, custo_total, tuple(custo_por_faixa))

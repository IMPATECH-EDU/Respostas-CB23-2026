"""Dia de operação: registro de vazão, potência e tarifa (equipe de energia; NÃO ALTERE).

Unidades: tempo `t` em horas (0 a 24); vazão em L/s; altura em m; potência em kW; energia em
kWh; tarifa em R$/kWh.
"""
from __future__ import annotations

import numpy as np

from fornecido.simulador import gerar_demanda

#: Massa específica da água (kg/m³).
MASSA_ESPECIFICA = 998.0

#: Aceleração da gravidade (m/s²).
GRAVIDADE = 9.81

#: Faixas tarifárias do dia: (início em h, fim em h, tarifa em R$/kWh). A ponta é 18 h–21 h.
FAIXAS_TARIFARIAS = ((0.0, 18.0, 0.50), (18.0, 21.0, 1.50), (21.0, 24.0, 0.50))


def potencia_eletrica(vazao: np.ndarray, altura: np.ndarray, rendimento: np.ndarray) -> np.ndarray:
    """Potência elétrica da bomba (kW): `ρ · g · (Q/1000) · H / (1000 · η)`.

    Recebe arrays (ou números) com a vazão `Q` (L/s), a altura `H` (m) e o rendimento `η`
    (entre 0 e 1) e devolve um `ndarray`. Levanta `ValueError` se algum rendimento não for
    positivo.
    """
    q = np.asarray(vazao, dtype=float)
    h = np.asarray(altura, dtype=float)
    eta = np.asarray(rendimento, dtype=float)
    if np.any(eta <= 0):
        raise ValueError("o rendimento deve ser positivo em todos os instantes")
    return MASSA_ESPECIFICA * GRAVIDADE * (q / 1000.0) * h / (1000.0 * eta)


def vazao_registrada(matricula: int) -> tuple[np.ndarray, np.ndarray]:
    """Registro de vazão do dia, `(t, q)`: leituras a cada 15 min, de 0 h a 24 h.

    O SCADA perdeu 8 das 97 leituras do dia (falhas de comunicação), então o espaçamento entre
    instantes consecutivos **não é constante**: às vezes é 15 min, às vezes 30 min. As leituras
    em 0 h, 18 h, 21 h e 24 h (os limites das faixas tarifárias) estão sempre presentes.
    """
    t, q = gerar_demanda(matricula)
    rng = np.random.default_rng([matricula, 4])
    limites = {inicio for inicio, _, _ in FAIXAS_TARIFARIAS} | {FAIXAS_TARIFARIAS[-1][1]}
    candidatos = [i for i in range(t.size) if t[i] not in limites]
    perdidas = rng.choice(candidatos, 8, replace=False)
    manter = np.setdiff1d(np.arange(t.size), perdidas)
    return t[manter], q[manter]

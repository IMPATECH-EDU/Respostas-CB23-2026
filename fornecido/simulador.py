"""Simulador do Projeto Elevatória (Programação 2, IMPATECH, 2026).

Gera os dados da estação elevatória e os valores de conferência ("verdade") usados nos
`assert` dos marcos. NÃO ALTERE este arquivo: copie-o para a pasta do seu projeto.

Os valores "verdadeiros" da planta existem apenas para CONFERIR os seus resultados. Usá-los
para calcular o que o enunciado pede que você estime a partir dos dados invalida o exercício.

Requer apenas NumPy. Python 3.9 ou superior.
"""
import numpy as np
from datetime import datetime, timedelta

# ----------------------------------------------------------------------------------------
# Planta (valores verdadeiros)
# ----------------------------------------------------------------------------------------
RHO = 998.0        # massa específica da água (kg/m3)
G = 9.81           # aceleração da gravidade (m/s2)
NU = 1.004e-6      # viscosidade cinemática da água (m2/s)
DIAMETRO = 0.20    # diâmetro da adutora (m)
COMPRIMENTO = 850.0  # comprimento da adutora (m)
RUGOSIDADE = 0.15e-3  # rugosidade absoluta do tubo (m)
DESNIVEL = 18.0    # desnível geométrico entre os reservatórios (m)
PRESSAO_SUCCAO = 30.0     # pressão de sucção em operação (kPa)
PRESSAO_RECALQUE = 380.0  # pressão de recalque em operação (kPa)
TARIFA_FORA_PONTA = 0.50  # R$/kWh
TARIFA_PONTA = 1.50       # R$/kWh, das 18 h às 21 h


# ----------------------------------------------------------------------------------------
# Transmissores de pressão (0 a 600 kPa) e conversor A/D de 12 bits (0 a 4095 contagens)
# ----------------------------------------------------------------------------------------
def p_real(c):
    """Resposta verdadeira do transmissor (kPa) para contagens c do A/D (0 a 4095)."""
    return 600.0 * np.sin(0.5 * np.pi * np.asarray(c, dtype=float) / 4095.0)


def c_real(p):
    """Contagens do A/D (12 bits) que correspondem à pressão p (kPa)."""
    return 4095.0 * (2.0 / np.pi) * np.arcsin(np.asarray(p, dtype=float) / 600.0)


def tabela_calibracao():
    """Tabela de calibração disponível ao engenheiro: (c_cal, p_cal), com 9 pontos."""
    c_cal = np.linspace(0.0, 4095.0, 9)
    return c_cal, p_real(c_cal)


# ----------------------------------------------------------------------------------------
# Marco 1: log do SCADA
# ----------------------------------------------------------------------------------------
def gerar_log(matricula):
    """Log SCADA de 1 hora (05/10/2026, 08:00 a 09:00, uma leitura a cada 6 s).

    Retorna (texto, verdade): o log em texto e os valores de conferência.
    """
    rng = np.random.default_rng(matricula)
    n = 600
    t0 = datetime(2026, 10, 5, 8, 0, 0)
    c101 = np.round(c_real(PRESSAO_SUCCAO) + rng.normal(0, 3.0, n)).astype(int)     # PT101
    c102 = np.round(c_real(PRESSAO_RECALQUE) + rng.normal(0, 3.0, n)).astype(int)   # PT102
    idx = np.sort(rng.choice(n, 5, replace=False))
    c102[idx] += 400                                                                # 5 leituras espúrias
    pulsos = rng.poisson(3892, n)                                                   # FT201: pulsos de 0,1 L em 6 s
    nivel = 47.0 + np.cumsum(rng.normal(0.01, 0.02, n))                             # LT301: nível (%)

    def ts(i):
        return (t0 + timedelta(seconds=6 * i)).strftime("%Y-%m-%d %H:%M:%S")

    linhas = [f"{ts(0)} INFO B1 evento=partida corrente=47.5"]
    for i in range(n):
        linhas += [f"{ts(i)} INFO PT101 contagens={c101[i]}",
                   f"{ts(i)} INFO PT102 contagens={c102[i]}",
                   f"{ts(i)} INFO FT201 pulsos={pulsos[i]}",
                   f"{ts(i)} INFO LT301 nivel={nivel[i]:.2f}"]
        if i in idx[:2]:
            linhas.append(f"{ts(i)} ALARME PT102 evento=pressao_alta limite=2000")
        if i == 450:
            linhas.append(f"{ts(i)} WARN B1 evento=vibracao corrente=49.8")
    for pos, lixo in zip([2050, 1203, 410, 57],
                         ["### falha de comunicacao com a RTU ###", "2026-10-05 08:20:4",
                          "### falha de comunicacao com a RTU ###", "2026-10-05 08:03"]):
        linhas.insert(pos, lixo)                                                    # 4 linhas corrompidas
    verdade = {"linhas": len(linhas), "invalidas": 4,
               "por_nivel": {"INFO": 2401, "WARN": 1, "ALARME": 2},
               "registros_por_tag": {"B1": 2, "PT101": 600, "PT102": 602, "FT201": 600, "LT301": 600},
               "espurios": idx.tolist(), "pulsos_total": int(pulsos.sum()),
               "pressao_succao": PRESSAO_SUCCAO, "pressao_recalque": PRESSAO_RECALQUE,
               "altura_manometrica": (PRESSAO_RECALQUE - PRESSAO_SUCCAO) * 1000.0 / (RHO * G),
               "vazao_media": 3892 / 6.0 * 0.1}
    return "\n".join(linhas) + "\n", verdade


# ----------------------------------------------------------------------------------------
# Marco 3 e 4: hidráulica (valores verdadeiros; implementação independente, só NumPy)
# ----------------------------------------------------------------------------------------
def fator_atrito_real(Q, rugosidade=RUGOSIDADE):
    """Fator de atrito de Darcy (Colebrook) para a vazão Q (L/s); aceita escalar ou array."""
    Q = np.asarray(Q, dtype=float)
    v = 4.0 * (Q / 1000.0) / (np.pi * DIAMETRO ** 2)
    Re = np.maximum(v * DIAMETRO / NU, 1.0)
    x = np.full_like(Re, 8.0)                       # x = 1 / sqrt(f)
    for _ in range(60):
        x = -2.0 * np.log10(rugosidade / (3.7 * DIAMETRO) + 2.51 * x / Re)
    return 1.0 / x ** 2


def perda_de_carga_real(Q, rugosidade=RUGOSIDADE):
    """Perda de carga distribuída (m) na adutora para a vazão Q (L/s)."""
    Q = np.asarray(Q, dtype=float)
    v = 4.0 * (Q / 1000.0) / (np.pi * DIAMETRO ** 2)
    return fator_atrito_real(Q, rugosidade) * (COMPRIMENTO / DIAMETRO) * v ** 2 / (2.0 * G)


def altura_sistema_real(Q):
    """Altura manométrica exigida pelo sistema (m) para a vazão Q (L/s)."""
    return DESNIVEL + perda_de_carga_real(Q)


def altura_bomba_real(Q):
    """Curva verdadeira da bomba: altura manométrica (m) para a vazão Q (L/s)."""
    Q = np.asarray(Q, dtype=float)
    return 45.0 - 0.0022 * Q ** 2


def rendimento_real(Q):
    """Curva verdadeira de rendimento da bomba (adimensional) para a vazão Q (L/s)."""
    x = np.asarray(Q, dtype=float) / 70.0
    return 0.75 * (2.0 * x - x ** 2)


def potencia_real(Q):
    """Potência elétrica verdadeira (kW) absorvida pela bomba na vazão Q (L/s)."""
    Q = np.asarray(Q, dtype=float)
    return RHO * G * (Q / 1000.0) * altura_bomba_real(Q) / rendimento_real(Q) / 1000.0


def gerar_ensaio_bomba(matricula):
    """Ensaio da bomba: 11 pontos, Q de 0 a 100 L/s. Retorna dict com 'vazao', 'altura', 'rendimento'."""
    rng = np.random.default_rng([matricula, 1])
    q = np.arange(0.0, 101.0, 10.0)
    h = altura_bomba_real(q) + rng.normal(0.0, 0.15, q.size)
    eta = rendimento_real(q) + rng.normal(0.0, 0.005, q.size)
    eta[0] = 0.0
    return {"vazao": q, "altura": h, "rendimento": eta}


def gerar_ensaio_perda(matricula):
    """Ensaio de perda de carga na adutora: 9 pontos (Q de 20 a 100 L/s). Retorna dict 'vazao', 'perda'."""
    rng = np.random.default_rng([matricula, 2])
    q = np.arange(20.0, 101.0, 10.0)
    hf = perda_de_carga_real(q) * np.exp(rng.normal(0.0, 0.03, q.size))
    return {"vazao": q, "perda": hf}


def gerar_demanda(matricula):
    """Vazão medida (L/s) a cada 15 min em 24 h (97 pontos). Retorna (t_horas, vazao)."""
    rng = np.random.default_rng([matricula, 3])
    t = np.arange(0.0, 24.0 + 1e-9, 0.25)
    q = demanda_real(t) * (1.0 + rng.normal(0.0, 0.02, t.size))
    return t, q


def demanda_real(t):
    """Vazão de demanda verdadeira (L/s) no instante t (horas): máxima às 18 h."""
    return 45.0 + 15.0 * np.sin(2.0 * np.pi * (np.asarray(t, dtype=float) - 12.0) / 24.0)


def tarifa(t):
    """Tarifa de energia (R$/kWh) no instante t (horas): ponta das 18 h (inclusive) às 21 h (exclusive)."""
    t = np.asarray(t, dtype=float)
    return np.where((t >= 18.0) & (t < 21.0), TARIFA_PONTA, TARIFA_FORA_PONTA)


def ponto_operacao_real():
    """Ponto de operação verdadeiro (Q em L/s, H em m): bomba x sistema (bissecção)."""
    a, b = 1.0, 120.0
    f = lambda q: float(altura_bomba_real(q) - altura_sistema_real(q))
    for _ in range(200):
        m = 0.5 * (a + b)
        if f(a) * f(m) <= 0.0:
            b = m
        else:
            a = m
    q = 0.5 * (a + b)
    return q, float(altura_bomba_real(q))


def verdade_dia():
    """Valores verdadeiros do dia de operação: volume (m3), energia (kWh) e custo (R$)."""
    t = np.linspace(0.0, 24.0, 240001)
    q = demanda_real(t)
    p = potencia_real(q)
    trap = lambda y: float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(t)))
    return {"volume_m3": trap(q) * 3.6, "energia_kwh": trap(p), "custo_reais": trap(p * tarifa(t))}


if __name__ == "__main__":
    # Verificação rápida: python simulador.py
    texto, verdade = gerar_log(123456)
    q, h = ponto_operacao_real()
    print(texto[:500] + "...\n")
    print(f"log: {verdade['linhas']} linhas ({verdade['invalidas']} corrompidas)")
    print(f"ponto de operação verdadeiro: Q = {q:.2f} L/s, H = {h:.2f} m")
    print("simulador.py OK")

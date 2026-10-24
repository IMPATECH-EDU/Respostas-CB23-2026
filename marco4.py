"""Marco 4 — Ajuste e integração: script de demonstração (PRONTO; NÃO ALTERE).

Execute a partir da raiz do repositório, com o ambiente ativado:  python marco4.py

O script usa a MATRICULA do seu marco1.py e roda em etapas. Ele para no primeiro assert que
falhar ou no primeiro NotImplementedError:

- Etapa 1 só usa código que já existe: roda desde o início;
- Etapa 2 depende da correção da issue #11;
- Etapa 3 depende da issue #10.
"""
import sys

import numpy as np
import scipy
from scipy.integrate import quad

import fornecido
from fornecido.energia import FAIXAS_TARIFARIAS, vazao_registrada
from fornecido.simulador import (altura_bomba_real, demanda_real, gerar_ensaio_bomba,
                                 potencia_real, rendimento_real, tarifa, verdade_dia)
from elevatoria.dia import ajustar_polinomio, dia_de_operacao
from elevatoria.integracao import Simpson, Trapezio
from marco1 import MATRICULA


def _ordem(ns: list, erros: list) -> float:
    """Ordem observada: menos a inclinação da reta log(erro) × log(n)."""
    return -float(np.polyfit(np.log(ns), np.log(erros), 1)[0])


def _polinomio(coef) -> str:
    """Texto do polinômio a partir dos coeficientes em ordem crescente: 45.1 − 0.0022·Q²."""
    termos = []
    for k, c in enumerate(coef):
        monomio = f"{abs(c):.5g}" + ("" if k == 0 else "·Q" if k == 1 else f"·Q^{k}")
        termos.append(("−" if c < 0 else "+") + " " + monomio)
    texto = " ".join(termos)
    return texto[2:] if texto.startswith("+") else "−" + texto[2:]


def etapa0() -> None:
    """Etapa 0 — Ambiente."""
    print("=== Etapa 0: ambiente ===")
    print(f"Python {sys.version.split()[0]} | NumPy {np.__version__} | SciPy {scipy.__version__}"
          f" | fornecido {fornecido.VERSAO} | matrícula {MATRICULA}")


def etapa1() -> None:
    """Etapa 1 — Convergência das regras de integração (código pronto)."""
    print("\n=== Etapa 1: convergência das regras de integração ===")
    regras = (Trapezio(), Simpson())

    # (a) Uma função suave: a demanda verdadeira de 0 h a 18 h.
    exato = 810.0 - 180.0 / np.pi
    ns = [4, 8, 16, 32, 64]
    print(f"(a) ∫ demanda de 0 a 18 h; erros para n = {ns}")
    for regra in regras:
        erros = [abs(regra.integrar(demanda_real, 0.0, 18.0, n) - exato) for n in ns]
        ordem = _ordem(ns, erros)
        print(f"    {type(regra).__name__:<9}" + " ".join(f"{e:9.2e}" for e in erros)
              + f"   ordem {ordem:.2f} (teórica {regra.ordem_teorica})")
        assert abs(ordem - regra.ordem_teorica) < 0.25
    assert abs(quad(demanda_real, 0.0, 18.0)[0] - exato) < 1e-9

    # (b) O custo, que tem a tarifa descontínua às 18 h e às 21 h.
    def potencia(t):
        return potencia_real(demanda_real(t))

    def custo(t):
        return potencia(t) * tarifa(t)

    exato = sum(preco * quad(potencia, a, b)[0] for a, b, preco in FAIXAS_TARIFARIAS)
    ns = [30, 50, 70, 90, 110]
    print(f"(b) custo do dia; erros para n = {ns}")
    for regra in regras:
        de_uma_vez = [abs(regra.integrar(custo, 0.0, 24.0, n) - exato) for n in ns]
        por_faixa = [abs(sum(preco * regra.integrar(potencia, a, b, n)
                             for a, b, preco in FAIXAS_TARIFARIAS) - exato) for n in ns]
        ordem_1, ordem_2 = _ordem(ns, de_uma_vez), _ordem(ns, por_faixa)
        print(f"    {type(regra).__name__:<9}de uma vez: ordem {ordem_1:.2f} | "
              f"por faixa: ordem {ordem_2:.2f} (erro em n = 110: {por_faixa[-1]:.1e})")
        assert ordem_1 < 1.5 and abs(ordem_2 - regra.ordem_teorica) < 0.25


def etapa2(matricula: int = MATRICULA) -> None:
    """Etapa 2 — Volume do dia, com falhas no registro (issue #11)."""
    print("\n=== Etapa 2: volume do dia ===")
    t, q = vazao_registrada(matricula)
    passos = sorted(set(np.round(np.diff(t) * 60).astype(int).tolist()))
    print(f"(a) {t.size} leituras de 97; intervalos entre leituras (min): {passos}")
    try:
        Simpson().integrar_tabela(t, q)
        recusou = False
    except ValueError as erro:
        recusou = True
        print(f"    Simpson: recusa ({erro})")
    assert recusou

    volume = 3.6 * Trapezio().integrar_tabela(t, q)
    referencia = verdade_dia()["volume_m3"]
    erro = abs(volume / referencia - 1)
    print(f"(b) volume pelo trapézio: {volume:.1f} m³ (conferência {referencia:.1f} m³; erro {erro:.2%})")
    assert erro < 0.015, "o volume do dia está errado: veja a issue #11"


def etapa3(matricula: int = MATRICULA) -> None:
    """Etapa 3 — Curvas da bomba e custo do dia (issue #10)."""
    print("\n=== Etapa 3: curvas da bomba e custo do dia ===")
    # (a) Ajuste de grau 2 ao ensaio da bomba.
    ensaio = gerar_ensaio_bomba(matricula)
    coef_altura = ajustar_polinomio(ensaio["vazao"], ensaio["altura"], 2)
    coef_rendimento = ajustar_polinomio(ensaio["vazao"], ensaio["rendimento"], 2)
    q = np.linspace(10.0, 100.0, 901)
    erro_h = float(np.max(np.abs(np.polynomial.polynomial.polyval(q, coef_altura) - altura_bomba_real(q))))
    erro_r = float(np.max(np.abs(np.polynomial.polynomial.polyval(q, coef_rendimento) - rendimento_real(q))))
    print(f"(a) altura(Q) = {_polinomio(coef_altura)}   (erro máximo {erro_h:.3f} m)")
    print(f"    rendimento(Q) = {_polinomio(coef_rendimento)}   (erro máximo {erro_r:.4f})")
    assert erro_h < 0.6 and erro_r < 0.02

    # (b) O dia de operação.
    t, vazao = vazao_registrada(matricula)
    resumo = dia_de_operacao(t, vazao, coef_altura, coef_rendimento, Trapezio())
    verdade = verdade_dia()
    print(f"(b) {'faixa':<14}{'tarifa (R$/kWh)':>16}{'custo (R$)':>12}")
    for (inicio, fim, preco), custo in zip(FAIXAS_TARIFARIAS, resumo.custo_por_faixa):
        print(f"    {f'{inicio:g} h a {fim:g} h':<14}{preco:>16.2f}{custo:>12.2f}")
    ponta = resumo.custo_por_faixa[1] / resumo.custo_reais
    print(f"    a ponta é {3 / 24:.1%} das horas do dia e {ponta:.1%} do custo")
    for nome, valor, chave, tolerancia in [("volume (m³)", resumo.volume_m3, "volume_m3", 0.015),
                                           ("energia (kWh)", resumo.energia_kwh, "energia_kwh", 0.03),
                                           ("custo (R$)", resumo.custo_reais, "custo_reais", 0.03)]:
        erro = abs(valor / verdade[chave] - 1)
        print(f"    {nome:<14}{valor:>10.2f}   conferência {verdade[chave]:>9.2f}   erro {erro:.2%}")
        assert erro < tolerancia
    assert abs(sum(resumo.custo_por_faixa) - resumo.custo_reais) < 1e-9


def main() -> None:
    """Executa as etapas do Marco 4."""
    etapa0()
    etapa1()
    etapa2()
    etapa3()
    print("\nMarco 4: todos os assert passaram.")


if __name__ == "__main__":
    main()

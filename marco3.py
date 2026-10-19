"""Marco 3 — Ponto de operação: script de demonstração (PRONTO; NÃO ALTERE).

Execute a partir da raiz do repositório, com o ambiente ativado:  python marco3.py

O script usa a MATRICULA do seu marco1.py e roda em etapas. Ele para no primeiro assert que
falhar ou no primeiro NotImplementedError:

- Etapa 1 só usa código que já existe: roda desde o início;
- Etapa 2 depende da issue #8 (ordem_convergencia) e revela o defeito da issue #9;
- Etapa 3 depende da issue #8 (ponto_operacao).
"""
import sys

import numpy as np
import scipy
from scipy.interpolate import BarycentricInterpolator

import fornecido
from fornecido.hidraulica import Tubulacao, fator_atrito_colebrook
from fornecido.simulador import altura_bomba_real, gerar_ensaio_bomba, ponto_operacao_real
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.operacao import ordem_convergencia, ponto_operacao
from elevatoria.raizes import Bisseccao, Newton
from marco1 import MATRICULA


def etapa0() -> None:
    """Etapa 0 — Ambiente."""
    print("=== Etapa 0: ambiente ===")
    print(f"Python {sys.version.split()[0]} | NumPy {np.__version__} | SciPy {scipy.__version__}"
          f" | fornecido {fornecido.VERSAO} | matrícula {MATRICULA}")


def etapa1(matricula: int = MATRICULA) -> dict:
    """Etapa 1 — Interpolação do ensaio da bomba (código pronto). Devolve as curvas."""
    print("\n=== Etapa 1: interpolação do ensaio da bomba ===")
    ensaio = gerar_ensaio_bomba(matricula)
    vazao, altura = ensaio["vazao"], ensaio["altura"]
    curvas = {metodo: CurvaCalibracao(vazao, altura, metodo) for metodo in ("linear", "spline")}
    polinomio = BarycentricInterpolator(vazao, altura)   # grau 10: passa pelos 11 pontos

    # (a) Erro máximo de cada interpolação em relação à curva verdadeira, de 0 a 100 L/s.
    q = np.linspace(0.0, 100.0, 1001)
    real = altura_bomba_real(q)
    erros = {nome: float(np.max(np.abs(curva(q) - real))) for nome, curva in curvas.items()}
    erros["polinomial"] = float(np.max(np.abs(polinomio(q) - real)))
    print(f"(a) ensaio: {len(vazao)} pontos, de {vazao[0]:g} a {vazao[-1]:g} L/s")
    for nome, erro in erros.items():
        print(f"    {nome:<11} erro máximo em [0, 100] L/s = {erro:.3f} m")
    assert erros["linear"] < 1.0 and erros["spline"] < 1.0

    # (b) Extrapolação: Q = 130 L/s, fora do ensaio.
    q_fora = 130.0
    real_fora = float(altura_bomba_real(q_fora))
    erro_polinomio = abs(float(polinomio(q_fora)) - real_fora)
    print(f"(b) Q = {q_fora:g} L/s: altura verdadeira {real_fora:.2f} m; "
          f"polinômio {float(polinomio(q_fora)):.2f} m (erro {erro_polinomio:.1f} m)")
    try:
        curvas["spline"](q_fora)
        recusou = False
    except ValueError as erro:
        recusou = True
        print(f"    spline: recusa ({erro})")
    assert erro_polinomio > 10 and recusou
    return curvas


def etapa2() -> None:
    """Etapa 2 — Fator de atrito: bissecção × Newton (issues #8 e #9)."""
    print("\n=== Etapa 2: fator de atrito (Colebrook) ===")
    rugosidade_relativa = 0.15e-3 / 0.20
    esperado = {1e4: 0.03202, 1e5: 0.02130, 1e6: 0.01871}

    # (a) As duas soluções e o número de iterações (só código pronto).
    print(f"(a) {'Re':>7}{'f':>10}{'iterações bissecção':>22}{'iterações Newton':>19}")
    newton = {}
    for reynolds, f_esperado in esperado.items():
        f_bis, r_bis = fator_atrito_colebrook(reynolds, rugosidade_relativa, Bisseccao(tol=1e-12))
        f_new, r_new = fator_atrito_colebrook(reynolds, rugosidade_relativa, Newton(tol=1e-12))
        print(f"    {reynolds:>7.0e}{f_new:>10.5f}{r_bis.iteracoes:>22}{r_new.iteracoes:>19}")
        assert abs(f_bis - f_new) < 1e-10 and abs(f_new - f_esperado) < 5e-5
        newton[reynolds] = r_new

    # (b) A ordem de convergência do Newton (com a sua ordem_convergencia).
    for reynolds, resultado in newton.items():
        erros = " ".join(f"{abs(x - resultado.raiz):.1e}" for x in resultado.historico)
        ordem = ordem_convergencia(resultado.historico, resultado.raiz)
        print(f"(b) Re = {reynolds:.0e}: erros {erros}")
        print(f"    ordem de convergência estimada: {ordem:.2f}")
        assert ordem > 1.8, "o Newton não está convergindo quadraticamente (issue #9)"


def etapa3(curvas: dict) -> None:
    """Etapa 3 — Ponto de operação (issue #8)."""
    print("\n=== Etapa 3: ponto de operação ===")
    tubulacao = Tubulacao(0.20, 850.0, 0.15e-3, 18.0, Newton(tol=1e-12))
    q_real, h_real = ponto_operacao_real()
    print(f"    {'curva':<8}{'método':<11}{'Q (L/s)':>10}{'H (m)':>9}{'iterações':>11}{'ordem':>7}")
    for nome, curva in curvas.items():
        pontos = {}
        for metodo in (Bisseccao(tol=1e-10), Newton(tol=1e-10)):
            ponto = ponto_operacao(curva, tubulacao, metodo)
            pontos[type(metodo).__name__] = ponto
            ordem = "—"
            if isinstance(metodo, Newton):
                try:
                    ordem = f"{ordem_convergencia(ponto.resultado.historico, ponto.vazao):.2f}"
                except ValueError:
                    pass
            print(f"    {nome:<8}{type(metodo).__name__:<11}{ponto.vazao:>10.3f}{ponto.altura:>9.3f}"
                  f"{ponto.resultado.iteracoes:>11}{ordem:>7}")
        bis, new = pontos["Bisseccao"], pontos["Newton"]
        assert abs(bis.vazao - new.vazao) < 1e-6
        assert abs(new.vazao - q_real) < 1.0
        assert new.resultado.iteracoes < bis.resultado.iteracoes / 3
    print(f"    ponto de operação verdadeiro (conferência): Q = {q_real:.3f} L/s, H = {h_real:.3f} m")


def main() -> None:
    """Executa as etapas do Marco 3."""
    etapa0()
    curvas = etapa1()
    etapa2()
    etapa3(curvas)
    print("\nMarco 3: todos os assert passaram.")


if __name__ == "__main__":
    main()

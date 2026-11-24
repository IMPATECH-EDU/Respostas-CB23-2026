"""Roda o projeto nesta máquina e gera o RELATORIO.md final, para o envio 5.

Uso (PowerShell, dentro da pasta upload_3508), depois do envio 1:

    & $HOME\\venvs\\prog2-venv\\Scripts\\python.exe preparar_relatorio.py HASH

HASH é o código curto (7 caracteres) do commit do envio 1, que aparece no GitHub.

O programa roda os 108 testes e o marco1.py a marco4.py na pasta projeto_completo e grava
5_relatorio/RELATORIO.md com: o hash das previsões, o seu Python, a Etapa 0 dos Marcos 1 e 2 e
a coluna "Medido" da R5 com os seus tempos. Pode rodar quantas vezes quiser: o relatório é
sempre gerado de novo a partir do modelo em projeto_completo/RELATORIO.md.
"""
import math
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PROJETO = AQUI / "projeto_completo"
SAIDA = AQUI / "5_relatorio" / "RELATORIO.md"


def parar(mensagem: str) -> None:
    """Mostra o erro e encerra sem gravar nada."""
    print(f"\nERRO: {mensagem}")
    sys.exit(1)


def numero_br(x: float, casas: int) -> str:
    """Número com vírgula decimal: 23.04 -> '23,0' (com casas=1)."""
    return f"{x:.{casas}f}".replace(".", ",")


def inteiro_br(n: int) -> str:
    """Inteiro com espaço como separador de milhar: 36000056 -> '36 000 056'."""
    return f"{n:,}".replace(",", " ")


def rodar(*argumentos: str) -> str:
    """Roda o Python do ambiente dentro de projeto_completo e devolve a saída; para se falhar."""
    ambiente = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    feito = subprocess.run([sys.executable, *argumentos], cwd=PROJETO, env=ambiente,
                           capture_output=True, text=True, encoding="utf-8")
    saida = feito.stdout + feito.stderr
    if feito.returncode != 0:
        print(saida[-3000:])
        parar(f"'python {' '.join(argumentos)}' falhou (a saída está acima)")
    return saida


def etapa0(saida: str) -> str:
    """A linha logo depois de '=== Etapa 0: ambiente ==='."""
    linhas = saida.splitlines()
    return linhas[linhas.index("=== Etapa 0: ambiente ===") + 1].strip()


def valor(saida: str, padrao: str) -> str:
    """Primeiro grupo do padrão na saída do marco1.py."""
    achado = re.search(padrao, saida, re.MULTILINE)
    if achado is None:
        parar(f"não achei {padrao!r} na saída do marco1.py")
    return achado.group(1)


def trocar(texto: str, velho: str, novo: str) -> str:
    """Troca exatamente uma ocorrência; para com erro se não houver exatamente uma."""
    if texto.count(velho) != 1:
        parar(f"trecho não encontrado no modelo do relatório: {velho[:60]!r}")
    return texto.replace(velho, novo)


def paragrafo_r5(r_vet: float, r_comp: float) -> str:
    """Parágrafo da R5: a explicação depende de qual previsão ficou mais longe da medição."""
    vet_txt, comp_txt = numero_br(r_vet, 0), numero_br(r_comp, 2)
    if abs(math.log(r_vet / 50)) >= abs(math.log(r_comp / 0.7)):
        if r_vet < 50:
            abertura = (f"A maior diferença foi no laço ÷ vetorizado: previ 50× e medi {vet_txt}×. A "
                        "versão vetorizada não é só uma multiplicação. Ela converte o `int64` para "
                        "`float64` (uma cópia de 8 MB) e cria mais dois vetores temporários, um em "
                        "`* 600` e outro em `/ 4095`. Então ela passa três vezes por 8 MB de memória, e "
                        "com 1 milhão de elementos a memória limita mais que a conta.")
        else:
            abertura = (f"A maior diferença foi no laço ÷ vetorizado: previ 50× e medi {vet_txt}×. O "
                        "laço em Python custa mais do que eu imaginava. A cada elemento, o interpretador "
                        "cria um `float` novo, faz duas operações com verificação de tipo e chama o "
                        "`append`, enquanto o NumPy faz a mesma conta em C, sobre um bloco contíguo de "
                        "memória e sem criar objetos.")
    elif r_comp > 0.7:
        abertura = (f"A maior diferença foi na compreensão ÷ laço: previ 0,7 e medi {comp_txt}. A "
                    "compreensão só economiza a busca do método `append` e a chamada dele. O grosso do "
                    "tempo vai na conta `c * 600 / 4095`, que cria um `float` novo por elemento nas duas "
                    "versões, e por isso o ganho foi menor do que eu esperava. O vetorizado foi "
                    f"{vet_txt}× mais rápido que o laço (eu previa 50×).")
    else:
        abertura = (f"A maior diferença foi na compreensão ÷ laço: previ 0,7 e medi {comp_txt}. A "
                    "compreensão foi ainda mais rápida do que eu previa: além de evitar a busca e a "
                    "chamada do `append`, ela usa uma instrução própria do interpretador para "
                    f"acrescentar à lista. O vetorizado foi {vet_txt}× mais rápido que o laço (eu "
                    "previa 50×).")
    fecho = ("`uint16 * 20` dá 16364 porque o NumPy mantém o resultado em `uint16`, que vai até "
             "65535: 81900 dá a volta, e 81900 − 65536 = 16364, sem nenhum aviso. Eu guardaria as "
             "contagens em `uint16` (12 bits cabem em 2 B), convertendo para `float64` antes de "
             "qualquer conta, e as pressões em kPa em `float64`.")
    return textwrap.fill(abertura + " " + fecho, width=99, break_on_hyphens=False)


def main() -> None:
    """Confere o ambiente, roda tudo e grava o relatório final."""
    if len(sys.argv) != 2 or not re.fullmatch(r"[0-9a-f]{7,40}", sys.argv[1]):
        parar("passe o hash do commit do envio 1 (7 letras/números, ex.: 3f9a2c1), como no LEIA-ME")
    hash_previsoes = sys.argv[1][:7]
    if "prog2-venv" not in sys.executable:
        parar(f"este não é o Python do ambiente prog2-venv: {sys.executable}")
    try:
        import numpy, scipy  # noqa: F401
    except ImportError:
        parar("faltam NumPy/SciPy. Rode: & $HOME\\venvs\\prog2-venv\\Scripts\\python.exe -m pip install numpy scipy")

    print("Rodando os testes...")
    testes = rodar("-m", "unittest", "discover")
    print("  " + " | ".join(l for l in testes.splitlines() if l.startswith(("Ran ", "OK"))))
    saidas = {}
    for m in (1, 2, 3, 4):
        saidas[m] = rodar(f"marco{m}.py")
        print(f"  marco{m}.py: {saidas[m].strip().splitlines()[-1]}")

    relatorio = (PROJETO / "RELATORIO.md").read_text(encoding="utf-8")
    relatorio = trocar(relatorio, "`HASH_DAS_PREVISOES`", f"`{hash_previsoes}`")
    relatorio = trocar(relatorio, "Windows 11, Git Bash, ambiente", "Windows 11 (PowerShell), ambiente")
    relatorio = trocar(relatorio, "$ which python\n/usr/local/bin/python3\n",
                       f"$ where python\n{sys.executable}\n")
    relatorio = trocar(relatorio, "Python 3.13.18 | NumPy 2.5.3 | fornecido 4.0\n", etapa0(saidas[1]) + "\n")
    relatorio = trocar(relatorio, "Python 3.13.18 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3508\n",
                       etapa0(saidas[2]) + "\n")

    s1 = saidas[1]
    b_lista = int(valor(s1, r"^\s+list\s+[\d.]+\s+([\d,]+)").replace(",", ""))
    b_uint16 = int(valor(s1, r"^\s+uint16\s+[\d.]+\s+([\d,]+)").replace(",", ""))
    t_laco = float(valor(s1, r"^\s+laço\s+([\d.]+)"))
    t_comp = float(valor(s1, r"^\s+compreensão\s+([\d.]+)"))
    t_vet = float(valor(s1, r"^\s+vetorizado\s+([\d.]+)"))
    r_mem, r_vet, r_comp = b_lista / b_uint16, t_laco / t_vet, t_comp / t_laco
    relatorio = trocar(relatorio, "| 18,0× (36 000 056 B / 2 000 000 B) |",
                       f"| {numero_br(r_mem, 1)}× ({inteiro_br(b_lista)} B / {inteiro_br(b_uint16)} B) |")
    relatorio = trocar(relatorio, "| 23,0× (61,88 ms / 2,69 ms) |",
                       f"| {numero_br(r_vet, 1)}× ({numero_br(t_laco, 2)} ms / {numero_br(t_vet, 2)} ms) |")
    relatorio = trocar(relatorio, "| 0,81 (50,13 ms / 61,88 ms) |",
                       f"| {numero_br(r_comp, 2)} ({numero_br(t_comp, 2)} ms / {numero_br(t_laco, 2)} ms) |")
    inicio = relatorio.index("A maior diferença foi no laço ÷ vetorizado")
    fim = relatorio.index("\n\n### R6")
    novo_paragrafo = paragrafo_r5(r_vet, r_comp)
    relatorio = relatorio[:inicio] + novo_paragrafo + relatorio[fim:]

    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text(relatorio, encoding="utf-8", newline="\n")
    print(f"\nPronto: {SAIDA}")
    print(f"  lista / uint16 = {numero_br(r_mem, 1)}× | laço / vetorizado = {numero_br(r_vet, 1)}× | "
          f"compreensão / laço = {numero_br(r_comp, 2)}")
    print("\nParágrafo da R5 com os seus números (leia e confira se concorda):\n")
    print(novo_paragrafo)


if __name__ == "__main__":
    main()

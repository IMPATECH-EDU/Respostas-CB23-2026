# Projeto Elevatória — Marco 2: Medição (Aula 9, 19/10)

O fluxo de trabalho (fork, branch, Pull Request) e as regras da casa estão no `README.md`
deste repositório; as regras gerais do projeto (uso de IA, antiplágio e prazo final de
23/11/2026), no documento principal da disciplina. Este arquivo descreve só o Marco 2. Data
sugerida para concluí-lo: **02/11**.

## A situação

O seu leitor de log já está em uso, e a primeira reclamação chegou: pela escala nominal, a
pressão de recalque dá cerca de 262 kPa, quando deveria dar 380 kPa (Etapa 2(f) do Marco 1).
A resposta do transmissor não é linear. Enquanto você trabalhava no Marco 1, outras pessoas
escreveram as peças para resolver isso:

- um colega escreveu a **curva de calibração**, que converte contagens em kPa interpolando a
  tabela do fabricante com o SciPy;
- a equipe de metrologia entregou a classe **`Medida`** (valor ± incerteza), que propaga
  incertezas nas contas;
- outro colega escreveu os **totalizadores** de pulsos, e já há um relato de defeito neles.

Neste marco você escreve pouco código, mas código que junta tudo isso: as peças dos colegas,
a biblioteca científica e o seu leitor do Marco 1. Para isso, é preciso ler e entender o
código dos outros antes de usá-lo. Você também vai corrigir um defeito numérico sutil.

**Neste marco você vai:**

- integrar o seu código com o de outras pessoas e com o SciPy, respeitando os contratos;
- detectar leituras espúrias com estatística robusta (mediana e MAD);
- usar uma classe de outra equipe para propagar incertezas;
- diagnosticar e corrigir um defeito de ponto flutuante, com teste de regressão;
- observar, na saída do script, os erros de truncamento e de arredondamento de uma derivada
  numérica.

## 1. Preparação

**Trazer o Marco 2 para a sua branch:**

```bash
git switch projeto_<sua_matricula>
git pull --no-rebase --no-edit upstream main
git push
```

O Marco 2 só acrescenta arquivos novos e atualiza `fornecido/`: nada do que você fez no
Marco 1 muda.

**Instalar o SciPy**, com o ambiente do projeto ativo:

```bash
source ~/venvs/prog2-venv/bin/activate
python -m pip install scipy
```

**Primeira execução:** rode `python marco2.py`. A Etapa 1 já funciona, porque só usa código
pronto. A Etapa 2 para com um `AssertionError`: é o defeito da issue #7.

## 2. O que chegou na base

```
Respostas-CB23-2026/
├── ENUNCIADO_MARCO2.md          # este arquivo
├── marco2.py                    # script do marco: PRONTO, não altere
├── fornecido/
│   ├── medida.py                #   Medida: valor ± incerteza (equipe de metrologia)
│   └── testes_aceitacao/
│       └── test_aceitacao_m2.py #   testes de aceitação do Marco 2
├── elevatoria/
│   ├── calibracao.py            #   CurvaCalibracao (colega): pronta, sem issues
│   ├── acumuladores.py          #   totalizadores (colega): issue #7
│   └── medicao.py               #   esqueleto: issue #6 (é aqui que você escreve)
└── testes/
    └── test_medicao.py          # os seus testes do Marco 2 (há um exemplo)
```

Você mexe em **dois arquivos de código**: `elevatoria/medicao.py` (duas funções) e
`elevatoria/acumuladores.py` (o defeito). Além deles, nos seus testes e no `RELATORIO.md`.
Leia as docstrings de `calibracao.py` e de `fornecido/medida.py` antes de começar: elas são
o contrato do que você vai usar.

## 3. Issues abertas

### #6 — Medição de pressão

**Arquivo:** `elevatoria/medicao.py` (funções `medir` e `altura_manometrica`).

**Descrição.** `medir(registros, tag, curva, u_sistematica)` transforma as contagens de um
transmissor, registradas no log, em uma medida de pressão com incerteza. Ela não faz quase
nada sozinha: encadeia peças que já existem.

| Passo | De onde vem |
| --- | --- |
| As contagens da tag no log | `serie`, do seu Marco 1 (`elevatoria/dados.py`) |
| Contagens → kPa | `CurvaCalibracao`, do colega (`elevatoria/calibracao.py`) |
| Descartar as leituras espúrias (z robusto) | `numpy` e `scipy.stats.median_abs_deviation` |
| Média, desvio e erro padrão | `numpy` e `scipy.stats.sem` |
| O resultado: valor ± incerteza | `Medida`, da metrologia (`fornecido/medida.py`) |

`altura_manometrica(registros, curva)` usa `medir` nos dois transmissores e calcula a altura
manométrica da bomba com `Medida`, que propaga as incertezas sozinha. A docstring de cada
função traz o contrato completo: os passos, as fórmulas e quando levantar `ValueError`.

A issue #6 usa a sua `serie` do Marco 1: ela só funciona com a issue #1 resolvida.

**Critério de aceitação.** Os testes de aceitação de `medir` e `altura_manometrica` passam, e
a Etapa 3 do `marco2.py` roda com a sua matrícula.

### #7 — BUG: o `AcumuladorKahan` não compensa nada

**Arquivo:** `elevatoria/acumuladores.py`.

**Relato.** "Totalizei 1 000 000 de pulsos de 0,1 L com o `AcumuladorKahan` e obtive
`100000.00000133288`, exatamente o mesmo resultado do `AcumuladorIngenuo`. A soma de Kahan
deveria dar `100000.0`. Os testes de aceitação passam, por isso ninguém tinha notado."

**Critério de aceitação.**

1. **Antes** de corrigir, escreva em `testes/test_medicao.py` pelo menos dois testes de
   regressão que falhem com o código atual. Confirme que eles falham.
2. Corrija o defeito mudando o mínimo possível. Os testes de aceitação continuam passando, os
   seus passam a passar, e a Etapa 2 do `marco2.py` roda.
3. Na correção, os seus testes serão rodados também contra o código original: pelo menos um
   deles precisa falhar.

## 4. O script `marco2.py`

O script vem pronto: **não o altere**. Ele usa a `MATRICULA` do seu `marco1.py` e para no
primeiro `assert` que falhar.

- **Etapa 1, Calibração.** Erro das curvas linear e spline e a tabela do erro de uma derivada
  numérica em função do passo `h`. Usa só código pronto.
- **Etapa 2, Totalizador (#7).** Um milhão de parcelas de 0,1 L com os três acumuladores.
- **Etapa 3, Medição (#6).** As pressões de `PT101` e `PT102` com as duas curvas e a altura
  manométrica.

## 5. Testes

Rode tudo com `python -m unittest discover -v`. Os testes de aceitação dos dois marcos devem
passar, assim como os seus testes do Marco 1.

Em `testes/test_medicao.py`, escreva **pelo menos 4 testes**, sem contar o exemplo, com uma
docstring de uma linha em cada um:

- pelo menos 2 testes de regressão da issue #7, escritos antes da correção;
- pelo menos 2 testes de `medir` que os testes de aceitação não cobrem. Releia a docstring:
  há regras do contrato que eles não verificam.

## 6. Relatório: seção "Marco 2" do `RELATORIO.md`

Copie o modelo abaixo para o fim do seu `RELATORIO.md` e responda com as suas palavras e com
os números da sua execução, em até 6 linhas por pergunta.

```markdown
## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->
```

## 7. Entrega

**Descrição do Pull Request.** Acrescente à descrição do seu PR, abaixo da seção do Marco 1:

```markdown
## Marco 2
Resolve as issues #6 e #7 do enunciado.

### O que mudou
- ...

### Como testei
- `python -m unittest discover -v`: N testes, todos passando
- `python marco1.py` e `python marco2.py`: todos os assert passam

### Pontos de atenção para o revisor
- ...
```

**Checklist do Marco 2**

- [ ] `git fetch upstream` seguido de `git diff upstream/main --stat -- fornecido/ marco2.py`
      não mostra nada (você não alterou o código fornecido nem o script).
- [ ] `python -m unittest discover -v` roda sem falhas, com pelo menos 4 testes seus do Marco 2.
- [ ] `python marco1.py` e `python marco2.py` rodam sem exceções.
- [ ] O código novo tem docstrings e anotações de tipo, e `elevatoria/` não tem `print`.
- [ ] Os testes de regressão da #7 falhavam antes da correção.
- [ ] O `RELATORIO.md` tem a seção "Marco 2", com o ambiente e as respostas R8 a R10.
- [ ] Todo o código foi executado, testado e lido por você, inclusive o gerado com ajuda de IA.

## 8. Material complementar (opcional)

- https://docs.scipy.org/doc/scipy/reference/stats.html
- https://docs.scipy.org/doc/scipy/tutorial/interpolate.html
- https://docs.python.org/3/tutorial/floatingpoint.html
- https://en.wikipedia.org/wiki/Kahan_summation_algorithm

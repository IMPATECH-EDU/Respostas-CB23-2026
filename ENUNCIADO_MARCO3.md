# Projeto Elevatória — Marco 3: Raízes e interpolação (Aula 10, 26/10)

O fluxo de trabalho (fork, branch, Pull Request) e as regras da casa estão no `README.md`
deste repositório; as regras gerais do projeto (uso de IA, antiplágio e prazo final de
23/11/2026), no documento principal da disciplina. Este arquivo descreve só o Marco 3. Data
sugerida para concluí-lo: **09/11**.

## A situação

Com as pressões medidas no Marco 2, a equipe quer prever em que vazão a bomba trabalha: o
**ponto de operação**, em que a altura que a bomba fornece é igual à altura que o sistema
exige. É a raiz de uma equação que não se resolve à mão. Três peças chegaram à base:

- a equipe de hidráulica entregou o **modelo da adutora** (`fornecido/hidraulica.py`). Ele
  precisa resolver uma equação implícita, mas não traz um método de raiz: recebe um
  *resolvedor* de fora;
- um colega escreveu os **métodos de raiz**, bissecção e Newton (`elevatoria/raizes.py`), e
  já há um relato de defeito no Newton;
- a **curva da bomba** sai do ensaio do fabricante, com 11 pontos, interpolado pela
  `CurvaCalibracao` do Marco 2.

Como no Marco 2, você escreve pouco código, mas código que junta tudo isso. A estação
continua sendo só o cenário: as fórmulas de engenharia já estão no código fornecido.

**Neste marco você vai:**

- integrar código de três origens: o modelo de outra equipe, os métodos de um colega e a
  curva do Marco 2;
- usar o mesmo método de raiz em dois problemas, um dentro do outro (composição);
- medir a ordem de convergência de um método a partir das suas iterações;
- diagnosticar e corrigir um defeito que não muda o resultado, só a velocidade;
- observar, na saída do script, os riscos da interpolação polinomial e da extrapolação.

## 1. Preparação

**Trazer o Marco 3 para a sua branch:**

```bash
git switch projeto_<sua_matricula>
git pull --no-rebase --no-edit upstream main
git push
```

Não há nada novo a instalar. Este marco não depende do seu código dos Marcos 1 e 2: só da
`MATRICULA` do seu `marco1.py`.

**Primeira execução:** rode `python marco3.py`. A Etapa 1 já funciona, porque só usa código
pronto. A Etapa 2 imprime uma tabela e para com `NotImplementedError`: é a issue #8.

## 2. O que chegou na base

```
Respostas-CB23-2026/
├── ENUNCIADO_MARCO3.md          # este arquivo
├── marco3.py                    # script do marco: PRONTO, não altere
├── fornecido/
│   ├── hidraulica.py            #   Tubulacao e Colebrook (equipe de hidráulica)
│   └── testes_aceitacao/
│       └── test_aceitacao_m3.py #   testes de aceitação do Marco 3
├── elevatoria/
│   ├── raizes.py                #   Bisseccao e Newton (colega): issue #9
│   └── operacao.py              #   esqueleto: issue #8 (é aqui que você escreve)
└── testes/
    └── test_operacao.py         # os seus testes do Marco 3 (há um exemplo)
```

Você mexe em **dois arquivos de código**: `elevatoria/operacao.py` (duas funções) e
`elevatoria/raizes.py` (o defeito). Além deles, nos seus testes e no `RELATORIO.md`. Leia
antes as docstrings de `fornecido/hidraulica.py` (em especial o protocolo `Resolvedor`) e de
`elevatoria/raizes.py`: elas são o contrato do que você vai usar.

## 3. Issues abertas

### #8 — Ponto de operação e ordem de convergência

**Arquivo:** `elevatoria/operacao.py` (funções `ponto_operacao` e `ordem_convergencia`).

**Descrição.** `ponto_operacao(bomba, tubulacao, resolvedor)` encontra a vazão `Q` em que
`bomba(Q) = tubulacao.altura_sistema(Q)`, isto é, a raiz de
`f(Q) = bomba(Q) − tubulacao.altura_sistema(Q)`. Ela encadeia peças que já existem:

| Peça | De onde vem |
| --- | --- |
| `bomba(Q)`: a altura que a bomba fornece | `CurvaCalibracao` do ensaio (`elevatoria/calibracao.py`, Marco 2) |
| `tubulacao.altura_sistema(Q)`: a altura que o sistema exige | `Tubulacao`, da equipe de hidráulica (`fornecido/hidraulica.py`) |
| A raiz de `f` | `Bisseccao` ou `Newton`, do colega (`elevatoria/raizes.py`) |

Repare que a própria `Tubulacao` recebe um resolvedor: a cada avaliação de `f`, ela resolve a
equação de Colebrook para obter o fator de atrito. São dois problemas de raiz, um dentro do
outro, e os mesmos métodos servem aos dois.

`ordem_convergencia(historico, raiz)` estima a ordem de convergência `p` de um método a
partir das aproximações que ele produziu (o `historico` do `ResultadoRaiz`). É com ela que o
`marco3.py` confere se o Newton converge como deveria.

A docstring de cada função traz o contrato completo: os passos, a fórmula e quando levantar
`ValueError`.

**Critério de aceitação.** Os testes de aceitação de `ponto_operacao` e de
`ordem_convergencia` passam, e as Etapas 2(b) e 3 do `marco3.py` rodam.

### #9 — BUG: o Newton está lento

**Arquivo:** `elevatoria/raizes.py`.

**Relato.** "O fator de atrito sai certo com o `Newton`, mas ele leva 10 iterações para
Re = 10⁴, quando deveria levar umas 5. Pela teoria, o número de dígitos corretos deveria
dobrar a cada iteração, e não é o que acontece. Os testes de aceitação passam, por isso
ninguém tinha notado."

**Critério de aceitação.**

1. **Antes** de corrigir, escreva em `testes/test_operacao.py` pelo menos dois testes de
   regressão que falhem com o código atual. Confirme que eles falham.
2. Corrija o defeito mudando o mínimo possível. Os testes de aceitação continuam passando, os
   seus passam a passar, e a Etapa 2 do `marco3.py` roda.
3. Na correção, os seus testes serão rodados também contra o código original: pelo menos um
   deles precisa falhar.

## 4. O script `marco3.py`

O script vem pronto: **não o altere**. Ele usa a `MATRICULA` do seu `marco1.py` e para no
primeiro `assert` que falhar.

- **Etapa 1, Interpolação.** O ensaio da bomba interpolado de três formas (linear, spline e
  um polinômio de grau 10) e uma tentativa de extrapolação. Usa só código pronto.
- **Etapa 2, Fator de atrito (#8 e #9).** A equação de Colebrook resolvida pela bissecção e
  pelo Newton: (a) o número de iterações; (b) os erros e a ordem de convergência do Newton.
- **Etapa 3, Ponto de operação (#8).** O ponto de operação com as duas curvas e os dois
  métodos, comparado com o valor de conferência.

## 5. Testes

Rode tudo com `python -m unittest discover -v`. Os testes de aceitação dos três marcos devem
passar, assim como os seus testes dos marcos anteriores.

Em `testes/test_operacao.py`, escreva **pelo menos 4 testes**, sem contar o exemplo, com uma
docstring de uma linha em cada um:

- pelo menos 2 testes de regressão da issue #9, escritos antes da correção;
- pelo menos 2 testes de `ponto_operacao` ou de `ordem_convergencia` que os testes de
  aceitação não cobrem. Releia as docstrings: há regras do contrato que eles não verificam.

## 6. Relatório: seção "Marco 3" do `RELATORIO.md`

Copie o modelo abaixo para o fim do seu `RELATORIO.md` e responda com as suas palavras e com
os números da sua execução, em até 6 linhas por pergunta.

```markdown
## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->

```

## 7. Entrega

**Descrição do Pull Request.** Acrescente à descrição do seu PR, abaixo da seção do Marco 2:

```markdown
## Marco 3
Resolve as issues #8 e #9 do enunciado.

### O que mudou
- ...

### Como testei
- `python -m unittest discover -v`: N testes, todos passando
- `python marco3.py`: todos os assert passam

### Pontos de atenção para o revisor
- ...
```

**Checklist do Marco 3**

- [ ] `git fetch upstream` seguido de
      `git diff upstream/main --stat -- fornecido/ marco2.py marco3.py` não mostra nada
      (você não alterou o código fornecido nem os scripts).
- [ ] `python -m unittest discover -v` roda sem falhas, com pelo menos 4 testes seus do Marco 3.
- [ ] `python marco3.py` roda sem exceções.
- [ ] O código novo tem docstrings e anotações de tipo, e `elevatoria/` não tem `print`.
- [ ] Os testes de regressão da #9 falhavam antes da correção.
- [ ] O `RELATORIO.md` tem a seção "Marco 3", com as respostas R11 a R13.
- [ ] Todo o código foi executado, testado e lido por você, inclusive o gerado com ajuda de IA.

## 8. Material complementar (opcional)

- https://en.wikipedia.org/wiki/Bisection_method
- https://en.wikipedia.org/wiki/Newton%27s_method
- https://en.wikipedia.org/wiki/Rate_of_convergence
- https://en.wikipedia.org/wiki/Runge%27s_phenomenon
- https://docs.python.org/3/library/typing.html#typing.Protocol

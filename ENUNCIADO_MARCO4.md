# Projeto Elevatória — Marco 4: Ajuste e integração (Aula 11, 09/11)

O fluxo de trabalho (fork, branch, Pull Request) e as regras da casa estão no `README.md`
deste repositório; as regras gerais do projeto (uso de IA, antiplágio e prazo final de
23/11/2026), no documento principal da disciplina. Este arquivo descreve só o Marco 4. Data
sugerida para concluí-lo: **16/11**.

## A situação

Com o ponto de operação do Marco 3, a equipe quer o balanço de um dia inteiro: quanto se
bombeou, quanta energia se gastou e quanto isso custou, sabendo que a energia é três vezes
mais cara das 18 h às 21 h (a "ponta"). Três peças chegaram à base:

- a equipe de energia entregou o **registro de vazão do dia**, a fórmula da potência e as
  faixas tarifárias (`fornecido/energia.py`). O registro tem falhas: o SCADA perdeu 8 das 97
  leituras do dia;
- um colega escreveu as **regras de integração**, trapézio e Simpson
  (`elevatoria/integracao.py`), e já há um relato de defeito;
- as **curvas da bomba** saem do mesmo ensaio do Marco 3, agora por **ajuste** de mínimos
  quadrados, que filtra o ruído, em vez de interpolação, que passa por ele.

Como nos Marcos 2 e 3, você escreve pouco código, mas código que junta tudo isso. A estação
continua sendo só o cenário: as fórmulas de engenharia já estão no código fornecido.

**Neste marco você vai:**

- ajustar curvas por mínimos quadrados, escolhendo um dos métodos do NumPy ou do SciPy;
- integrar dados medidos em uma malha irregular, escolhendo a regra adequada;
- integrar por faixas para respeitar a descontinuidade da tarifa;
- diagnosticar e corrigir um defeito que só aparece com dados reais;
- observar, na saída do script, a ordem de convergência do trapézio e do Simpson e o efeito
  de uma descontinuidade.

## 1. Preparação

**Trazer o Marco 4 para a sua branch:**

```bash
git switch projeto_<sua_matricula>
git pull --no-rebase --no-edit upstream main
git push
```

Não há nada novo a instalar. Este marco não depende do seu código dos Marcos 1 a 3: só da
`MATRICULA` do seu `marco1.py`.

**Primeira execução:** rode `python marco4.py`. A Etapa 1 já funciona, porque só usa código
pronto. A Etapa 2 para com um `AssertionError`: é o defeito da issue #11.

## 2. O que chegou na base

```
Respostas-CB23-2026/
├── ENUNCIADO_MARCO4.md          # este arquivo
├── marco4.py                    # script do marco: PRONTO, não altere
├── fornecido/
│   ├── energia.py               #   registro do dia, potência e tarifas (equipe de energia)
│   └── testes_aceitacao/
│       └── test_aceitacao_m4.py #   testes de aceitação do Marco 4
├── elevatoria/
│   ├── integracao.py            #   Trapezio e Simpson (colega): issue #11
│   └── dia.py                   #   esqueleto: issue #10 (é aqui que você escreve)
└── testes/
    └── test_dia.py              # os seus testes do Marco 4 (há um exemplo)
```

Você mexe em **dois arquivos de código**: `elevatoria/dia.py` (duas funções) e
`elevatoria/integracao.py` (o defeito). Além deles, nos seus testes e no `RELATORIO.md`. Leia
antes as docstrings de `fornecido/energia.py` e de `elevatoria/integracao.py`: elas são o
contrato do que você vai usar.

## 3. Issues abertas

### #10 — Curvas da bomba e balanço do dia

**Arquivo:** `elevatoria/dia.py` (funções `ajustar_polinomio` e `dia_de_operacao`).

**Descrição.** `ajustar_polinomio(x, y, grau)` devolve os coeficientes do polinômio de mínimos
quadrados. O NumPy e o SciPy têm mais de um método para isso, e a escolha é sua: a docstring
indica alguns pontos de partida. É com essa função que o `marco4.py` ajusta as curvas de altura
e de rendimento da bomba ao ensaio.

`dia_de_operacao(t, vazao, coef_altura, coef_rendimento, integrador)` faz o balanço do dia a
partir do registro de vazão. Ela encadeia peças que já existem:

| Passo | De onde vem |
| --- | --- |
| Altura e rendimento em cada instante | os coeficientes de `ajustar_polinomio` e `np.polynomial.polynomial.polyval` |
| Potência em cada instante | `potencia_eletrica`, da equipe de energia (`fornecido/energia.py`) |
| Volume, energia e custo de cada faixa | `integrador.integrar_tabela`, do colega (`elevatoria/integracao.py`) |
| As faixas e as tarifas | `FAIXAS_TARIFARIAS` (`fornecido/energia.py`) |

O custo é integrado **faixa por faixa**, com a tarifa constante em cada uma. A Etapa 1 do
`marco4.py` mostra por que integrar o custo do dia de uma vez é uma má ideia.

A docstring de cada função traz o contrato completo: os passos, as fórmulas e quando levantar
`ValueError`.

**Critério de aceitação.** Os testes de aceitação de `ajustar_polinomio` e de
`dia_de_operacao` passam, e a Etapa 3 do `marco4.py` roda.

### #11 — BUG: o volume do dia está errado

**Arquivo:** `elevatoria/integracao.py`.

**Relato.** "O volume do dia calculado pelo trapézio ficou vários por cento abaixo do que
marcou o totalizador do medidor. Em dias sem falhas de comunicação, as contas batem. Os testes
de aceitação passam, por isso ninguém tinha notado."

**Critério de aceitação.**

1. **Antes** de corrigir, escreva em `testes/test_dia.py` pelo menos dois testes de regressão
   que falhem com o código atual. Confirme que eles falham.
2. Corrija o defeito mudando o mínimo possível. Os testes de aceitação continuam passando, os
   seus passam a passar, e a Etapa 2 do `marco4.py` roda.
3. Na correção, os seus testes serão rodados também contra o código original: pelo menos um
   deles precisa falhar.

## 4. O script `marco4.py`

O script vem pronto: **não o altere**. Ele usa a `MATRICULA` do seu `marco1.py` e para no
primeiro `assert` que falhar.

- **Etapa 1, Convergência.** O erro do trapézio e do Simpson quando o número de subintervalos
  dobra: (a) numa função suave; (b) no custo do dia, que tem a tarifa descontínua, integrado
  de uma vez e por faixas. Usa só código pronto.
- **Etapa 2, Volume do dia (#11).** O volume a partir do registro com falhas, comparado com o
  valor de conferência.
- **Etapa 3, Curvas e custo (#10).** O ajuste das curvas da bomba e o balanço do dia: volume,
  energia e custo de cada faixa.

## 5. Testes

Rode tudo com `python -m unittest discover -v`. Os testes de aceitação dos quatro marcos
devem passar, assim como os seus testes dos marcos anteriores.

Em `testes/test_dia.py`, escreva **pelo menos 4 testes**, sem contar o exemplo, com uma
docstring de uma linha em cada um:

- pelo menos 2 testes de regressão da issue #11, escritos antes da correção;
- pelo menos 2 testes de `ajustar_polinomio` ou de `dia_de_operacao` que os testes de
  aceitação não cobrem. Releia as docstrings: há regras do contrato que eles não verificam.

## 6. Relatório: seção "Marco 4" do `RELATORIO.md`

Copie o modelo abaixo para o fim do seu `RELATORIO.md` e responda com as suas palavras e com
os números da sua execução, em até 6 linhas por pergunta.

```markdown
## Marco 4

### R13 — Integração e descontinuidade

<!-- Na Etapa 1(b), integrando o custo do dia de uma vez, a ordem observada cai para cerca
de 1, no trapézio e no Simpson; integrando cada faixa separadamente, voltam as ordens 2 e 4.
Por quê? -->

### R14 — Issue #11

<!-- Os nomes dos seus testes de regressão; a causa do defeito; por que os testes de
aceitação não o pegaram; por que a regra de Simpson não serve para o registro do dia. -->
```

## 7. Entrega

**Descrição do Pull Request.** Acrescente à descrição do seu PR, abaixo da seção do Marco 3:

```markdown
## Marco 4
Resolve as issues #10 e #11 do enunciado.

### O que mudou
- ...

### Como testei
- `python -m unittest discover -v`: N testes, todos passando
- `python marco4.py`: todos os assert passam

### Pontos de atenção para o revisor
- ... (por exemplo, o método de mínimos quadrados que você escolheu e por quê)
```

**Checklist do Marco 4**

- [ ] `git fetch upstream` seguido de
      `git diff upstream/main --stat -- fornecido/ marco2.py marco3.py marco4.py` não mostra
      nada (você não alterou o código fornecido nem os scripts).
- [ ] `python -m unittest discover -v` roda sem falhas, com pelo menos 4 testes seus do Marco 4.
- [ ] `python marco4.py` roda sem exceções.
- [ ] O código novo tem docstrings e anotações de tipo, e `elevatoria/` não tem `print`.
- [ ] Os testes de regressão da #11 falhavam antes da correção.
- [ ] O `RELATORIO.md` tem a seção "Marco 4", com as respostas R13 e R14.
- [ ] Todo o código foi executado, testado e lido por você, inclusive o gerado com ajuda de IA.

## 8. Material complementar (opcional)

- https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.polyfit.html
- https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
- https://docs.scipy.org/doc/scipy/reference/integrate.html
- https://en.wikipedia.org/wiki/Linear_least_squares
- https://en.wikipedia.org/wiki/Simpson%27s_rule

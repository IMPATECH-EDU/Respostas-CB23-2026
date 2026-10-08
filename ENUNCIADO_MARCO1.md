# Projeto Elevatória — Marco 1: Dados (após a Aula 8, 05/10)

O fluxo de trabalho (branch, Pull Request) e as regras da casa estão no `README.md` deste
repositório; as regras gerais do projeto (uso de IA, antiplágio e prazo final de 23/11/2026),
no documento principal da disciplina. Este arquivo descreve só o Marco 1. Data sugerida para
concluí-lo: **19/10**.

## A situação

Você acaba de entrar na equipe que mantém o software de supervisão de uma estação elevatória
de água. Você não começa do zero: a base de código já existe. Parte dela foi escrita por
colegas que passaram pelo projeto antes de você, parte é mantida por outra equipe e não pode
ser alterada, e há cinco *issues* abertas esperando alguém para resolvê-las. O seu trabalho
chega à base por um Pull Request, que passa por testes automáticos e pela revisão de um
colega (o professor e os monitores).

É assim que a maior parte do trabalho de programação acontece fora da universidade: ler
código escrito por outras pessoas, respeitar as convenções da casa, mexer só no que é preciso,
provar com testes que a mudança funciona e explicar a mudança para quem vai revisá-la.

A estação é só o cenário. Nenhum conhecimento de engenharia é necessário: o que importa são
as expressões regulares, as funções lambda e as compreensões, o NumPy e a organização do
código.

**Neste marco você vai:**

- trabalhar em uma base de código existente, respeitando a separação entre o seu código e o
  de outra equipe;
- implementar um leitor de log com expressões regulares (grupos nomeados, `fullmatch`,
  `findall`, `sub`);
- usar lambdas e compreensões de lista, de dicionário e de conjunto, e reconhecer a armadilha
  do *late binding*;
- medir o custo em memória e em tempo de `list`, `array.array` e `numpy.ndarray`;
- diagnosticar e corrigir um defeito em código alheio, com um teste de regressão;
- acrescentar um método a uma classe existente (uma subclasse de `numpy.ndarray`) seguindo as
  convenções dela.

## 1. Preparação

### 1.1 Ambiente (Linux)

Crie um ambiente virtual com `venv`, fora do repositório, e instale o NumPy. O Python deve
ser 3.9 ou superior.

```bash
python3 --version
python3 -m venv ~/venvs/prog2-venv
source ~/venvs/prog2-venv/bin/activate    # o prompt passa a mostrar (prog2-venv)
which python                              # deve apontar para ~/venvs/prog2-venv/bin/python
python -m pip install --upgrade pip
python -m pip install numpy
```

Em cada terminal novo é preciso **ativar o ambiente de novo** (`source ...`). Se `which
python` não apontar para o ambiente, ele não está ativo. Quem preferir pode usar `conda`
(`conda create -n prog2-conda python numpy` e `conda activate prog2-conda`); nesse caso,
indique no `RELATORIO.md`.

### 1.2 Fork e branch

Você não tem permissão para escrever no repositório da disciplina: trabalhe em um fork. No
GitHub, abra https://github.com/IMPATECH-EDU/Respostas-CB23-2026 e clique em **Fork**. Depois:

```bash
git clone https://github.com/<seu_usuario>/Respostas-CB23-2026.git
cd Respostas-CB23-2026
git remote add upstream https://github.com/IMPATECH-EDU/Respostas-CB23-2026.git
git switch -c projeto_<sua_matricula>
```

Todo o seu trabalho acontece nessa branch, nos arquivos da própria base de código. Nunca faça
commit na `main`.

### 1.3 Primeira execução

A partir da raiz do repositório, com o ambiente ativado:

```bash
python fornecido/simulador.py          # deve terminar com "simulador.py OK"
python -m unittest discover -v         # roda os testes de aceitação e os seus
```

A maior parte dos testes de aceitação deve **falhar** com `NotImplementedError`: é o código
que você ainda vai escrever. Depois do seu primeiro commit, envie a branch para o seu fork
(`git push -u origin projeto_<sua_matricula>`) e abra o Pull Request como rascunho (*Draft*),
com o título `projeto_<sua_matricula>`: base `IMPATECH-EDU/Respostas-CB23-2026`, branch
`main`; head `<seu_usuario>/Respostas-CB23-2026`, branch `projeto_<sua_matricula>`.

## 2. A base de código

```
Respostas-CB23-2026/
├── README.md                # fluxo de trabalho e regras da casa: leia antes de começar
├── ENUNCIADO_MARCO1.md      # este arquivo
├── RELATORIO.md             # o seu relatório (modelo com as perguntas do Marco 1)
├── marco1.py                # script de demonstração (esqueleto com os assert)
├── fornecido/               # código de outra equipe: NÃO ALTERE
│   ├── simulador.py         #   gera o log da estação a partir da sua matrícula
│   ├── cronometro.py        #   mede o tempo de funções
│   └── testes_aceitacao/    #   testes de aceitação de cada marco
├── elevatoria/              # código da aplicação
│   ├── dados.py             #   esqueleto: assinaturas e docstrings (issues #1 a #3)
│   └── serie.py             #   classe SerieTemporal, escrita por um colega (issues #4 e #5)
└── testes/
    └── test_dados.py        # os seus testes (há um exemplo de formato)
```

| O quê | De quem é | O que você pode fazer |
| --- | --- | --- |
| `fornecido/` | Outra equipe (a disciplina) | Nada. Qualquer mudança aparece no diff do seu PR e é conferida na correção. Se achar um problema, avise o professor. |
| `elevatoria/dados.py` | Sua equipe | Implementar as funções marcadas com `NotImplementedError`, sem mudar nomes nem assinaturas públicas. Funções auxiliares privadas (`_nome`) são permitidas. |
| `elevatoria/serie.py` | Um colega | Só o necessário para as issues #4 e #5. |
| `testes/`, `marco1.py`, `RELATORIO.md` | Você | Tudo, sem remover nem enfraquecer os `assert` do `marco1.py`. |

As docstrings de `dados.py` e de `serie.py` são o contrato de cada função: leia-as com
atenção, porque os testes de aceitação foram escritos a partir delas.

## 3. O log do SCADA

A função `gerar_log(matricula)`, de `fornecido/simulador.py`, devolve `(texto, verdade)`: uma
hora de log (05/10/2026, das 08:00 às 09:00, uma leitura de cada instrumento a cada 6 s) e um
dicionário com os valores de conferência usados nos `assert`. Cada linha tem o formato
`DATA HORA NIVEL TAG chave=valor [chave=valor ...]`:

```
2026-10-05 08:00:00 INFO B1 evento=partida corrente=47.5
2026-10-05 08:00:00 INFO PT101 contagens=131
2026-10-05 08:00:00 INFO PT102 contagens=1790
2026-10-05 08:00:00 INFO FT201 pulsos=3873
2026-10-05 08:00:00 INFO LT301 nivel=46.99
2026-10-05 08:08:24 ALARME PT102 evento=pressao_alta limite=2000
```

| Tag | O que é | Valor registrado |
| --- | --- | --- |
| `PT101`, `PT102` | Transmissores de pressão (sucção e recalque) | `contagens` de um conversor A/D de 12 bits (0 a 4095) |
| `FT201` | Medidor de vazão | `pulsos` nos últimos 6 s (cada pulso é 0,1 L) |
| `LT301` | Nível do reservatório | `nivel`, em % |
| `B1` | Bomba | eventos (`evento=partida`, `evento=vibracao`) |

O log também contém **linhas corrompidas** (falhas de comunicação e linhas truncadas), que
devem ser descartadas, mas contadas. O dicionário `verdade` traz `linhas`, `invalidas`,
`por_nivel`, `registros_por_tag`, `espurios` (índices das 5 leituras espúrias de `PT102`),
`pulsos_total` e valores de referência que serão usados nos próximos marcos.

## 4. Issues abertas

### #1 — Leitor do log SCADA

**Arquivo:** `elevatoria/dados.py` (`LINHA`, `valida_tag`, `ler_log`, `contagem_por_tag`,
`serie`).

**Descrição.** A base ainda não sabe ler o log. As docstrings trazem o contrato completo; em
resumo:

- `LINHA` é um padrão compilado com `re.VERBOSE`, com um comentário em cada parte e os grupos
  nomeados `data`, `hora`, `nivel`, `tag` e `resto`. A linha inteira deve casar com o padrão,
  que é aplicado com `fullmatch`.
- `valida_tag(s)` diz se a string **inteira** é uma tag válida.
- `ler_log(texto)` devolve `(registros, invalidas)`. Cada `Registro` (já definido no módulo)
  tem `instante` (`datetime`), `nivel`, `tag` e `valores`, um dicionário em que os números
  viram `float` e o resto continua `str`. A docstring define o que conta como linha inválida.
- `contagem_por_tag` usa uma compreensão de dicionário sobre um conjunto obtido por
  compreensão de conjunto.
- `serie(registros, tag, chave)` monta uma `SerieTemporal` com os valores de `chave`.

**Critério de aceitação.** Os testes de aceitação de `LINHA`, `valida_tag`, `ler_log`,
`contagem_por_tag` e `serie` passam, e a Etapa 1 do `marco1.py` roda.

### #2 — Conversores de unidade por tag

**Arquivo:** `elevatoria/dados.py` (`criar_conversores`).

**Descrição.** Na versão anterior deste módulo, alguém montou os conversores de unidade com
uma compreensão de lambdas, e todos os instrumentos passaram a ser convertidos com o fator do
`FT201`. A função foi removida da base. Reescreva-a: dado `{tag: fator}`, ela devolve
`{tag: função}`, em que cada função (uma lambda) multiplica a contagem pelo fator **da sua
própria tag**.

**Critério de aceitação.** O teste de aceitação de `criar_conversores` passa, e a Etapa 2(e)
do `marco1.py` mostra a versão errada e a sua lado a lado.

### #3 — Comparativo de memória e tempo

**Arquivo:** `elevatoria/dados.py` (`medir_memoria`, `converter_laco`,
`converter_compreensao`, `converter_map`, `converter_vetorizado`, `medir_tempos`).

**Descrição.** A equipe quer decidir como guardar as contagens. `medir_memoria` mede o espaço
ocupado por um milhão de contagens em uma `list`, em um `array.array('H')` e em `ndarray`s de
vários `dtype`. A docstring define exatamente o que contar em cada caso; para o `ndarray`, use
o atributo `.nbytes`. As quatro funções `converter_*` fazem a mesma conversão
(`c * 600 / 4095`) de quatro formas, e `medir_tempos` mede cada uma com `cronometrar`, de
`fornecido/cronometro.py`.

**Critério de aceitação.** Os testes de aceitação de memória e tempo passam, e a Etapa 3 do
`marco1.py` roda.

### #4 — BUG: `media_movel` devolve um valor a menos

**Arquivo:** `elevatoria/serie.py`.

**Relato.** "Calculei a média móvel de 30 pontos da série de pressão `PT102` (600 leituras) e
recebi 570 valores. Pela docstring, deveriam ser 571. Os testes de aceitação passam, por isso
ninguém tinha notado."

**Critério de aceitação.**

1. **Antes** de corrigir, escreva em `testes/test_dados.py` pelo menos um teste de regressão
   que falhe com o código atual. Confirme que ele falha.
2. Corrija o defeito sem laços, sem modificar `self` e mantendo o tipo de retorno
   (`SerieTemporal`). Os testes de aceitação continuam passando, e o seu teste passa a passar.
3. Na correção, os seus testes serão rodados também contra o código original: pelo menos um
   deles precisa falhar.
4. Responda a pergunta R7 do relatório.

### #5 — Médias por bloco

**Arquivo:** `elevatoria/serie.py` (`SerieTemporal.reamostrar`).

**Descrição.** A operação quer a pressão média por minuto. As leituras chegam a cada 6 s,
então cada minuto tem 10 leituras. Implemente `reamostrar(k)`, que devolve as médias de
blocos consecutivos de `k` pontos. A docstring traz o contrato, inclusive o que fazer com os
pontos que sobram no fim. Siga as convenções da classe: só operações do NumPy, sem laços, e
sem modificar `self`.

**Critério de aceitação.** Os testes de aceitação de `reamostrar` passam, os seus testes
cobrem a sobra no fim, e a Etapa 4(c) do `marco1.py` roda.

## 5. O script `marco1.py`

O esqueleto já traz a estrutura, os imports e todos os `assert`. Troque `MATRICULA` pelo seu
número, complete os trechos marcados com `_todo(...)` e acrescente as impressões pedidas nos
comentários. O script usa apenas a interface pública dos módulos.

- **Etapa 0, Ambiente.** Versões e verificação rápida do NumPy (já pronta).
- **Etapa 1, Leitura do log (#1).** (a) registros e linhas inválidas; (b) registros por nível,
  com uma compreensão de dicionário; (c) total de pulsos e volume bombeado; (d) `valida_tag`.
- **Etapa 2, Lambda e compreensões (#2).** (a) ordenações com `sorted` e `key=lambda`;
  (b) as contagens de `PT102` com `map`/`filter` e com compreensão; (c) contagens acima de 2000
  e tags distintas; (d) `re.sub` com uma lambda como `repl`; (e) *late binding*; (f) a pressão
  de recalque pela escala nominal, comparada com o valor de conferência.
- **Etapa 3, Memória e tempo (#3).** (a) tabela de memória; (b) tabela de tempos;
  (c) `dtype` de uma lista mista e *overflow* em `uint16`.
- **Etapa 4, A série de pressão (#4 e #5).** (a) estatísticas; (b) média móvel; (c) médias
  por minuto; (d) tipos de cinco expressões com a `SerieTemporal`.

**Previsões antes de medir.** Antes de implementar as Etapas 3 e 4, preencha no `RELATORIO.md` as
colunas de previsão das tabelas R5 e R6 e faça um commit só com elas. O histórico de
commits mostra a ordem. Previsões
erradas não perdem pontos; o que se avalia é a explicação da diferença.

## 6. Testes

- **Testes de aceitação** (`fornecido/testes_aceitacao/`): todos devem passar. Você não pode
  alterá-los.
- **Os seus testes** (`testes/test_dados.py`): pelo menos 8, sem contar o exemplo, com
  `unittest` e uma docstring de uma linha em cada teste dizendo qual caso ele cobre. Entre
  eles, obrigatoriamente:
  - pelo menos 2 testes de regressão da issue #4, escritos antes da correção;
  - pelo menos 2 testes de `reamostrar`, incluindo a sobra no fim;
  - pelo menos 2 testes de regras do contrato de `ler_log` que os testes de aceitação não
    verificam.

Compare números de ponto flutuante com `assertAlmostEqual` ou `np.allclose`, nunca com `==`.
Para rodar tudo: `python -m unittest discover -v`.

## 7. Relatório: seção "Marco 1" do `RELATORIO.md`

O `RELATORIO.md` já traz o modelo. Responda com as suas palavras e com os números da sua
execução, em até 6 linhas por pergunta, além das tabelas.

- **Ambiente.** Cole a saída de `which python` e da Etapa 0 do `python marco1.py`.
- **R1, Expressões regulares.** Dê uma string que `re.match` aceita e `re.fullmatch` rejeita
  com o padrão de tag, e diga o que aconteceria em `valida_tag` se você usasse `match`.
- **R2, Linhas inválidas.** Por que `ler_log` devolve as linhas descartadas, em vez de
  simplesmente ignorá-las? Descreva uma situação na operação da estação em que descartar em
  silêncio esconderia um problema real.
- **R3, Late binding.** Por que `errados["PT102"](4095)` dá 409,5? Por que a sua
  `criar_conversores` não tem o problema?
- **R4, Escala nominal.** Na Etapa 2(f), a escala nominal dá cerca de 262 kPa, e o valor de
  conferência é 380 kPa. Proponha uma hipótese para a diferença e diga onde, no código da base,
  está a explicação. (Ler o código de outras equipes faz parte do trabalho.)
- **R5, Previsão × medição.** Preencha a tabela (a previsão vem do commit de previsões) e
  explique a maior diferença. Explique por que `uint16` vezes 20 dá 16364 e diga que `dtype`
  você escolheria para guardar contagens e para guardar pressões em kPa.
- **R6, Tipos da `SerieTemporal`.** Preencha a tabela e explique o resultado que mais
  surpreendeu você.
- **R7, Issue #4.** Descreva o sintoma, o seu teste de regressão (nome), a causa (em termos
  da soma acumulada) e a correção. Explique por que os testes de aceitação não pegaram o
  defeito e aponte mais um caso que eles não cobrem e qual teste seu o cobre.

## 8. Entrega

**Commits.** Faça commits pequenos, uma ideia por commit. Uma sequência possível:
previsões, #1, #2, #3, teste de regressão da #4, correção da #4, #5, relatório. Fazer o teste
de regressão e a correção em commits separados é o que se espera numa equipe real.

**Descrição do Pull Request.** Mantenha a descrição atualizada a cada marco, neste formato:

```markdown
## Marco 1
Resolve as issues #1 a #5 do enunciado.

### O que mudou
- ...

### Como testei
- `python -m unittest discover -v`: N testes, todos passando
- `python marco1.py`: todos os assert passam

### Pontos de atenção para o revisor
- ...
```

**Checklist do Marco 1**

- [ ] `git fetch upstream` seguido de `git diff upstream/main --stat -- fornecido/` não mostra
      nada (nenhum arquivo de `fornecido/` foi alterado).
- [ ] `python -m unittest discover -v` roda sem falhas, com todos os testes de aceitação e
      pelo menos 8 testes seus.
- [ ] `python marco1.py` roda sem exceções, com a sua matrícula, e todos os `assert` passam.
- [ ] Os módulos de `elevatoria/` não têm `print`, e todo o código novo tem docstring e
      anotações de tipo (veja as regras da casa no `README.md`).
- [ ] O commit de previsões vem antes do código das Etapas 3 e 4, e o teste de regressão da
      #4 falhava antes da correção.
- [ ] O `RELATORIO.md` tem a seção "Marco 1", com o ambiente e as respostas R1 a R7.
- [ ] Todo o código foi executado, testado e lido por você, inclusive o gerado com ajuda de IA.

**Originalidade.** Os nomes e as assinaturas públicas são definidos pela base, e todo o
código que está na `main` fica fora da comparação do antiplágio. A comparação recai sobre o
que o seu PR muda: as implementações, os testes e o relatório.

## 9. Material complementar (opcional)

- https://docs.python.org/3/howto/regex.html
- https://docs.python.org/3/library/re.html
- https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
- https://docs.python.org/3/library/dataclasses.html
- https://docs.python.org/3/library/unittest.html
- https://numpy.org/doc/stable/user/quickstart.html
- https://numpy.org/doc/stable/user/basics.subclassing.html

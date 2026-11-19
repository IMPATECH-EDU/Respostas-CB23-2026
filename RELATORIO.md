# Relatório — <seu nome> (3507)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
$ which python
/home/fred/venvs/prog2-venv/bin/python
$ python marco1.py
=== Etapa 0: ambiente ===
Python 3.14.6 | NumPy 2.5.4 | fornecido 4.0
```

### R1 — Expressões regulares

Com o padrão `[A-Z]{1,2}\d{1,3}`, `re.match` aceita `"PT1010"` (e também `"PT101 "`), porque
basta o começo da string casar (`"PT101"`); `re.fullmatch` rejeita, porque exige que a string
inteira case. Se `valida_tag` usasse `match`, ela diria que `"PT1010"` e `"PT101 "` são tags
válidas, e um log com lixo depois da tag passaria pela validação.

### R2 — Linhas inválidas

Descartar não é o mesmo que esquecer: quem chama `ler_log` precisa saber quantas linhas se
perderam e quais eram, para decidir se o log é confiável. No meu log foram 4 linhas (2 falhas
de comunicação com a RTU e 2 linhas truncadas). Se a RTU começasse a falhar com frequência, ou
se um alarme de pressão alta chegasse truncado, descartar em silêncio esconderia a falha de
comunicação e o próprio alarme, e o operador nem saberia que perdeu dados.

### R3 — Late binding

A lambda `lambda c: c * k` não guarda o valor de `k`, só o nome: `k` é procurado quando a
função é chamada, e aí a compreensão já terminou com `k = 0.1` (o fator de `FT201`, o último do
dicionário). Logo `errados["PT102"](4095) = 4095 · 0,1 = 409,5`. Na minha `criar_conversores`,
cada lambda recebe `k=fator` como argumento padrão, que é avaliado quando a lambda é criada:
cada função guarda o fator da sua própria tag.

### R4 — Escala nominal

A escala nominal supõe que a pressão é linear nas contagens (`c · 600 / 4095`), o que dá
262,0 kPa para a média de PT102 (≈ 1788 contagens), contra 380 kPa de conferência. Hipótese: a
resposta do transmissor não é linear. A explicação está em `fornecido/simulador.py`, na função
`p_real`: `p = 600 · sen(π/2 · c / 4095)`. Para c ≈ 1788, o seno dá ≈ 380 kPa; a reta só
coincide com essa curva nas pontas (0 e 4095), e no meio subestima a pressão.

### R5 — Previsão × medição (Etapa 3)

Previsões: _(preencher)_

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | _(preencher)_ | 18 (36 000 056 B / 2 000 000 B) |
| Tempo do laço / tempo vetorizado | _(preencher)_ | ≈ 31 (80,3 ms / 2,6 ms) |
| Tempo da compreensão / tempo do laço | _(preencher)_ | ≈ 0,91 (72,9 ms / 80,3 ms) |

_(explicar aqui a maior diferença entre a sua previsão e a medição)_. A lista guarda 8 bytes
de ponteiro por elemento mais um objeto `int` de 28 bytes para cada número (36 B/elemento),
contra 2 B do `uint16`. `uint16` vai só até 65 535 e a conta é feita no próprio `dtype`:
4095 · 20 = 81 900 estoura e dá 81 900 − 65 536 = 16 364 (aritmética módulo 2¹⁶), sem aviso.
Para contagens (0 a 4095) eu usaria `uint16`; para kPa, `float64` (ou `float32`, se memória
pesar), porque a pressão é fracionária e entra em contas que precisam de precisão.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | _(preencher)_ | `SerieTemporal` |
| `s[1:]` | _(preencher)_ | `SerieTemporal` |
| `s * 2` | _(preencher)_ | `SerieTemporal` |
| `s.sum()` | _(preencher)_ | `SerieTemporal` |
| `s[0]` | _(preencher)_ | `float64` |

O mais surpreendente é `s.sum()` ser uma `SerieTemporal` (um array de dimensão 0), e não um
número: as reduções do NumPy chamam `__array_wrap__` e preservam a subclasse. Já `s[0]`, um
índice inteiro, devolve um escalar `np.float64`. Por isso a `SerieTemporal.amplitude` faz
`float(...)`: sem isso, devolveria uma `SerieTemporal` em vez de um `float`.

### R7 — Issue #4

Sintoma: `media_movel(30)` de 600 pontos devolvia 570 valores, e não 571. Testes de regressão:
`test_tamanho_serie_de_600_janela_30`, `test_primeira_media_usa_os_primeiros_pontos`,
`test_janela_igual_ao_tamanho` e `test_janela_1_devolve_a_propria_serie`. Causa: com
`S = cumsum(x)`, `S[i]` é a soma de `x[0..i]`; `S[j:] - S[:-j]` dá as somas das janelas que
começam em 1, 2, …, e a primeira janela (`x[0:j]`, cuja soma é o próprio `S[j-1]`) se perde.
Correção: pôr um 0 na frente de `S`, de modo que `S[i]` seja a soma de `x[:i]`. Os testes de
aceitação só olham o tipo e os erros, nunca o tamanho nem os valores. Eles também não cobrem
`janela == len(self)` (o código antigo devolvia uma série vazia): coberto por
`test_janela_igual_ao_tamanho`.

## Marco 2

### Ambiente

```
=== Etapa 0: ambiente ===
Python 3.14.6 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3507
```

### R8 — Derivada numérica

De h = 1 até h = 1e-5 o erro cai 10 vezes a cada passo (1,7e-5 → 6,2e-10): domina o erro de
truncamento da diferença adiante, que é proporcional a h. Abaixo disso, o erro volta a crescer
(1e-8: 6,2e-8; 1e-12: 1,4e-2): domina o arredondamento, porque `f(x+h) − f(x)` subtrai dois
números quase iguais, perdendo dígitos (≈ ε·|f|/h). Em h = 1e-14, `1000 + 1e-14 == 1000` é
verdadeiro (1e-14 é menor que meio ulp de 1000, ≈ 1,1e-13), então `f(x+h) − f(x) = 0`, a
aproximação dá 0, e o erro é a própria derivada (0,2134).

### R9 — Issue #7

Testes de regressão: `test_milhao_de_pulsos_de_0_1`, `test_parcelas_pequenas_nao_somem` e
`test_kahan_bem_melhor_que_ingenuo`. Causa: `t` é exatamente o resultado arredondado de
`s + y`; calcular `s + y` de novo produz o mesmo número arredondado, então `t − (s + y)` é
sempre 0 e a correção nunca guarda nada. A forma `(t − s) − y` primeiro recupera a parte de
`y` que de fato entrou na soma (`t − s` é exato) e depois subtrai `y`, sobrando o que se perdeu.
Os testes de aceitação somam só 10 parcelas de 0,1 com `isclose`: o erro do ingênuo é pequeno
demais para a tolerância, então o Kahan quebrado passava.

### R10 — Precisão × exatidão

Precisão é a dispersão das leituras; exatidão, a proximidade do valor verdadeiro. Para PT102,
os desvios são 0,548 kPa (linear) e 0,549 kPa (spline): a mesma precisão, porque o ruído é o do
transmissor. Mas o viés é −1,826 kPa na linear e 0,004 kPa na spline: a linear é menos exata.
A média de ≈ 595 leituras reduz o erro aleatório (o erro padrão cai com 1/√n), mas o viés da
linear é sistemático (a corda entre os pontos da tabela fica abaixo do seno em toda leitura),
e erro igual em todas as leituras não se cancela na média.

## Marco 3

### R11 — Bissecção × Newton

A bissecção divide o intervalo ao meio a cada iteração, sem olhar para `g`: o número de
iterações só depende de `(b − a)/tol`, aqui `log2(13 / 1e-12) ≈ 43,6`, ou seja, 44, para
qualquer Reynolds. Ordem 2 quer dizer `e_{k+1} ≈ C·e_k²`: o número de dígitos corretos dobra.
Com Re = 1e4 os erros do Newton foram 2,9 → 5,0e-2 → 2,3e-5 → 5,0e-12 (expoentes −2, −5, −12),
e a ordem estimada foi 2,00. O Newton falha, por exemplo, quando a derivada se anula ou o chute
inicial está longe (em `x³ − 2x + 2` a partir de 0 ele oscila entre 0 e 1); a bissecção, com
troca de sinal em `[a, b]`, sempre converge.

### R12 — Issue #9

Testes de regressão: `test_colebrook_re_1e4_em_poucas_iteracoes`,
`test_raiz_de_2_com_derivada_exata` e `test_erro_cai_quadraticamente`. Com a derivada fixa
`d = f'(x0)`, a iteração `x − f(x)/d` é o método da corda: perto da raiz,
`e_{k+1} ≈ (1 − f'(r)/d)·e_k`, um fator constante, ou seja, convergência linear. A ordem 2 só
aparece quando `d = f'(x_k)` acompanha o ponto atual, cancelando o termo de primeira ordem. Os
testes de aceitação só conferem se a raiz está certa, nunca o número de iterações.

## Marco 4

### R13 — Integração e descontinuidade

As estimativas de erro do trapézio (∝ h²·f″) e de Simpson (∝ h⁴·f⁽⁴⁾) supõem um integrando
suave em todo o intervalo. O custo tem saltos em 18 h e 21 h (a tarifa triplica): no
subintervalo que contém o salto, a regra aproxima uma função descontínua por um polinômio e erra
algo proporcional a h (a largura do subintervalo vezes o salto). Esse erro de ordem 1 domina, e a
ordem observada cai para ≈ 1 (1,00 no trapézio e 0,65 no Simpson). Por faixas, cada integral é de
uma função suave, e voltam as ordens 2,00 e 4,00.

### R14 — Issue #11

Testes de regressão: `test_reta_em_malha_irregular`,
`test_constante_da_o_comprimento_do_intervalo` e `test_reta_na_malha_do_registro_com_falhas`.
Causa: `integrar_tabela` usava `h = x[1] − x[0]` para todos os trapézios; com 8 leituras perdidas,
os intervalos de 30 min eram contados como 15 min, e o volume saía abaixo do totalizador. Os
testes de aceitação só usam malhas uniformes, em que o código antigo acerta. Simpson composto
exige pontos igualmente espaçados e um número par de subintervalos, e o registro (89 pontos, com
passos de 15 e 30 min) não satisfaz isso: ele recusa (Etapa 2 do `marco4.py`).

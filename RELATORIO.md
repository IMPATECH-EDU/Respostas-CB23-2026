# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
$ which python
<cole aqui a saída de `which python` no seu ambiente>

=== Etapa 0: ambiente ===
Python 3.13.18 | NumPy 2.5.3 | fornecido 4.0
```

### R1 — Expressões regulares

Com o padrão `[A-Z]{1,2}\d{1,3}`, `re.match` aceita `"PT1010"` (casa o prefixo `"PT101"` e
ignora o `0` que sobra), mas `re.fullmatch` rejeita, porque exige que a string inteira case.
O mesmo vale para `"PT101 "`. Se `valida_tag` usasse `match`, essas duas tags inválidas seriam
aceitas, e o teste de aceitação `test_invalidas` falharia.

### R2 — Linhas inválidas

Descartar sem avisar apaga a evidência de uma falha. `ler_log` devolve as linhas para que quem
chamou possa contá-las, registrá-las e alertar: na minha execução foram 4 de 2408 (0,17 %). Se
a comunicação com a RTU começar a cair com frequência, a série de `PT102` passa a ter buracos
justamente durante um alarme de pressão alta, e a média continuaria saindo "normal", sem
ninguém perceber que metade das leituras daquele minuto se perdeu.

### R3 — Late binding

A lambda `lambda c: c * k` não guarda o valor de `k`: guarda a variável `k` da compreensão, que
só é consultada quando a função é chamada. Nesse momento a compreensão já terminou e `k` vale o
último fator do dicionário, 0,1 (o do `FT201`); daí 4095 · 0,1 = 409,5. Em `criar_conversores`
eu uso um argumento padrão (`lambda c, fator=fator: c * fator`): o valor padrão é avaliado
quando cada lambda é criada, então cada uma fica com o fator da sua própria tag.

### R4 — Escala nominal

Hipótese: o transmissor não é linear, e a escala nominal (600 kPa em 4095 contagens, uma reta)
subestima a pressão no meio da faixa. A explicação está em `fornecido/simulador.py`, na função
`p_real`: a resposta verdadeira é `600·sin(π/2 · c/4095)`, uma curva côncava. Com a média de
≈1791 contagens, a reta dá 262,0 kPa e a senoide dá 380 kPa. Por isso o Marco 2 usa a tabela
de calibração (`tabela_calibracao`) em vez da escala nominal.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d604fd0

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18× (8 B de ponteiro + 28 B de `int` por elemento, contra 2 B) | 18,0× (36 000 056 B / 2 000 000 B) |
| Tempo do laço / tempo vetorizado | ≈ 50× | 52,8× (56,97 ms / 1,08 ms) |
| Tempo da compreensão / tempo do laço | ≈ 0,7 (a compreensão evita o `append`) | 0,96 (54,41 ms / 56,97 ms) |

A maior diferença foi a compreensão: previ 30 % de ganho e foi só 4 %. No Python 3.13 o
`append` dentro do laço é barato (o interpretador especializa a chamada), e o tempo é dominado
pela conta `c * 600 / 4095` em cada elemento, que as duas versões fazem igual. `uint16` só
guarda de 0 a 65535; 4095 · 20 = 81900 não cabe e "dá a volta": 81900 − 65536 = 16364, sem
erro nem aviso. Para contagens eu usaria `uint16` (0–4095 cabe e ocupa 2 B), convertendo para
float antes de multiplicar; para kPa, `float64`, porque médias e desvios precisam da precisão.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

O que surpreendeu foi `s.sum()`. A soma é uma redução de ufunc (`np.add.reduce`), e o NumPy
embrulha o resultado de volta na subclasse: o resultado é uma `SerieTemporal` de dimensão 0. Já
`s[0]` é indexação de um elemento, que devolve um escalar do NumPy (`float64`) e não passa pela
subclasse. Para usar a soma como número é preciso `float(s.sum())`, como faz `amplitude`.

### R7 — Issue #4

Sintoma: `media_movel(30)` em 600 pontos devolvia 570 valores, e não 571. Testes de regressão:
`TestMediaMovelRegressao.test_quantidade_de_valores` e `test_primeira_janela_presente`. Causa:
`acumulada[i]` é a soma de `x[0..i]`, então `acumulada[janela:] - acumulada[:-janela]` dá as
somas das janelas que começam em 1, 2, ...; a janela que começa em 0 (soma `acumulada[janela-1]`)
fica de fora. Correção: pôr um zero antes da soma acumulada. Os testes de aceitação só olhavam
o tipo e os erros de janela, nunca o tamanho nem os valores. Outro caso não coberto: janela igual
ao tamanho da série devolvia um vetor vazio; `test_janela_do_tamanho_da_serie` o cobre.

## Marco 2

### Ambiente

```
=== Etapa 0: ambiente ===
Python 3.13.18 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 123456
```

### R8 — Derivada numérica

De h = 1 até h = 1e-5 o erro cai 10× a cada década (1,66e-5 → 1,65e-9): domina o erro de
truncamento da diferença adiante, ≈ h·|f''|/2, proporcional a h. Abaixo disso domina o erro de
arredondamento, ≈ ε·|f|/h: f(x+h) e f(x) ficam quase iguais, a subtração cancela dígitos e
dividir por h amplifica o resto. O mínimo é h = 1e-5 (erro 6,2e-10). Em h = 1e-14,
`1000 + 1e-14 == 1000` é `True` (o espaçamento entre floats perto de 1000 é ≈1,1e-13), então
f(x+h) − f(x) = 0, a derivada estimada é 0 e o erro é a própria derivada, 0,2134.

### R9 — Issue #7

Testes de regressão: `TestKahanRegressao.test_dez_decimos_dao_exatamente_um`,
`test_parcelas_menores_que_o_ulp_nao_se_perdem` e `test_erro_muito_menor_que_o_ingenuo`. Causa:
`t = soma + y` já é o valor arredondado; recalcular `soma + y` arredonda de novo para o mesmo
float, então `t - (soma + y)` é sempre 0 e nunca há correção. Na forma `(t - soma) - y`, a
subtração `t - soma` é exata e recupera a parte de `y` que de fato entrou; menos `y`, sobra
(com sinal trocado) o que se perdeu. Os testes de aceitação somavam só 10 × 0,1 e comparavam
com `math.isclose`, que tolera o erro de 1e-16 da soma ingênua.

### R10 — Precisão × exatidão

Precisão é o espalhamento das leituras; exatidão é a distância da média ao valor verdadeiro. Em
PT102, linear e spline têm o mesmo desvio (0,528 e 0,529 kPa: o ruído do transmissor), mas o
viés é −1,830 kPa na linear e −0,000 na spline. A média de 595 leituras reduz o erro aleatório
(erro padrão ≈ 0,528/√595 ≈ 0,02 kPa), mas não o viés: a reta entre os pontos da tabela fica
abaixo da senoide, e todas as leituras saem convertidas com o mesmo erro sistemático, que não
se cancela na média.

## Marco 3

### R11 — Bissecção × Newton

A bissecção só usa o sinal de g: cada iteração divide o intervalo ao meio, e o número de passos
depende só de (b − a)/tol = 13/1e-12, ou seja, ⌈log2(1,3e13)⌉ = 44, para qualquer Reynolds.
Ordem 2 quer dizer e_{k+1} ≈ C·e_k²: em Re = 10⁴ os erros foram 5,0e-2 → 2,3e-5 → 5,0e-12, e o
número de dígitos corretos (1, 5, 11) praticamente dobra a cada passo (ordem estimada 2,00). O
Newton falha onde a bissecção não falha, por exemplo em `atan(x)` a partir de |x0| > 1,39: os
passos crescem e divergem, enquanto a bissecção em [−2, 3] sempre converge. Também, no ponto de
operação, um passo do Newton pode sair do domínio da curva da bomba.

### R12 — Issue #9

Testes de regressão: `TestNewtonRegressao.test_raiz_de_dois_em_poucas_iteracoes`,
`test_colebrook_re_1e4`, `test_derivada_avaliada_a_cada_iteracao` e
`test_erros_caem_quadraticamente`. Com f'(x0) fixa, o passo é o do método da corda:
e_{k+1} ≈ (1 − f'(r)/f'(x0))·e_k, um fator constante, ou seja, convergência linear. Só usando
f'(x_k) esse termo de 1ª ordem se anula e sobra o termo em e_k². Os testes de aceitação só
conferiam se convergia e se a raiz estava certa, nunca o número de iterações nem a ordem.

## Marco 4

### R13 — Integração e descontinuidade

As ordens 2 e 4 vêm de estimativas de erro que exigem o integrando suave (f'' ou f⁽⁴⁾ limitada)
em cada subintervalo. O custo tem um salto da tarifa às 18 h e às 21 h, e com n = 30 a 110 os
nós quase nunca caem nesses instantes: o subintervalo que contém o salto erra O(h·salto), e
esse termo domina, então a ordem cai para ≈1 (trapézio 1,00; Simpson 0,65, irregular porque
depende de onde o salto cai). Integrando cada faixa, o integrando é a potência (suave) vezes
uma constante, e voltam as ordens 2,00 e 4,00 (erro em n = 110: 6,3e-4 e 8,1e-8).

### R14 — Issue #11

Testes de regressão: `TestTrapezioTabelaRegressao.test_reta_em_malha_irregular_e_exata`,
`test_constante_da_comprimento_total` e `test_registro_com_falhas_igual_ao_np_trapezoid`. Causa:
`integrar_tabela` usava o mesmo passo `h = x[1] - x[0]` (15 min) em todos os trapézios; onde
faltava uma leitura o intervalo era de 30 min e entrava com metade da largura. O volume saía
3544,8 m³ contra 3888,0 m³ (−8,8 %). Os testes de aceitação só usavam malhas uniformes. Simpson
não serve porque exige pontos igualmente espaçados e em número ímpar, e o registro tem passos
de 15 e 30 min.

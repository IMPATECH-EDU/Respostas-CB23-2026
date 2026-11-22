# Relatório — Lourenzo Francisco Balonekr dos Santos (3514)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```text
$ which python
/home/codespace/.python/current/bin/python
Usei o Python do próprio GitHub Codespaces, sem ambiente virtual separado.

$ python marco1.py
=== Etapa 0: ambiente ===
Python 3.14.2 | NumPy 2.5.5 | fornecido 4.0
```

### R1 — Expressões regulares

Com o padrão de tag `[A-Z]{1,2}[0-9]{1,3}`, a string `"PT1010"` passa no `re.match`, que só
olha o começo e já encontra `"PT101"`, mas falha no `re.fullmatch`, que exige casar a string
inteira. Se `valida_tag` usasse `match`, ela diria que `"PT1010"`, `"PT101 "` (com espaço no
fim) e até `"B1abc"` são tags válidas, porque todas começam com uma tag. O mesmo vale para o
`ler_log`: com `match`, uma linha com lixo no fim seria aceita.

### R2 — Linhas inválidas

As linhas descartadas mostram como está a comunicação com a planta, então não dá para jogar
fora sem registrar. No meu log foram 4 (duas `### falha de comunicacao com a RTU ###` e duas
truncadas, como `2026-10-05 08:20:4`). Se a RTU começasse a falhar com frequência, um leitor que
ignorasse essas linhas continuaria mostrando médias normais. Um pico de pressão que caísse numa
linha corrompida simplesmente sumiria. Devolvendo a lista, dá para contar as falhas e gerar um alarme.

### R3 — Late binding

Na compreensão `{tag: (lambda c: c * k) for ...}`, cada lambda guarda uma referência à variável
`k`, e não o valor que `k` tinha naquele momento. O valor só é lido quando a lambda é chamada,
e aí o laço já acabou: `k` ficou com o último fator, `0.1` do `FT201`. Por isso
`errados["PT102"](4095)` dá `4095 * 0.1 = 409.5`. Na minha `criar_conversores`, cada lambda nasce
dentro de uma chamada separada a `_multiplicador(fator)`. Cada chamada tem o próprio escopo, e
a lambda fica presa ao `fator` daquela chamada.

### R4 — Escala nominal

Na Etapa 2(f), a média das 595 contagens normais de PT102 foi 1788,0. Pela escala nominal,
isso dá 262,0 kPa, contra 380,0 kPa de conferência. Minha hipótese é que o transmissor não é
linear. A explicação está em `fornecido/simulador.py`, na função `p_real`: a resposta
verdadeira é `p = 600 * sin(π/2 * c / 4095)`. A escala linear só acerta nas pontas (0 e 4095).
Com o seno, 1788 contagens dão 380 kPa. A `tabela_calibracao()` do mesmo arquivo serve para
corrigir isso.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 8c58353

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18 (cada item da lista custa um ponteiro de 8 B mais um objeto `int` de ~28 B, contra 2 B no `uint16`) | 18,0 (36.000.056 B / 2.000.000 B) |
| Tempo do laço / tempo vetorizado | ≈ 50 (o NumPy faz a conta em C, sem criar um objeto Python por elemento) | ≈ 88 (93,19 ms / 1,06 ms) |
| Tempo da compreensão / tempo do laço | ≈ 0,7 (a compreensão evita a busca e a chamada de `append` a cada iteração) | ≈ 0,93 (86,95 ms / 93,19 ms) |

A memória bateu: 36 bytes por elemento na lista (8 do ponteiro e 28 do `int`) contra 2 no
`uint16`. A maior diferença foi no vetorizado: previ 50 e deu 88. Subestimei o custo do laço
em Python. Cada elemento leva cerca de 93 ns, porque o interpretador lê o `int`, faz duas
operações e cria um objeto `float` novo. No NumPy, o mesmo trabalho leva cerca de 1 ns por
elemento, num laço em C sem objetos. A compreensão também ganhou menos do que eu esperava
(0,93 em vez de 0,7), porque o `append` pesa pouco perto da aritmética. O `map` com lambda foi
o mais lento (116 ms), pois chama uma função Python por elemento.

`uint16` só guarda de 0 a 65535 e faz a conta módulo 2¹⁶, sem avisar. Como
`4095 * 20 = 81900 = 65536 + 16364`, sobra 16364. Eu guardaria as contagens em `uint16` (0 a 4095
cabe, com 2 bytes cada), mas convertendo para `float` antes de qualquer conta. As pressões em
kPa eu guardaria em `float64`: tem precisão de sobra e é o padrão do NumPy.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

O que mais me surpreendeu foi `s.sum()`. Eu esperava um número, mas veio uma `SerieTemporal`
de dimensão zero. Nas reduções, o NumPy devolve um array 0-d da mesma subclasse. Já `s[0]`, que
pega um único elemento, devolve um escalar `np.float64`. É por isso que `amplitude()` usa
`float(...)` para cumprir a promessa de devolver um `float`.

### R7 — Issue #4

**Sintoma:** a média móvel de 30 pontos da série PT102 (600 leituras) devolvia 570 valores,
e não 571 (`n - janela + 1`).
**Testes de regressão:** a classe `TestRegressaoMediaMovel`, com
`test_tamanho_n_menos_janela_mais_um`, `test_primeiro_valor_e_media_da_primeira_janela`,
`test_janela_igual_ao_tamanho_da_serie` e `test_janela_unitaria_devolve_a_propria_serie`.
Os quatro falharam antes da correção (commit 103f2db) e passaram depois dela (cf5fc3c).
**Causa:** com `C = cumsum(x)`, `C[i]` é a soma de `x[0]` até `x[i]`. Então
`C[i+j] - C[i]` soma `x[i+1]` até `x[i+j]`, e a janela que começa em 0 nunca é calculada.
Faltava a soma vazia no início.
**Correção:** pôr um 0 na frente antes do `cumsum`. Assim `S[i]` é a soma de `x[:i]`, e
`S[i+j] - S[i]` é exatamente a soma de `x[i:i+j]`, para i de 0 até n−j.
**Por que passou:** o teste de aceitação só confere o tipo do resultado e os `ValueError`, nunca
o tamanho nem os valores. **Outro caso não coberto:** `janela == len(s)`. O código antigo
devolvia um array vazio, sem erro nenhum. Esse caso é coberto por
`test_janela_igual_ao_tamanho_da_serie`.


## Marco 2

### Ambiente

```text
$ python marco2.py
=== Etapa 0: ambiente ===
Python 3.14.2 | NumPy 2.5.5 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3514
```

### R8 — Derivada numérica

De h = 1 até h = 1e-5, o erro cai 10 vezes a cada passo (de 1,658e-05 para 6,224e-10). Nessa
faixa domina o erro de truncamento da diferença adiante, que é proporcional a h (≈ h/2 · |f''|).
Depois de 1e-5, o erro volta a crescer (1,4e-05 em h = 1e-9 e 1,4e-02 em h = 1e-12): domina o
arredondamento. `f(x+h)` e `f(x)` ficam quase iguais, a subtração cancela os dígitos certos, e o
erro que sobra, de ordem ε·|f|, é dividido por um h cada vez menor. Em h = 1e-14,
`1000 + 1e-14 == 1000` dá `True`: o espaço entre floats perto de 1000 é ~1e-13. Então `x + h` é o
próprio `x`, o numerador dá 0, e o erro é a derivada inteira (0,2134 kPa/contagem).

### R9 — Issue #7

**Testes de regressão:** `test_dez_parcelas_de_um_decimo_dao_exatamente_um`,
`test_parcelas_pequenas_nao_somem` e `test_um_milhao_de_pulsos`, da classe `TestRegressaoKahan`.
Os três falhavam antes da correção.
**Causa:** `t` já é o valor arredondado de `soma + y`. Calcular `soma + y` de novo dá exatamente
o mesmo float, então `t - (soma + y)` é sempre 0, e o Kahan virava a soma ingênua. Na ordem
`(t - soma) - y`, a subtração `t - soma` é exata e mostra quanto de `y` entrou de fato na soma;
tirando `y`, sobra o pedaço perdido. Depois da correção, a Etapa 2 dá `100000.0`, com erro 0,
contra 1,333e-06 L do ingênuo.
**Por que os testes de aceitação não pegaram:** eles somam só 10 × 0,1 e comparam com
`math.isclose`, e 0.9999999999999999 é "próximo" de 1.0. Nenhum teste compara o Kahan com o
valor exato ou com o ingênuo.

### R10 — Precisão × exatidão

Para PT102, as duas curvas dão quase o mesmo desvio: 0,508 kPa na linear e 0,510 kPa na
spline. A precisão (a dispersão entre leituras) é a mesma, porque perto de 1788 contagens as
duas curvas têm praticamente a mesma inclinação. Já o viés é bem diferente: −1,831 kPa na
linear e −0,001 kPa na spline. Isso é exatidão, a distância até o valor verdadeiro. A linear
liga os pontos da tabela com retas, e como a resposta (um seno) é côncava, a reta fica sempre
abaixo. Com 595 leituras válidas, a média reduz o erro aleatório para cerca de
0,51/√595 ≈ 0,02 kPa. Mas o viés da curva é o mesmo em toda leitura, e nenhuma média o tira.
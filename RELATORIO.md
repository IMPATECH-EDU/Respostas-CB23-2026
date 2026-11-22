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
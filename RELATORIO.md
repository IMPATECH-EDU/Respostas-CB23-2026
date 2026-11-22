# Relatório — Manoel Felipe Macena de Azevedo (3524)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
<!-- COLE AQUI a saída de `which python` no SEU computador -->
=== Etapa 0: ambiente ===
<!-- COLE AQUI a linha "Python ... | NumPy ... | fornecido 4.0" da SUA execução -->
```

### R1 — Expressões regulares

Com o padrão `[A-Z]{1,2}\d{1,3}`, a string `"PT1010"` é aceita por `re.match`, que só exige que o
**começo** case (casa `"PT101"` e ignora o último `0`), e rejeitada por `re.fullmatch`, que exige a
string inteira. O mesmo vale para `"PT101 "`. Se `valida_tag` usasse `match`, aceitaria tags com
dígitos ou espaços a mais, e uma tag mal digitada passaria como válida.

### R2 — Linhas inválidas

Descartar uma linha é perder um dado, e quem chama precisa saber quanto e o quê foi perdido. No meu
log foram 4 linhas inválidas em 2408, e elas aparecem na Etapa 1(a). Se o enlace com a RTU começar a
falhar, as linhas `### falha de comunicacao com a RTU ###` aumentam e as leituras de PT102 ficam com
buracos. Descartadas em silêncio, uma sobrepressão durante a falha passaria despercebida e a média
pareceria normal. Com as linhas devolvidas, a taxa de inválidas vira um indicador da saúde da comunicação.

### R3 — Late binding

A lambda da compreensão não guarda o **valor** de `k`: guarda a **variável** `k`, que só é lida quando
a função é chamada. Nesse momento a compreensão já terminou e `k` vale o último fator do dicionário,
0,1 (o do FT201). Por isso todas as funções dão `4095 * 0.1 = 409.5`. Na minha `criar_conversores`,
cada lambda é criada dentro de uma chamada de `_multiplicador(fator)`. Cada chamada tem o seu próprio
escopo, e a lambda fica presa ao `fator` daquela tag, por isso `certos["PT102"](4095)` dá 600,0.

### R4 — Escala nominal

A escala nominal (`600/4095` kPa por contagem) supõe que o transmissor é linear. Ela dá 262,0 kPa
para a média das contagens normais (1788,3), contra 380 kPa de referência. Hipótese: a resposta do
transmissor não é linear. A explicação está em `fornecido/simulador.py`, na função `p_real`:
`p = 600·sin(π/2 · c/4095)`. Ela é côncava, então, no meio da escala, a reta fica muito abaixo da
curva. A `tabela_calibracao` (9 pontos dessa curva) é o que o Marco 2 usa para corrigir isso.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ~10× | 18,0× (36 000 056 / 2 000 000 bytes) |
| Tempo do laço / tempo vetorizado | ~50× | ~25× (54,7 ms / 2,2 ms) |
| Tempo da compreensão / tempo do laço | ~0,8 | ~0,94 (51,3 ms / 54,7 ms) |

A maior diferença foi na aceleração do vetorizado: previ 50× e medi cerca de 25×. A conta
`c * 600 / 4095` faz duas passagens sobre o array e cria arrays temporários de `float64` (8 MB cada),
e esse custo de memória pesa contra o ganho. A lista também ocupou mais do que previ, 36 bytes por
elemento: 8 do ponteiro mais 28 de cada objeto `int`. `uint16` vai até 65 535, e 81 900 transborda:
`81 900 − 65 536 = 16 364` (a conta é módulo 2¹⁶). Eu guardaria as contagens em `uint16` (0 a 4095
cabem em 2 bytes) e as pressões em kPa em `float64`, para não perder precisão nas contas.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `SerieTemporal` | `SerieTemporal` |
| `s[0]` | `float` | `float64` |

A única diferença foi `s[0]`: previ `float` e veio `numpy.float64`, porque indexar por inteiro devolve
um escalar do NumPy, e não um `float` do Python. O resultado mais estranho, mesmo previsto, é
`s.sum()` ser uma `SerieTemporal`: numa subclasse de `ndarray`, a redução devolve um array 0-d da
própria classe, e não um número. É por isso que `amplitude()` e o `marco1.py` usam `float(...)`.

### R7 — Issue #4

**Sintoma:** com 600 pontos e janela 30, `media_movel` devolvia 570 valores, e não 571.
**Testes:** `test_tamanho_n_menos_janela_mais_um`, `test_primeira_janela_incluida` e
`test_janela_do_tamanho_da_serie`, em `TestRegressaoMediaMovel`. **Causa:** `c = cumsum(s)` tem
`c[i] = s[0] + … + s[i]`, então `c[j:] − c[:-j]` dá as somas de `s[i+1 : i+j+1]`. A janela que começa
em 0 precisaria de `c[−1] = 0`, que não existe. **Correção:** pôr um zero na frente da soma acumulada.
Os testes de aceitação só conferiam o tipo e os erros, nunca o tamanho nem os valores. Outro caso
descoberto é `janela == len(s)`, que devolvia vazio: coberto por `test_janela_do_tamanho_da_serie`.

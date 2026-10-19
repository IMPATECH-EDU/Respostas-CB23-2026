# Relatório — Maria Leticia Lins Nunes (3478)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
/home/leticia/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.4 | fornecido 1.0
```

### R1 — Expressões regulares

O padrão de tag é `[A-Z]{1,2}\d{1,3}`. A string `"PT1010"` é aceita por `re.match`, que só exige que o começo combine (`PT101`) e ignora o `0` que sobra, mas é rejeitada por `re.fullmatch`, que exige a string inteira. O mesmo vale para `"PT101 "` (espaço no fim). Se `valida_tag` usasse `match`, ela devolveria `True` para essas duas tags inválidas.

### R2 — Linhas inválidas

`ler_log` devolve as linhas descartadas para que quem chamou possa contá-las, conferi-las e investigá-las. No meu log, 4 das 2408 linhas estavam corrompidas, e o `assert` do script confere esse número. Se elas fossem descartadas em silêncio, uma falha de comunicação com a RTU (as linhas `### falha de comunicacao ###`) passaria despercebida: um instrumento ficaria sem registrar durante minutos e o volume bombeado ou a pressão média seriam calculados com dados faltando, sem ninguém saber.

### R3 — Late binding

Em `{tag: (lambda c: c * k) for tag, k in escalas.items()}`, a lambda não guarda o valor de `k`, guarda a variável `k`. Ela só consulta o valor quando é chamada, e nesse momento o laço já terminou e `k` vale o último fator (0,1, do `FT201`). Por isso `errados["PT102"](4095)` dá 4095 × 0,1 = 409,5. A minha `criar_conversores` chama a função auxiliar `_fazer_conversor(fator)` para cada tag: cada chamada cria o seu próprio `fator`, que a lambda guarda e que nunca muda.

### R4 — Escala nominal

A escala nominal (600/4095) supõe que o transmissor é linear, isto é, que a pressão é proporcional às contagens. Minha hipótese é que ele não é linear. No `fornecido/simulador.py`, a função `p_real` mostra que a resposta verdadeira é `600 * sin(0,5 * pi * c / 4095)`. Para a contagem média normal de PT102 (cerca de 1788), a escala nominal dá 262,0 kPa, enquanto `p_real` dá 380,02 kPa, igual ao valor de conferência. A função `tabela_calibracao`, com 9 pontos, indica que o próximo passo é usar a calibração em vez da escala linear.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 063aa63

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 vezes | 18 vezes |
| Tempo do laço / tempo vetorizado | 100 vezes | 32 vezes |
| Tempo da compreensão / tempo do laço | 0,7 | 0,71 |

A maior diferença foi no tempo: previ ~100 vezes e medi 32. Minha hipótese é que subestimei o custo do NumPy: `contagens * 600 / 4095` percorre 1 milhão de elementos duas vezes e cria vetores temporários. `uint16 * 20` dá 16364 porque 81900 não cabe em 16 bits (máximo 65535) e o NumPy "dá a volta" sem avisar: 81900 − 65536 = 16364. Escolheria `uint16` para contagens e `float32` para kPa (`float64` se forem encadear muitos cálculos).

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O que mais me surpreendeu foi `s.sum()` devolver uma `SerieTemporal` (um array de dimensão 0) e não um número comum. A subclasse de `ndarray` mantém o seu tipo até nas reduções, enquanto `s[0]` devolve um escalar `float64`. Para ter um número simples preciso converter, como em `int(...)` ou `float(...)`, que usei na Etapa 1(c).

### R7 — Issue #4

Sintoma: 600 leituras e janela 30 davam 570 valores, não 571. Regressão: `test_tamanho_de_600_com_janela_30` e `test_primeira_media_inclui_o_inicio_da_serie`, que falhavam antes da correção. Causa: `cumsum[i]` já inclui o elemento `i`, então `acumulada[janela:] - acumulada[:-janela]` somava `self[i+1 : i+janela+1]`: a primeira janela (`self[0:janela]`) se perdia. Correção: um `0` na frente da soma acumulada. Os de aceitação só conferem o tipo de retorno e os erros de janela (0 e 6) de `media_movel`, nunca o tamanho nem os valores; com o defeito, todos passavam. Caso não coberto: janela igual a `len(s)` (dava zero valores), coberto por `test_janela_igual_ao_tamanho`.

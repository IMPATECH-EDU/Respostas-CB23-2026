# Relatório — Vitor Marian (3518)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Saída de `which python`: /c/Users/vitor/venvs/prog2-venv/Scripts/python

Etapa 0 do `python marco1.py`: 
=== Etapa 0: ambiente ===
Python 3.14.3 | NumPy 2.5.4 | fornecido 1.0

### R1 — Expressões regulares

Com o padrão `[A-Z]{1,2}\d{1,3}`, `re.match` aceita `"PT1010"` (casa o prefixo `PT101`), e `re.fullmatch` rejeita porque sobra o `0`. Se `valida_tag` usasse `match`, tags com sobra no fim, como `"PT1010"` e `"PT101 "`, seriam consideradas válidas.

### R2 — Linhas inválidas

Para que as falhas possam ser contadas e auditadas, em vez de sumirem. Se a comunicação com a RTU cair repetidamente durante um alarme de pressão alta, descartar essas linhas em silêncio faria parecer que a estação operou normalmente, quando na verdade ficou minutos sem leituras.

### R3 — Late binding

A lambda guarda a variável `k`, não o seu valor; `k` só é lido quando a função é chamada, e aí já vale o último fator do laço (`0.1`, de `FT201`): 4095 × 0,1 = 409,5. Em `criar_conversores`, o parâmetro padrão `fator=escalas[tag]` é avaliado na criação de cada lambda, então cada uma fica presa à sua própria tag.

### R4 — Escala nominal

O transmissor não é linear, pois a escala nominal supõe `p = c × 600 / 4095` e a resposta real é `p = 600 · sen(π/2 · c / 4095)`, que cresce mais rápido nas contagens médias. Por isso ~1788 contagens dão 262 kPa pela escala linear e 380 kPa pela curva real. A explicação está em `p_real` e `tabela_calibracao`, em `fornecido/simulador.py`.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d050c9b

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 16 | 18,0 |
| Tempo do laço / tempo vetorizado | 20 | 15,5 |
| Tempo da compreensão / tempo do laço | 0,5 | 0,97 |

**Justificativa da previsão** O `uint16` ocupa 2 bytes por elemento, e a lista padrão do Python certamente ocupa muito mais, o que torna a razão alta. Como o NumPy é otimizado para operações numéricas, a versão vetorizada deve ser a mais rápida. As versões com `list` e `map` devem ser mais lentas que o NumPy e ficar um pouco atrás da compreensão, que o Python também otimiza. Por fim, o laço `for` deve ter o pior desempenho, pois laços em Python não são adequados para tratamentos de dados simples como esse.

**Maior diferença** Considerando a diferença relativa entre o previsto e o medido, a maior diferença foi entre a compreensão e o laço de repetição. A compreensão só economiza a busca e o append no fim da lista; o maior custo, que é calcular `c * 600 / 4095` e criar um novo `float` por elemento, continua o mesmo, por isso o ganho foi bem menor que os 50% estimados.

**Estouro do `uint16`** O `uint16` guarda de 0 a 65535; 4095 × 20 = 81900 estoura e dá a volta: 81900 − 65536 = 16364. Para contagens (0 a 4095), pode-se usar `uint16`; já para pressões em kPa, `float64`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

**Justificativa da previsão** `s + s`, `s * 2` e `s[1:]` devem ser `SerieTemporal`, pois são operações ou fatiamentos sobre o próprio objeto da classe, então não há mudança de tipo. Já `s.sum()` e `s[0]` devem ser `float`: `s.sum()` é a soma dos itens de `s`, que são `float`, e `s[0]` é justamente um desses itens.

**Maior diferença** O `s.sum()` devolve uma `SerieTemporal` de dimensão 0, e não um número, porque o numpy repassa a subclasse no resultado das reduções. Note que `s[0]` devolve um escalar conforme previsto, porque referenciar um único elemento não usa esse mecanismo.

### R7 — Issue #4

Sintoma: `media_movel(30)` em 600 pontos devolvia 570 valores, e não 571. Teste de regressão: `test_quantidade_de_valores`. Causa: `acumulada[i]` é a soma de `self[0..i]`, então `acumulada[janela:] - acumulada[:-janela]` começa na janela `self[1:janela+1]` e perde a primeira. Correção: pôr um `0` no início da soma acumulada. A aceitação só confere o tipo e os erros, nunca o tamanho nem os valores. Outro caso não coberto: `janela == len(self)`, que devolvia 0 valores; é coberto por `test_janela_igual_ao_tamanho`.
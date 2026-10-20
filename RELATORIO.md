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

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

Previsões registradas no commit: d050c9b

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 16 | |
| Tempo do laço / tempo vetorizado | 20 | |
| Tempo da compreensão / tempo do laço | 0,5 | |

**Justificativa da previsão** O `uint16` ocupa 2 bytes por elemento, e a lista padrão do Python certamente ocupa muito mais, o que torna a razão alta. Como o NumPy é otimizado para operações numéricas, a versão vetorizada deve ser a mais rápida. As versões com `list` e `map` devem ser mais lentas que o NumPy e ficar um pouco atrás da compreensão, que o Python também otimiza. Por fim, o laço `for` deve ter o pior desempenho, pois laços em Python não são adequados para tratamentos de dados simples como esse.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | |
| `s[1:]` | `SerieTemporal` | |
| `s * 2` | `SerieTemporal` | |
| `s.sum()` | `float64` | |
| `s[0]` | `float64` | |

**Justificativa da previsão** `s + s`, `s * 2` e `s[1:]` devem ser `SerieTemporal`, pois são operações ou fatiamentos sobre o próprio objeto da classe, então não há mudança de tipo. Já `s.sum()` e `s[0]` devem ser `float`: `s.sum()` é a soma dos itens de `s`, que são `float`, e `s[0]` é justamente um desses itens.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

# Relatório — <Renan Faria Domingos> (<3538>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

((.venv))Renan F. Domingos@BOOK-6HRA46BJSQ MINGW64 /d/Aulas de programação IMPA tech/programação 2/Respostas-CB23-2026 (projeto_3538)$ which python
/d/Aulas de programação IMPA tech/programação 2/Respostas-CB23-2026/.venv/Scripts/python

=== Etapa 0: ambiente ===
Python 3.12.10 | NumPy 2.5.3 | fornecido 1.0

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

### R1 — Expressões regulares

A string `"PT101 extra"` é aceita por `re.match(r"[A-Z]{1,2}\d{1,3}", ...)` pois o casamento ocorre no início da string, mas é rejeitada por `re.fullmatch`, que exige o casamento com a string inteira. Se `valida_tag` usasse `re.match`, aceitaria erroneamente tags inválidas seguidas de caracteres espúrios ou espaço (como `"PT101 "`, `"PT1010"` ou `"PT101abc"`).

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

A função `ler_log` devolve as linhas descartadas para garantir auditabilidade do log, permitindo diagnosticar falhas na telemetria. Se uma RTU ou canal de comunicação falhasse e enviasse mensagens como `"### falha de comunicacao com a RTU ###"`, descartar em silêncio esconderia a perda recorrente de pacotes de dados, fazendo parecer que a estação operava normalmente quando, na verdade, havia um apagão de sensores.

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

### R3 — Late binding

Em `errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}`, a variável `k` é buscada no escopo externo apenas no momento em que a lambda é chamada. Ao final do laço, `k` fica fixado no último valor do dicionário (`0.1` de `FT201`), resultando em `4095 * 0.1 = 409.5`. A função `criar_conversores` evita esse problema usando `f=fator` como argumento padrão da lambda, o que força a avaliação do fator no momento da criação da função.

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

A diferença ocorre porque a conversão nominal assume uma relação linear estrita entre contagens e pressão ($p = 600 \cdot c / 4095$), enquanto o transmissor físico real da planta possui uma resposta não linear. A explicação está nas funções `p_real(c)` e `c_real(p)` do módulo `fornecido/simulador.py`, que mostram que a resposta do sensor segue uma curva senoidal ($p = 600 \cdot \sin(0.5 \pi c / 4095)$).

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 335ac69

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 8x | 18.00x |
| Tempo do laço / tempo vetorizado | 50x | 10.00x |
| Tempo da compreensão / tempo do laço | 0.8x |0.95x |

**Diferença entre previsão e medição:**
A maior diferença ocorreu no tempo do laço em relação ao tempo vetorizado (previsto 50x vs medido 10.00x). Essa diferença ocorre porque, para 1.000.000 de elementos, a conversão e o overhead das chamadas internas do NumPy amortecem a aceleração em relação a vetores maiores. Em memória, a lista ocupou 18x mais espaço que o `uint16` (previsto 8x) porque a lista guarda ponteiros de 8 bytes para objetos inteiros envelopados (36 bytes/elemento), enquanto o `uint16` guarda apenas os dados brutos contíguos (2 bytes/elemento).

**Explicação do overflow em uint16:**
A operação `4095 * 20` resulta em `81900`. Como o `uint16` armazena valores de até $2^{16} - 1 = 65535$, ocorre um estouro (*overflow*) com aritmética modular modulo 65536: $81900 \pmod{65536} = 16364$.

**Escolha de dtypes:**
- **Para contagens (0 a 4095):** Escolheria `uint16`, pois ocupa apenas 2 bytes por elemento e suporta perfeitamente valores de até 65535 sem risco de overflow.
- **Para pressões em kPa:** Escolheria `float32` (ou `float64`), pois pressões são grandezas contínuas com casas decimais.

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | |
| `s[1:]` | SerieTemporal | |
| `s * 2` | SerieTemporal | |
| `s.sum()` | numpy.float64 | |
| `s[0]` | numpy.float64 | |

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

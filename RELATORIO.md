# Relatório — Cecília Maria Gomes dos Santos (3496)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

=== Etapa 0: ambiente ===
Python 3.14.7 | NumPy 2.5.4 | fornecido 2.0
C:\Users\cecil\Respostas-CB23-2026\.venv\Scripts\python.exe

### R1 — Expressões regulares

Uma string como "PT101_lixo" é aceita pelo re.match porque ele só verifica o começo do texto. O re.fullmatch rejeita porque exige que a string inteira esteja no padrão correto. Se a função valida_tag usasse match, o sistema acabaria aprovando tags com sujeira no final e processando dados errados em vez de descartá-los.

### R2 — Linhas inválidas

A função ler_log retorna as linhas descartadas para que possamos monitorar as falhas de comunicação. Se ela ignorasse os erros em silêncio, um defeito físico passaria despercebido, e o sistema apenas assumiria que há um volume menor de leituras. Ver esses erros ajuda a equipe a descobrir problemas no equipamento muito mais rápido.

### R3 — Late binding

No Python, funções lambda criadas dentro de um laço guardam a referência da variável, e não o seu valor no momento da criação. Assim, no código incorreto, todas as lambdas utilizam o último valor assumido pela variável no laço (0,1, referente ao sensor FT201), resultando na conta 4095 * 0,1. A função criar_conversores corrige o problema ao receber o fator como argumento padrão (f=fator), o que força o Python a fixar o valor exato no instante em que a lambda é definida.

### R4 — Escala nominal

Essa diferença acontece porque o cálculo da escala nominal considera que a medição do sensor começa do zero. Porém, ao ler o código do arquivo fornecido/simulador.py, notamos que o simulador adiciona um valor inicial na hora de gerar os dados exatos de referência.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 8 MB | 36000056 / 2000000 = 18 |
| Tempo do laço / tempo vetorizado | 2 MB | 0.13808 / 0.00696 = 19.8 |
| Tempo da compreensão / tempo do laço | 100 ms  | 0.11966 / 0.13808 = 0.87 |

A maior diferença foi no tempo, previ 2 vezes e medi 19,8 vezes (0,13808 s / 0,00696 s), porque o laço do Python trata um número por vez e o NumPy faz tudo de uma vez, em código compilado.
Na memória previ 8 vezes e medi 18, porque cada item da lista guarda um ponteiro e um objeto int (36 bytes), contra 2 bytes do uint16.
uint16 * 20 dá 16364 porque 4095 * 20 = 81900 passa do máximo 65535 e dá a volta: 81900 - 65536 = 16364.
Para as contagens usaria uint16, 0 a 4095 cabe em 2 bytes e para kPa usaria float64 que tem casas decimais.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float | SerieTemporal |
| `s[0]` | float | float64 |

O que mais me surpreendeu foi que s.sum() devolveu uma SerieTemporal, e não um número simples como eu previ. Como a SerieTemporal é uma subclasse do ndarray, o NumPy devolve o resultado da soma ainda no tipo da subclasse (um array de um único valor). Já s[0] pega o elemento de dentro da série e devolve só um float64.

### R7 — Issue #4

O sintoma era uma falha no cálculo do filtro da série temporal. Para garantir a correção, criamos o teste de regressão test_issue_4_soma_acumulada. A causa do problema estava no cálculo da soma acumulada (cumsum), que incluía índices fora da janela configurada. A solução foi reajustar os limites do intervalo no laço de processamento. Os testes de aceitação não detectaram o erro porque usavam apenas dados constantes, o que mascarava a falha. Outro cenário não coberto por eles são séries temporais vazias, caso que validamos no teste test_serie_vazia.
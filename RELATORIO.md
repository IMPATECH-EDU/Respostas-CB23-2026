# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
/opt/anaconda3/envs/ambiente_aluno/bin/python

=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.3 | fornecido 1.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
A string "EX248!" é aceita por re.match, uma vez que sua forma satisfaz a regra de começar com uma ou duas letras maiúsculas seguidas por 1,2 ou 3 números. No entanto, re.full.match a rejeitaria, pois possui um caractere "!" que está além das regras.
Como consequência, vê-se que re.fullmatch é mais restritivo e garante a padronização de tags, enquanto que re.match permitiria adições aleatórias no final e comprometeria a organização interna ao não garantir o padrão esperado.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
ler_log devolve as linhas descartadas para que seja possível analisar defeitos de comunicação ou dados corrompidos no monitoramento do sistema. Um exemplo realista em que isso é pertinente seria o caso de uma unidade perder contato com o sistema e passar a não conseguir produzir respostas válidas.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
O resultado final é 409,5 porque a função lambda só é chamada posteriormente, utilizando como fator de multiplicação do argumento c não pelo fator associado a cada item de "escalas", mas pelo último com que terminou o ciclo de criação de "errados": 0,1.


### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
A discrepância surge pela diferença entre a escala senoidal do medidor real e a linear utilizada no cálculo da nominal

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | |
| Tempo do laço / tempo vetorizado | 20 | |
| Tempo da compreensão / tempo do laço | 0.7 | |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | |
| `s[1:]` | SerieTemporal | |
| `s * 2` | SerieTemporal | |
| `s.sum()` | Float64 | |
| `s[0]` | Float64 | |

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

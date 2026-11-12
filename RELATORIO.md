# Relatório — Francisco Renan Vale Cardoso (3523)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

```
/home/renan/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.4 | fornecido 4.0
```

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

A string "PT101 ", uma das inválidas, é aceita por re.match e rejeitada por re.fullmatch. Isso
ocorre pois o re.match busca se a string começa com um trecho que casa com a expressão regular. 
Por outro lado, o re.fullmatch exige que a string inteira case com o padrão da expressão regular.
Se usássemos re.match em valida_tag, strings que começam com uma sequência válida mas possuem um
resto qualquer passariam na validação. Isso viola o contrato, que diz que a tag tem de ter 1 ou 2
letras maiúsculas e de 1 a 3 dígitos, e não mais que isso.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

A função ler_log devolve as linhas descartadas devido a integridade da informação: jogar fora os logs inválidos estaria 
jogando informação fora, não sendo possível resgatar parte dela ou entender um erro que possa estar ocorrendo com os dados,
de modo que a investigação é sobre a captação ou transmissão deles. Uma situação real para exemplificar o problema de jogar
os dados fora seria um eventual pico de dados ser considerado inválido e descartado, mas esse pico de dados pode nos estar
informando que algum aparelho de captação como o RTU dos dados ou alguma rede de comunicação está defeituosa. Com meus dados
recebi 4 linhas avisando sobre invalides de dados, onde elas apontam falha na comuniação com o RTU, e isso é importante saber.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

A forma errada é escrita assim `errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}`. Como k sempre varía e não é
fixo para cada tag, logo quando a comprehesion acaba o valor de k é último possível. Se o último valor foi para um sensor de fluxo,
logo ele guarda k = 0.1, e então o cálculo sai errado para os sensores de pressão, e por isso temos 409,5, que é 4095 * 0.1. A
minha criar_conversores guarda o k junto com a lambda, logo não há o problema da variação de k influenciar a lambda: a lambda guarda
a sua constante que será usada na hora. Esse problema também ocorre pel fato de criar_conversores ser uma função que apenas cria as
conversões: se ela cria-se uma conversão e a aplicasse em seguida ainda daria certo.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 4 | |
| Tempo do laço / tempo vetorizado | 4 | |
| Tempo da compreensão / tempo do laço | 1 | |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | | |
| `s[1:]` | | |
| `s * 2` | | |
| `s.sum()` | | |
| `s[0]` | | |

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

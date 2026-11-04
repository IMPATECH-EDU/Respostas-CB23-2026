# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

Path do python e Etapa 0:

No linux do IMPATECH.
``` 
-> which python                               
/home/al.souza.pedro/venvs/prog2-venv/bin/python
```
``` 
-> python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 4.0
``` 
No meu windows pessoal.
``` 
-> (Get-Command python).Path
C:\Users\pedro\venvs\prog2-venv\Scripts\python.exe
```
```
-> python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.5 | NumPy 2.4.6 | fornecido 4.0
```

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
re.match aceita 'PT103weubcwo9ien\n\nscv658212r5', mas re.fullmacth rejeita. Usar re.macth permite falsos positivos, já todos os positivos de fullmatch está contido em todos os positivos de match (O contrário não vale).

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Ainda que uma linha não seja útil para as medições, o sensor pode comunicar um erro por mensagem. Essa linha é corrompida do ponto de vista do tratamento dos dados, mas contém informação relevante. Basta ver uma das linhas corrompidas "### Falha de comunicação com o RTU ###" de exemplo.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Ao definirmos uma função lambda, criamos um escopo onde podemos definir variáveis. Errados define a variável de entrada, mas usa diretamente o k definido no escopo do for in line. Então quando chamamos a função, ela tenta usar uma variável que não existe no seu escopo e segue procurando nos escopos que contém a função. No escopo do for in line, k refere-se ao último valor acessaso. Na nossa função, k é definido no escopo de lambda.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
Nossa função de conversão é linear, mas a conversão real se da pela expressão c = 4095 · (2/π) · arcsin(p / 600), como pode ser visto em c_real em simulador.py.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: abaa37e <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 36000056/2000000 ~ 18.000028 | |
| Tempo do laço / tempo vetorizado ~35 | | |
| Tempo da compreensão / tempo do laço ~0.71 | | |

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

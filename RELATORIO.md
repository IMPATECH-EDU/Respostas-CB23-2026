# Relatório — Augusto Schaefer Huff (3527)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente
#### Output do Which Python
(prog2-venv) (ambiente_aluno) al.augusto.huff@C1-14-15-16124:~/Documentos/Respostas-CB23-2026$ which python
/home/al.augusto.huff/venvs/prog2-venv/bin/python

#### Output do marco1.py - Etapa 0
(prog2-venv) (ambiente_aluno) al.augusto.huff@C1-14-15-16124:~/Documentos/Respostas-CB23-2026$ python marco1.py 
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 2.0

### R1 — Expressões regulares
<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
"PT101 " e "PT1010"
O valida_tag aceitaria ambas como True se usassemos o re.match, o que iria em desacordo com o enunciado que especifica que ambas são inválidas.


### R2 — Linhas inválidas
<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Por que é importante saber quais linhas estão sendo descartadas, para poder identificar a causa dessas linhas inválidas. Um exemplo de situação real é algum sensor que não está funcionando ou algum erro de configuração/digitação na hora de digitar as tags, o que causaria o descarte das linhas.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | | |
| Tempo do laço / tempo vetorizado | | |
| Tempo da compreensão / tempo do laço | | |

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

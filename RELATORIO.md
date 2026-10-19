# Relatório — <Guilherme Araújo Diniz> (<3510>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/home/guilharaujo/venvs/prog2-venv/bin/python

=== Etapa 0: ambiente ===
Python 3.14.6 | NumPy 2.5.4 | fornecido 3.0

=== Etapa 1: leitura do log ===
Traceback (most recent call last):
  File "/mnt/c/Users/guilh/pogramas/prog2/Respostas-CB23-2026/marco1.py", line 159, in <module>
    main()
    ~~~~^^
  File "/mnt/c/Users/guilh/pogramas/prog2/Respostas-CB23-2026/marco1.py", line 151, in main
    registros = etapa1(texto, verdade)
  File "/mnt/c/Users/guilh/pogramas/prog2/Respostas-CB23-2026/marco1.py", line 41, in etapa1
    registros, invalidas = ler_log(texto)
                           ~~~~~~~^^^^^^^
  File "/mnt/c/Users/guilh/pogramas/prog2/Respostas-CB23-2026/elevatoria/dados.py", line 72, in ler_log
    raise NotImplementedError("issue #1: ler_log")
NotImplementedError: issue #1: ler_log
<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

### R1 — Expressões regulares

String aceita por re.match e rejeitada por re.fullmatch
<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

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

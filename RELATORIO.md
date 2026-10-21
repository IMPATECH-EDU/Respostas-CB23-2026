# Relatório — Mickael Eleakim dos Santos Oliveira Almeida (3492)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/home/al.mickael.eleakim/venvs/prog2-venv/bin/python

Python 3.14.4 | NumPy 2.3.5 | fornecido 4.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 9ed72f0

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18× (cerca de 36 MB contra 2 MB: 36 bytes por elemento na lista, 28 do `int` mais 8 do ponteiro, contra 2 bytes no `uint16`) | |
| Tempo do laço / tempo vetorizado | ≈ 30 a 40× (laço perto de 0,1 s, vetorizado perto de 3 ms) | |
| Tempo da compreensão / tempo do laço | ≈ 0,8× (compreensão um pouco mais rápida, perto de 1×) | |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | |
| `s[1:]` | `SerieTemporal` | |
| `s * 2` | `SerieTemporal` | |
| `s.sum()` | `SerieTemporal` (0-d, a subclasse costuma ser mantida) | |
| `s[0]` | `np.float64` | |

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
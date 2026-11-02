# Relatório — FLÁVIA JAKELINE DOS SANTOS AGRA (3479)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

A pressão do recalque com a escala nominal (a reta, c·600/4095) dá 262 kPa, mas o valor de conferência é 380 kPa. A hipótese, então, é de que o transmissor não segue uma reta, mas alguma outra curva que só coincide com a reta em 0 e em 4095 contagens. Em fornecido/simulador.py (funções p_real e c_real), temos que o transmissor não segue uma reta, mas sim uma função seno. Rodando c_real(380), temos cerca de 1788 contagens. Na escala nominal, isso dá 262 kPa, que é diferente de 380, então a reta não representa mesmo o transmissor. 

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 3a0f239

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18x | cerca de 18 vezes |
| Tempo do laço / tempo vetorizado | 40x | cerca de 10,7 vezes |
| Tempo da compreensão / tempo do laço | 68% | 52% |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | np.ndarray | |
| `s[1:]` | np.ndarray | |
| `s * 2` | np.ndarray | |
| `s.sum()` | np.uint64 | |
| `s[0]` | np.uint16 | |

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

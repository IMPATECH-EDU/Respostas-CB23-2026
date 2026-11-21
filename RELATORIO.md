# Relatório — Arthur Adriano Jacometi Barbosa (3544)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
/home/al.arthur.barbosa/venvs/prog2-venv/bin/python

### R1 — Expressões regulares

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

- **Sintoma e regressão:** Para uma série de $n$ pontos e janela $k$, `media_movel` devolvia $n - k$ valores em vez de $n - k + 1$ (ex.: 570 para $n=600, k=30$), descartando a primeira janela; coberto pelo teste `TestMediaMovel.test_media_movel_simples`.
- **Causa e correção:** O código original fazia `acumulada[janela:] - acumulada[:-janela]` diretamente sobre `np.cumsum(self)`, omitindo a diferença `acumulada[janela - 1] - 0` da primeira janela; a correção insere `0.0` no início da soma acumulada (`np.insert(np.cumsum(self), 0, 0.0)`), alinhando os índices.
- **Lacuna nos testes:** Os testes de aceitação verificavam apenas propriedades gerais (como tipo de retorno ou valores internos) sem checar o comprimento exato $n - k + 1$ nem casos de borda como $k = n$ (que antes devolvia série vazia), caso coberto pelo meu teste `TestMediaMovel.test_media_movel_janela_total`.

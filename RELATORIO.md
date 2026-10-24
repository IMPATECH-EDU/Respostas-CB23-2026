# Relatório — Felipe Beck Santor (3549)

<!--Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.-->

## Marco 1

### Ambiente

- Saída de "which python":
```bash
/home/al.felipe.santor/venvs/prog2-venv/bin/python`
```
- Etapa 0 do marco1.py:
```bash 
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 2.0
```

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

### R1 — Expressões regulares

- Exemplo que "re.match" aceita e "re.fullmatch" não aceita:
`AB123 coisa`

Isso implica que a função "valida_tag" irá apenas aceitar tags que cumprirem com os requisitos e não se extenderem para além do tamanho requisitado.

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

"ler_log" deve devolver as linhas descartadas pois é uma boa prática mostrar ao usuário a razão do erro, ou ao menos, o que resultou em erro. Por exemplo, se uma tag for lançada de maneira incorreta, e não soubermos qual tag foi, precisariamos analisar todas as tags e fazer uma verificação manual em cada uma para poder corrigir o erro.
<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

### R3 — Late binding

"errados\["PT102"](4095)" tenta converter as contagens em kPa, porém, devido ao Late Binding, este guarda uma função lambda c: c * k, com k = 0.1, ao invés de k = 600/4095, pois k recebe o valor 0.1 em sua última atribuição de "escalas". Já em "criar_conversores", consertamos esse erro ao criar uma variável auxiliar e determinar o valor do parâmetro da função lambda igual à essa variável (como default value), ao invés de passar essa variável diretamente como parâmetro, lambda c, f=fator: c * f [...], assim evitando o Late Binding. 
<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

A diferença é esperada pelo assert: o item 2(f) usa uma conversão linear nominal para calcular a pressão, enquanto o simulador gera as contagens com um modelo não linear.

Em marco1.py, o fator de PT102 é 600 / 4095. Aplicado à média das contagens normais, ele dá cerca de 261,9 kPa. O valor de referência é 380 kPa, então a diferença é de aproximadamente 118,1 kPa — e por isso abs(p_nominal - verdade["pressao_recalque"]) > 100 passa.

Em simulador.py temos as seguintes funções com as suas respectivas funcionalidades:
- `p_real` calcula a pressão com uma função seno.
- `c_real` calcula a operação inversa para gerar contagens a partir da pressão de referência.
- `gerar_log` usa esse modelo para gerar as leituras de PT102 e acrescenta cinco leituras falsas; a condição <= 2000 em marco1.py as exclui da média.

Com a minha matrícula, a média das contagens normais é aproximadamente 1787,8. Pelo modelo real, isso corresponde a cerca de 380 kPa; pela escala linear simplificada, dá aproximadamente 261,9 kPa. A comparação mostra que a escala nominal não representa a curva real do transmissor nessa faixa.
<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 909ed5f <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` |cerca de 18x               |17,85x |
| Tempo do laço / tempo vetorizado       |vetorizado é bem mais veloz|25.9x  |
| Tempo da compreensão / tempo do laço   |tempos similares           |1.1x   |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s`   |SerieTemporal  |SerieTemporal| 
| `s[1:]`   |float          |SerieTemporal|
| `s * 2`   |SerieTemporal  |SerieTemporal|
| `s.sum()` |float          |SerieTemporal|
| `s[0]`    |float          |float64      |

Fique surpreso que previ três floats, mas só veio um. O resultado que mais me supreende é como s.sum() retorna uma SerieTemporal. Pensava que estariamos somando os floats contidos em uma SerieTemporal, e portanto iriamos receber um float em retorno. Vou ter que dar uma olhada nessa função.

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

**Sintoma:**
Função `media_movel` em `elevatoria\serie.py` estava retornando um dado a menos do que deveria, de acordo com docstring. Mas apesar disso, passsava nos testes de aceitação. 
**Causa:**
Havia um deslocamento de índice em `np.cumsum`, por isso, a função não estava considerando a primeira janela.
**Correção:**
Adicionamos um zero no início da variável `acumulada`, para evitar esse deslocamento de índice. Além disso, tive que garantir que a função retornava uma `SerieTemporal`, pois sem essa parte, não passava nos testes.
**Por que os testes não pegaram o defeito antes?**
Isso aconteceu porque o teste não verifica se os valores estão certos, nem se a quatidade de valores está certa, apenas verifica se janelas inválidas realmente estão sendo tratadas como inválidas, levantando `ValueError`, e se o tipo que a função retorna está correto (ou seja, retorna uma `SerieTemporal`)
**Testes que implementei:**
Os testes que implementei em `testes\test_dados.py` cobrem tanto o tamanho da janela quanto os valores que a função retorna, assim garantindo o bom funcionamento da função.

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

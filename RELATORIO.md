# Relatório — Nícolas Kemmerich (3460)
## Marco 1

### Ambiente

No Windows, o comando `where.exe python` retornou:
- `C:\Users\nicol\AppData\Local\Microsoft\WindowsApps\python.exe`
- `C:\Users\nicol\AppData\Local\Python\bin\python.exe`

O executável utilizado (`sys.executable`) foi `C:\Users\nicol\AppData\Local\Python\pythoncore-3.14-64\python.exe`.

Etapa 0: Python 3.14.3, NumPy 2.5.3 e fornecido 3.0. Todas as verificações iniciais do NumPy passaram.

### R1 — Expressões regulares

`re.match` verifica, desde o começo da string, se há alguma correspondência ao formato exigido, mas isso não implica que o restante da entrada também esteja correto. Já `re.fullmatch` verifica se a string inteira corresponde ao formato exigido. Pode-se usar como exemplo a tag `PT1010`: se o padrão reconhecer `PT101`, `re.match` poderá encontrar essa correspondência no início da string, embora `PT1010` seja uma tag inválida, o que pode causar erros nos processamentos posteriores. Portanto, utilizar `re.fullmatch` em `valida_tag` garante que a string inteira corresponda ao padrão definido para uma tag.
### R2 — Linhas inválidas

A função `ler_log` devolve as linhas inválidas para que a pessoa responsável pela análise dos dados possa examiná-las, investigar a causa do erro e buscar uma solução. Caso essas linhas fossem descartadas silenciosamente, falhas de comunicação ou linhas corrompidas poderiam passar despercebidas, dificultando a análise dos dados e podendo produzir resultados imprecisos devido à perda de leituras.

### R3 — Late binding

O dicionário `errados` utiliza o mesmo fator de conversão `k` para todas as suas funções `lambda`. Ao terminar a compreensão do dicionário, `k` corresponde ao último fator percorrido, que é `0.1`, da tag `FT201`. Por isso, `errados["PT102"](4095)` calcula 4095 x 0,1 = 409,5, em vez de retornar `600`. Já a função `criar_conversores` faz com que cada conversor preserve o fator correspondente à sua própria tag, evitando o problema de *late binding* e garantindo que a ordem dos itens não altere os resultados.

### R4 — Escala nominal

A escala nominal produz aproximadamente 262 kPa porque, no `marco1.py`, as contagens de `PT102` são convertidas por meio de um fator linear (`600/4095`). Entretanto, no `fornecido/simulador.py`, a função `c_real` utiliza arco-seno para gerar as contagens a partir da pressão, enquanto `p_real` utiliza seno na relação direta. Essa diferença explica por que a conversão nominal linear não recupera o valor de referência de 380 kPa.

### R5 — Previsão × medição (Etapa 3)

Não registrei as previsões em um commit antes das medições. As estimativas desta tabela foram reconstruídas posteriormente, com base no comportamento esperado das estruturas e operações.

| Grandeza | Estimativa retrospectiva | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` |10x|18,00x|
| Tempo do laço / tempo vetorizado |10x|15,56x|
| Tempo da compreensão / tempo do laço |1x|0,76x|

A maior diferença entre as estimativas retrospectivas e as medições ocorreu na relação entre a memória da lista e a memória do `uint16`: 10x estimados contra 18x medidos. A `list` ocupou cerca de 18 vezes mais memória que `uint16`, pois armazena referências para objetos Python, enquanto cada elemento `uint16` ocupa 2 bytes. O produto 4095 × 20 = 81900 ultrapassa o máximo de 65535; o *overflow* corresponde a retirar uma volta de 65536, resultando em 16364. Escolheria `uint16` para contagens de 0 a 4095 e `float64` para pressões com valores decimais.
### R6 — Tipos da SerieTemporal (Etapa 4d)

Como não registrei os tipos previstos antes da implementação, a coluna de previsão abaixo foi reconstruída retrospectivamente.

| Expressão | Tipo previsto (estimativa retrospectiva) | Tipo observado |
| --- | --- | --- |
| `s + s` |`SerieTemporal`|`SerieTemporal`|
| `s[1:]` |`SerieTemporal`|`SerieTemporal`|
| `s * 2` |`SerieTemporal`|`SerieTemporal`|
| `s.sum()` |`float64`|`SerieTemporal`|
| `s[0]` |`float64`|`float64`|

O resultado de `s.sum()` me chamou a atenção porque eu esperava que a soma de todos os elementos retornasse um valor escalar. Entretanto, o resultado observado foi um objeto `SerieTemporal` de dimensão zero (`shape == ()`). Isso mostra que a operação preservou o tipo da subclasse `SerieTemporal`, mesmo produzindo um único valor.

### R7 — Issue #4

O defeito fazia `media_movel` retornar um resultado a menos: para uma série de 5 elementos e uma janela de 3, retornava 2 valores em vez dos 3 esperados. O teste `test_media_movel_tamanho_retornado` verifica a quantidade de resultados, enquanto `test_media_movel_valores_janela_2` confere as médias de `[10, 20, 30]`, que devem ser `[15, 25]`. A causa era a diferença entre fatias da soma acumulada sem um zero inicial; a correção foi inserir `0.0` no início para calcular também a primeira janela. Os testes de aceitação verificavam o tipo de retorno e os parâmetros inválidos, mas não esses casos específicos, cobertos pelos meus testes próprios.

## Marco 2

### Ambiente

Python 3.14.3, NumPy 2.5.3, SciPy 1.18.1, fornecido 4.0 e matrícula 3460.

### R8 — Derivada numérica

Quando o valor de \(h\) diminui, a aproximação da derivada fica inicialmente mais precisa, pois o erro de truncamento é reduzido. Porém, quando \(h\) fica muito pequeno, os valores utilizados na subtração ficam muito próximos, causando perda de algarismos significativos. Como essa diferença é dividida por \(h\), o erro de arredondamento acaba aumentando. Em \(h=10^{-14}\), `1000 + 1e-14` resulta em `1000`, devido à precisão limitada dos números de ponto flutuante, fazendo com que o numerador seja zero e o erro absoluto fique igual ao valor da derivada exata.

### R9 — Issue #7

O erro estava no cálculo da variável `correcao`: como `t` já armazenava o resultado da soma `self._soma + y`, a expressão original acabava subtraindo o mesmo valor de si próprio, resultando em zero. Embora as expressões sejam algebricamente equivalentes, a ordem das operações importa em ponto flutuante, pois cada operação pode introduzir arredondamentos. Os testes de aceitação não identificaram o problema porque utilizavam somas simples, com poucas parcelas. Para verificar essa falha, foram criados os testes `test_milhao_de_pulsos` e `test_compensacao_de_parcelas_pequenas`, que falhavam antes da correção.

### R10 — Precisão × exatidão

Ambas as curvas apresentaram praticamente a mesma precisão, como mostram os desvios-padrão: `0,548 kPa` para a linear e `0,549 kPa` para a spline. Porém, isso não significa que tenham a mesma exatidão, pois a curva linear apresentou um viés de `-1,828 kPa`, enquanto a spline apresentou apenas `0,001 kPa`. Isso mostra que a curva linear produziu valores abaixo da referência. Mesmo com quase 600 medições, o aumento da quantidade de dados não elimina o viés sistemático causado pela calibração.

## Marco 3

### R11 — Bissecção × Newton

A bissecção começa sempre com o mesmo intervalo `[2, 15]` e a mesma tolerância, por isso precisou das mesmas `44 iterações` nos três valores de Reynolds. Neste caso, o Newton foi mais rápido e apresentou ordem de convergência próxima de 2, ou seja, o erro diminui aproximadamente ao quadrado a cada iteração. Porém, pode falhar quando a derivada no ponto atual é zero, pois precisa dividir por ela. A bissecção ainda pode funcionar se houver troca de sinal e continuidade no intervalo.
### R12 — Issue #9

Antes da correção, a derivada era calculada apenas no primeiro ponto e permanecia fixa durante as iterações. Por isso, em vez de convergir quadraticamente, o Newton convergia de forma linear e precisava de 10 iterações. Os testes do professor não identificavam o problema porque verificavam apenas se o método encontrava a raiz, sem avaliar sua velocidade. Para identificar essa falha, criamos os testes `test_newton_com_derivada_exata` e `test_newton_com_derivada_numerica`, que falhavam antes da correção e passaram depois.

## Marco 4

### R13 — Integração e descontinuidade

Quando integramos o custo do dia inteiro de uma vez, acabamos incluindo as mudanças bruscas de tarifa na mesma integral, o que prejudica a precisão dos métodos. Na execução, as ordens foram `1,00` para o trapézio e `0,65` para Simpson. Ao separar a integração por faixas tarifárias, recuperamos as ordens `2,00` e `4,00`, respectivamente, pois evitamos essas descontinuidades dentro dos intervalos.

### R14 — Issue #11

O trapézio subestimava o volume porque usava a largura do primeiro intervalo em todos os cálculos, mesmo com intervalos de 15 e 30 minutos causados pelas falhas do SCADA. Antes da correção, calculou `3560,1 m³`, com erro de `8,43%`; depois, chegou a `3890,0 m³`, com erro de apenas `0,05%`, próximo dos `3888,0 m³` de conferência. Os testes de aceitação utilizavam malhas uniformes; nossos testes foram `test_trapezio_usa_largura_de_cada_intervalo` e `test_trapezio_com_vazao_constante`. O Simpson não podia ser usado diretamente porque exige pontos igualmente espaçados.
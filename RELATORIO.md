# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

/home/emanuel-dionisio/venvs/prog2-venv/bin/python

### R1 — Expressões regulares

<!-- - **Dê uma string que `re.match` aceita e `re.fullmatch` rejeita com o padrão de tag, e diga o que aconteceria em `valida_tag` se você usasse `match`. -->

Um exemplo de string que `re.match` aceita mas `re.fullmatch` rejeita é "PT102 extra". Se usássemos `match` em `valida_tag`, ele aceitaria a tag "PT102" e ignoraria o restante da string, o que poderia levar a erros de validação, pois a função deveria rejeitar qualquer entrada que não corresponda exatamente ao padrão esperado. Isso ocorre pois `match` verifica apenas o início da string, enquanto `fullmatch` exige que toda a string corresponda ao padrão.

### R2 — Linhas inválidas

<!-- Por que `ler_log` devolve as linhas descartadas, em vez de simplesmente ignorá-las? Descreva uma situação na operação da estação em que descartar em silêncio esconderia um problema real. -->

`ler_log` devolve as linhas descartadas para permitir que o usuário ou o sistema de monitoramento identifique e investigue possíveis problemas na operação da estação. Por exemplo, se uma linha inválida contiver dados críticos de um sensor que falhou, simplesmente ignorá-la poderia levar a uma falsa sensação de normalidade, enquanto registrar a linha descartada alertaria os operadores sobre a necessidade de manutenção ou verificação do sensor.

### R3 — Late binding

<!-- Por que `errados["PT102"](4095)` dá 409,5? Por que a sua `criar_conversores` não tem o problema? -->

Por causa do late binding, a função `errados["PT102"]` retorna 409,5 porque a variável que define o fator de conversão foi avaliada no momento da execução da função, e não no momento da criação do dicionário. Isso significa que todas as funções no dicionário compartilham a mesma referência à variável, resultando em um valor incorreto. A minha implementação de `criar_conversores` evita esse problema ao capturar o valor do fator de conversão no momento da criação de cada função, garantindo que cada função tenha seu próprio valor independente.

### R4 — Escala nominal

<!-- Na Etapa 2(f), a escala nominal dá cerca de 262 kPa, e o valor de conferência é 380 kPa. Proponha uma hipótese para a diferença e diga onde, no código da base, está a explicação. (Ler o código de outras equipes faz parte do trabalho.) -->

A resposta está no arquivo `fornecido/simulador.py`, as funções `p_real` e `c_real` apresentam funções não-lineares (senos) em suas fórmulas. Por outro lado, a conversão no arquivo `marco1.py`, por volta da linha 95, que usa os conversores de `elevatoria/dados.py` é linear. A diferença entre a escala nominal e o valor de conferência pode ser explicada pela não-linearidade das funções reais, que não são capturadas pela conversão linear utilizada na escala nominal.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 64fb65c8db686c8364611efc7e41cf95b8e196a4

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 14 | 18 |
| Tempo do laço / tempo vetorizado | 50175 | 46.15 |
| Tempo da compreensão / tempo do laço | 1 | 0.67 |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

Para calcular `Memória da lista / memória` do `uint16`, a previsão considerou que um inteiro padrão ocupa 28 bytes e um uint16 ocupa 2 bytes, resultando em uma razão de 14. No entanto, a medição real mostrou que a lista ocupa mais memória devido aos metadados e a estrutura interna de armazenamento de objetos em Python, resultando em uma razão de 18. A expressão `uint16 * 20` resulta em 16364 porque o valor máximo de um uint16 é 65535, e ao multiplicar por 20, ocorre um estouro de valor, retornando o resultado modulado pelo tamanho do tipo. Para contagens, eu escolheria `uint16`, pois é suficiente para os valores esperados e economiza memória. Para kPa, eu escolheria `float32`, pois oferece precisão suficiente para medições de pressão sem desperdiçar memória.

Para calcular `Tempo do laço / tempo vetorizado`, considerei que o laço iterativo processa cada elemento individualmente em complexidade O(n), enquanto a operação vetorizada utiliza otimizações internas e processamento em lote, o que considerei aproximadanete O(log n). A medição real mostrou que o tempo vetorizado demorou menos do que o previsto. O meu erro foi não considerar a complexidade real das operações vetorizadas, que são também O(n) mas com constantes muito menores devido à otimização interna.

Para calcular `Tempo da compreensão / tempo do laço`, considerei que a compreensão de listas e o tempo do laço ambos rodam em O(n), então apenas se diferenciam por uma constante (que aproximei para perto de 1). A medição real mostrou que a compreensão de listas foi mais rápida do que o laço, com uma razão de 0.67. O meu erro foi não considerar que a compreensão de listas é otimizada internamente em Python, resultando em um desempenho melhor do que o laço explícito.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float | SerieTemporal |
| `s[0]` | np.float64 | np.float64 |

<!-- Explique o resultado que mais surpreendeu você. -->

O `s.sum()` retornou um tipo `SerieTemporal` em vez de `float`, o que foi surpreendente. Isso ocorreu porque a implementação da classe `SerieTemporal` não sobrescreveu corretamente o método `sum()` para retornar um valor escalar, mas sim retornou uma nova instância da própria classe. Isso indica que a operação de soma foi tratada como uma operação de agregação que mantém a estrutura da série, em vez de reduzir os dados a um único valor.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

Sintoma: `media_movel(30)` em uma série de 600 pontos devolvia 570 valores, mas o contrato exige 571 (`n - janela + 1`).
Teste de regressão: `test_media_movel_janela_um_preserva_todos_os_elementos` e `test_media_movel_tem_tamanho_n_menos_janela_mais_um`.
Causa: na soma de prefixos, faltava o zero inicial; sem ele, os cortes da soma acumulada ficavam deslocados e um resultado era perdido.
Correção: usar `np.concatenate((np.zeros(1), np.cumsum(self)))` e então calcular `(cs[i + w] - cs[i]) / w` de forma vetorizada.
Os testes de aceitação não pegaram porque não cobriam o caso crítico de janela 1, onde o erro aparece claramente.
Caso extra não coberto por aceitação: a preservação do tamanho correto para janela arbitrária (ex.: 600 e 30), coberta por `test_media_movel_tem_tamanho_n_menos_janela_mais_um`.
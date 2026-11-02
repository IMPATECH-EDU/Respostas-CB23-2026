# Relatório — Matheus Ramos - Matrícula 3467

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/home/al.matheus.souza/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 4.0

### R1 — Expressões regulares

A string `"PT101 extra"` é aceita por `re.match` com o padrão `[A-Z]{1,2}\d{1,3}` porque ele valida apenas o início da cadeia de caracteres. Já o `re.fullmatch` a rejeita por exigir que a string inteira case com a expressão. Se `valida_tag` utilizasse `match`, entradas com sufixos inválidos ou espaços sobressalentes (como `"PT101 "` ou `"PT1010"`) seriam aceitas incorretamente como tags válidas.

### R2 — Linhas inválidas

A função `ler_log` devolve as linhas descartadas para permitir auditoria, rastreabilidade e diagnóstico de falhas de comunicação. Em uma operação real, o descarte silencioso esconderia ruídos na rede, pacotes corrompidos ou mal funcionamento de um sensor. Isso levaria a equipe a operar a estação sem notar que leituras críticas estavam sendo perdidas na transmissão.

### R3 — Late binding

O valor `409,5` ocorre porque, na versão errada, o escopo da lambda busca a variável `fator` no momento da execução (*late binding*), fazendo com que todas as funções usem o último fator iterado no dicionário (o do `FT201`, igual a `0,1`, resultando em $4095 \times 0,1 = 409,5$), nossa `criar_conversores` resolve isso usando o parâmetro padrão na lambda (`f=fator`), o que força a vinculação antecipada (*early binding*) do fator exato de cada tag.

### R4 — Escala nominal

A diferença ocorre porque a conversão nominal faz um mapeamento linear simples de 0 a 4095 sobre a faixa do sensor, enquanto a geração real do dado aplica um *offset* e um fator de calibração específico da faixa de operação. A explicação exata dessa calibração está no arquivo `fornecido/simulador.py`, nas funções internas que simulam o comportamento do transmissor de pressão.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `aa706fd`

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 15x | 18x |
| Tempo do laço / tempo vetorizado | 20x | 31x |
| Tempo da compreensão / tempo do laço | 1x | 0.90x |

A maior diferença entre a previsão e a medição ocorreu na velocidade da conversão vetorizada, pois a implementação do NumPy executa as operações diretamente em linguagem C de forma otimizada, eliminando o overhead do interpretador Python muito além do previsto.

O estouro do uint16 ao multiplicar por 20 ocorre porque a capacidade máxima de 16 bits sem sinal é 65535. Como a contagem máxima do conversor é 4095, o cálculo  excede o limite e dá a volta, resultando exatamente em 16364.

Para armazenar as contagens puras (inteiros de 0 a 4095), o `dtype` ideal é o `uint16`, pois consome apenas 2 bytes por elemento e comporta todos os valores sem estouro. Para as pressões calculadas em kPa, o tipo adequado é `float32` ou `float64`, que garantem a representação correta de números decimais.

### R6 — Tipos da SerieTemporal (Etapa 4)

| Expressão | Previsão | Medido |
| --- | --- | --- |
| `s + 10` | `SerieTemporal` | `SerieTemporal` |
| `s[0]` | `float` | `np.float64` |
| `s[1:5]` | `SerieTemporal` | `SerieTemporal` |
| `s > 10` | `np.ndarray` | `SerieTemporal` |
| `s.mean()` | `float` | `np.float64` |

O resultado que mais se destaca é o fato de comparações lógicas (`s > 10`) e fatiamentos (`s[1:5]`) preservarem o tipo `SerieTemporal` em vez de regredirem para um `np.ndarray` comum. Isso ocorre porque a subclasse implementada herda o mecanismo de propagação de tipo do NumPy para operações vetorizadas. 

E a indexação de elemento individual (`s[0]`) e métodos de agregação (`s.mean()`) reduzem a dimensão dos dados, retornando escalares do NumPy (`np.float64`).

### R7 — Issue #4

O sintoma era o retorno de N - n elementos em vez de N - n + 1$ (ex.: 570 valores para 600 leituras e janela n=30). O defeito foi identificado pelo teste de regressão `test_media_movel_tamanho_correto`. A causa ocorria no fatiamento incorreto da soma acumulada (`cumsum`), que omitia o termo inicial necessário para calcular a primeira média do intervalo. 

A correção ajustou os índices do fatiamento da `cumsum` (inserindo o zero inicial no cálculo da diferença de janelas), sem laços e preservando o tipo `SerieTemporal`. Os testes de aceitação originais não pegaram o defeito porque comparavam apenas os valores das posições existentes, sem validar o tamanho exato do array retornado. Outro caso não coberto por eles é o de janela de tamanho unitário (n=1), validado pelo teste `test_media_movel_janela_um`.

## Marco 2

### Ambiente

/home/al.matheus.souza/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3467

### R8 — Derivada numérica

O erro diminui entre h = 1 e h = 1e-5 porque nessa faixa domina o erro de truncamento da aproximação por diferenças finitas, que diminui proporcionalmente a h. Abaixo de h = 1e-5, o erro passa a crescer porque passa a dominar o erro de arredondamento por cancelamento catastrófico ao subtrair dois números de ponto flutuante quase idênticos. Em h = 1e-14, a limitação de precisão de 64 bits faz com que 1000 + 1e-14 seja igual a 1000, resultando em f(x+h) - f(x) = 0 e derivada estimada zero, fazendo com que o erro seja exatamente o valor absoluto da própria derivada exata (0,2134).

### R9 — Issue #7

Os testes de regressão criados foram `test_kahan_compensacao_um_milhao_pulsos` e `test_kahan_supera_ingenuo_em_somas_longas`. Em ponto flutuante, a expressão incorreta `t - (s + y)` avalia primeiro `(s + y)`, que resulta exatamente em `t`, fazendo com que a diferença dê zero e anule a compensação de Kahan. Já a versão corrigida `(t - s) - y` avalia primeiro `(t - s)` para isolar a parcela efetivamente somada a `s` e recuperar o erro de arredondamento. Os testes de aceitação originais não detectaram o erro porque somavam poucas parcelas ou usavam tolerâncias amplas onde o acúmulo de erro ainda não ultrapassava os limites.

### R10 — Precisão × exatidão

A precisão está associada à dispersão aleatória das medições, representada pelo desvio padrão amostral, que foi praticamente idêntico para ambas as curvas (~0,54 kPa). A exatidão reflete o viés em relação ao valor real de referência (380,0 kPa): a spline obteve viés de apenas -0,027 kPa (alta exatidão), enquanto a curva linear apresentou viés de -1,856 kPa (baixa exatidão). A média de quase 600 leituras reduz a incerteza aleatória, mas não elimina o viés da curva linear por tratar-se de um erro sistemático de modelagem decorrente de tentar aproximar uma resposta não linear por uma reta.

## Marco 3

### R11 — Bissecção × Newton

A bissecção realiza o mesmo número de iterações (44) para qualquer Reynolds porque o número de divisões depende apenas do tamanho do intervalo inicial $[a, b]$ e da tolerância desejada ($L_k = L_0 / 2^k$), independente dos valores da função. A ordem de convergência 2 (quadrática) significa que o número de dígitos decimais exatos aproximadamente dobra a cada iteração. O método de Newton falha quando a derivada no ponto é nula ($f'(x) = 0$), quando o ponto inicial $x_0$ está muito distante da raiz ou quando oscila em pontos de inflexão, cenários onde a bissecção continua funcionando desde que haja troca de sinal ($f(a) \cdot f(b) < 0$).

### R12 — Issue #9

Os testes de regressão criados em `testes/test_operacao.py` foram `test_newton_convergencia_quadratica` e `test_newton_poucas_iteracoes_para_precisao_alta`. Calcular a derivada uma única vez fixa a inclinação da tangente no ponto inicial $x_0$, transformando o algoritmo no método de Newton modificado/cordas, o que reduz o erro por um fator constante a cada passo e degrada a convergência para linear ($p \approx 1$). Os testes de aceitação originais não detectaram o defeito porque apenas verificavam se o valor final da raiz estava correto dentro da tolerância, sem checar a ordem de convergência ou o número limite de iterações.

## Marco 4

### R13 — Integração e descontinuidade

A teoria de convergência das regras de quadratura (Trapézio $O(h^2)$ e Simpson $O(h^4)$) exige que a função seja suave e tenha derivadas contínuas no intervalo de integração. As mudanças bruscas na tarifa de energia às 18 h e 21 h introduzem descontinuidades do tipo salto na função de custo. Nos subintervalos que contêm esses saltos, o erro local passa a depender diretamente da altura do salto e não mais da derivada, reduzindo a ordem de convergência global para 1. Ao integrar cada faixa tarifária separadamente, as descontinuidades ficam posicionadas exatamente nos limites dos intervalos de integração, tornando a função suave dentro de cada faixa e restaurando as ordens teóricas 2 e 4.

### R14 — Issue #11

Os testes de regressão criados em `testes/test_dia.py` foram `test_trapezio_tabela_malha_irregular` e `test_trapezio_tabela_intervalos_faltantes`. A causa do defeito era a suposição de que o passo entre as medições era constante ($h = x_1 - x_0$), calculando a área como se todos os subintervalos tivessem a mesma largura. Os testes de aceitação originais não pegaram o defeito porque utilizavam apenas tabelas com espaçamento uniforme. A regra de Simpson não serve para o registro do dia porque exige uma malha estritamente uniforme e número par de subintervalos, requisito violado pelas 8 leituras perdidas pelo SCADA.
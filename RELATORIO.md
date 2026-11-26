# Relatório — 3463

## Marco 1

### Ambiente

C:\Users\carol\AppData\Local\Programs\Python\Python314\python.exe
Python 3.14.3 | NumPy 2.5.5 | fornecido 4.0

### R1 — Expressões regulares

A string `PT101extra` é aceita por `re.match(r"[A-Z]{1,2}\d{1,3}", ...)`, pois `match` verifica apenas o começo da string. `fullmatch` rejeita porque exige que toda a string corresponda ao padrão. Se `valida_tag` usasse `match`, tags com caracteres extras no final poderiam ser aceitas incorretamente, como `PT101extra` ou `PT101 `.

### R2 — Linhas inválidas

As linhas descartadas são devolvidas para que a aplicação consiga contabilizar falhas de comunicação e investigar a qualidade do registro, em vez de ocultar o problema. Por exemplo, se o cabo de comunicação de um transmissor falhar e várias mensagens forem truncadas, ignorá-las silenciosamente faria parecer que houve menos leituras sem indicar a falha. Na execução, foram encontradas 4 linhas inválidas.

### R3 — Late binding

Na compreensão que cria `errados`, cada lambda consulta a variável `k` quando é chamada, e não quando é criada. Ao final da compreensão, `k` contém o último fator do dicionário, `0.1`, por isso `errados["PT102"](4095)` calcula `4095 × 0.1 = 409.5`. Em `criar_conversores`, o argumento padrão `fator=fator` guarda o valor correspondente no momento da criação de cada lambda, evitando que todas usem o último fator.

### R4 — Escala nominal

A conversão linear pela escala nominal produziu aproximadamente **261.98 kPa**, enquanto o valor de conferência é **380 kPa**. Uma hipótese é que o transmissor não tem resposta linear. A explicação está em `fornecido/simulador.py`, na função `p_real(c)`, que modela a pressão com uma função seno. A função inversa `c_real(p)` usa arco-seno. Portanto, multiplicar as contagens por `600/4095` não desfaz a calibração não linear do sensor.

### R5 — Previsão × medição

**Previsões qualitativas registradas para comparação:** a lista deve consumir muito mais memória que as representações compactas; `uint16` e `array('H')` devem usar 2 bytes por contagem; `int32` e `float32`, 4 bytes; `int64` e `float64`, 8 bytes. Para tempo, a previsão é que a conversão vetorizada do NumPy seja a mais rápida, pois aplica a operação ao array sem executar um laço Python por elemento.

**Medição desta execução (1.000.000 de contagens):**

| Estrutura | Bytes totais | Bytes por elemento | Razão lista/estrutura |
|---|---:|---:|---:|
| `list` | 36.000.056 | 36 | 1,00× |
| `array('H')` | 2.000.000 | 2 | 18,00× |
| `uint16` | 2.000.000 | 2 | 18,00× |
| `int32` | 4.000.000 | 4 | 9,00× |
| `int64` | 8.000.000 | 8 | 4,50× |
| `float32` | 4.000.000 | 4 | 9,00× |
| `float64` | 8.000.000 | 8 | 4,50× |

| Método | Tempo médio (ms) | Aceleração vs. laço |
|---|---:|---:|
| Laço | 87,025 | 1,00× |
| Compreensão | 61,745 | 1,41× |
| `map` + lambda | 82,555 | 1,05× |
| Vetorizado | 1,382 | 62,97× |

A maior diferença observada foi entre a lista e os arrays compactos: a lista guarda referências para objetos Python e cada inteiro também é um objeto com seu próprio custo. Já os arrays NumPy guardam os valores em uma região contígua com tamanho fixo por elemento. A multiplicação em `uint16` transborda porque o tipo só representa valores até 65535: o resultado matemático `4095 × 20 = 81900` é reduzido módulo 65536, resultando em `16364`. Para contagens de 0 a 4095, escolheria `uint16`. Para pressões em kPa, escolheria `float64` para preservar precisão nos cálculos (ou `float32` se a memória fosse a prioridade e a precisão fosse suficiente).

### R6 — Tipos da `SerieTemporal`

| Expressão | Tipo obtido |
|---|---|
| `s + s` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` |
| `s.sum()` | `SerieTemporal` |
| `s[0]` | `float64` |

O resultado mais surpreendente é `s.sum()`: embora a soma produza um único valor, a subclasse `numpy.ndarray` propaga o tipo da subclasse em algumas operações. Já a indexação por um único índice retorna um escalar NumPy (`float64`), e não uma série.

### R7 — Issue #4

O sintoma era receber 570 valores ao calcular a média móvel de 30 pontos de uma série com 600 leituras, embora o contrato exija `600 - 30 + 1 = 571`. Os testes de regressão são `test_regressao_media_movel_janela_1` e `test_regressao_media_movel_janela_completa`. A causa estava na diferença entre fatias da soma acumulada: `acumulada[janela:] - acumulada[:-janela]` perde a primeira janela porque não existe um zero inicial representando a soma anterior ao primeiro elemento. A correção foi acrescentar esse zero à soma acumulada e calcular a diferença entre prefixos, preservando as `n - janela + 1` janelas. Os testes de aceitação originais verificavam o tipo de retorno e os erros para janelas inválidas, mas não verificavam a quantidade nem os valores da média móvel. Um caso adicional não coberto era `janela == 1`, coberto pelo teste `test_regressao_media_movel_janela_1`.

## Marco 2 — Medição

### Ambiente

C:\Users\carol\AppData\Local\Programs\Python\Python314\python.exe
Python 3.14.3 | NumPy 2.5.5 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3463

### R8 — Derivada numérica

O erro cai de `1.658e-05` (h=1) até `6.224e-10` (h=1e-5), pois o erro de truncamento da diferença adiante diminui com h. Para passos menores, o cancelamento e o arredondamento em ponto flutuante passam a dominar, fazendo o erro crescer. Em `h=1e-14`, `1000 + h == 1000`: o numerador fica zero, a derivada aproximada é zero e o erro absoluto vira a própria derivada exata (`0.213432888873`).

### R9 — Issue #7

Os testes de regressão são `test_kahan_milhao_de_decimos` e `test_kahan_preserva_parcelas_pequenas`. Ambos falharam antes da correção. A expressão `t - (s + y)` refaz a mesma soma arredondada que produziu `t`, portanto a subtração resulta em zero. A forma `(t - s) - y` calcula primeiro a diferença entre o total arredondado e a soma anterior, preservando o resíduo que representa a parcela perdida. Os testes de aceitação só somavam dez parcelas de `0.1` e usavam tolerância, caso em que o erro era pequeno demais para revelar o defeito.

### R10 — Precisão × exatidão

Os desvios foram praticamente iguais: `0.540 kPa` na curva linear e `0.541 kPa` na spline. Portanto, a dispersão (precisão) é semelhante. Porém, os vieses foram `-1.871 kPa` e `-0.042 kPa`, respectivamente: a curva spline é muito mais exata em relação à referência. A média de muitas leituras reduz o efeito de variações aleatórias, mas não corrige um erro sistemático introduzido pelo modelo linear de calibração.

## Marco 3 — Raízes e interpolação

### Ambiente

C:\Users\carol\AppData\Local\Programs\Python\Python314\python.exe
Python 3.14.3 | NumPy 2.5.5 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3463

### R11 — Bissecção × Newton

A bissecção faz 44 iterações porque reduz sempre pela metade o intervalo inicial de largura 13; para chegar a menos de `1e-12`, precisa de `k` tal que `13/2^k < 1e-12`. O Newton fez 5, 4 e 3 iterações para Re de `1e4`, `1e5` e `1e6`, respectivamente. Ordem 2 significa que o erro seguinte é aproximadamente proporcional ao quadrado do erro atual: os dígitos corretos crescem rapidamente. Newton pode falhar se a derivada for nula ou se a tangente levar a uma região inadequada; a bissecção ainda converge quando há troca de sinal no intervalo.

### R12 — Issue #9

Os testes de regressão são `test_raiz_quadrada_de_dois_converge_em_poucas_iteracoes`, `test_derivada_numerica_e_reavaliada_no_ponto_atual` e `test_colebrook_re_1e4_converge_rapidamente`. Antes da correção, Colebrook em Re=`1e4` exigia 10 iterações (o teste limita a 6) e a derivada era avaliada uma única vez. Com derivada fixa no ponto inicial, Newton vira uma iteração de ponto fixo, cuja convergência em geral é linear. Recalculando `f'(x)` em cada aproximação, recupera-se a convergência quadrática local. Os testes de aceitação antigos verificavam a raiz, não a velocidade nem a quantidade de avaliações da derivada.

## Marco 4 — Ajuste e integração

### Ambiente

C:\Users\carol\AppData\Local\Programs\Python\Python314\python.exe
Python 3.14.3 | NumPy 2.5.5 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3463

### R13 — Integração e descontinuidade

Ao integrar o custo de uma vez, a tarifa muda bruscamente em 18 h e 21 h, quebrando a hipótese de suavidade das regras. A ordem observada cai (1,00 no trapézio e 0,65 no Simpson). Separando as três faixas, cada integral tem tarifa constante e a função fica suave, recuperando as ordens 2 e 4. A etapa 1 também confirmou as ordens 2,01 e 4,06 para a demanda suave.

### R14 — Issue #11

Os testes `test_trapezio_linear_em_malha_irregular` e `test_trapezio_usa_largura_de_cada_intervalo` falharam antes da correção. O defeito usava apenas o primeiro passo para todos os trapézios. A correção soma cada largura vezes a média das duas ordenadas. A aceitação não detectava isso porque não testava uma tabela irregular. Simpson não serve ao registro porque exige malha uniforme e número ímpar de pontos; o SCADA tem lacunas de 30 min.

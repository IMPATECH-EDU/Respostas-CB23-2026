# Relatório — 3494

## Marco 1

### Ambiente

C:\Users\sdani\AppData\Local\Python\pythoncore-3.14-64\python.exe
Python 3.14.2 | NumPy 2.4.4 | fornecido 4.0

### R1 — Expressões regulares

A string `PT101abc` é aceita por `re.match(r"[A-Z]{1,2}\d{1,3}", ...)`, pois o padrão encontra o prefixo `PT101`. `re.fullmatch` rejeita a string porque sobram caracteres depois da tag. Se `valida_tag` usasse `match`, aceitaria indevidamente tags com sufixos.

### R2 — Linhas inválidas

`ler_log` devolve as linhas inválidas para que falhas de comunicação, truncamentos e mensagens malformadas possam ser contabilizados e investigados. Ignorá-las silenciosamente poderia esconder, por exemplo, uma perda recorrente de comunicação com um transmissor.

### R3 — Late binding

Na compreensão original, a lambda consulta `k` quando é chamada. Nesse momento o laço já terminou e `k` contém o último fator (`0,1`, de FT201). Por isso `errados["PT102"](4095)` resulta em 409,5. Em `criar_conversores`, o argumento padrão `fator=fator` fixa o valor de cada iteração na criação da lambda.

### R4 — Escala nominal

A escala linear nominal produz aproximadamente 261,97 kPa, enquanto a conferência é 380 kPa. A hipótese é que o transmissor não tem resposta linear. Isso aparece em `fornecido/simulador.py`, na função `p_real`, que usa uma resposta senoidal, por isso uma curva construída com os pontos de calibração representa melhor a resposta real do que a escala nominal.

### R5 — Previsão × medição

| Conversão | Tempo medido (ms) |
|---|---:|
| Laço | 72,986 |
| Compreensão | 63,559 |
| `map` + lambda | 85,133 |
| Vetorizado | 0,823 |

Nesta execução, `map` com lambda ficou mais lento que o laço. O custo das chamadas de função e a materialização do iterador podem explicar a diferença. `uint16` guarda contagens de 0 a 4095 com folga. Ao multiplicar 4095 por 20 em `uint16`, 81900 excede 65535 e sofre retorno modular. Para pressões em kPa, usaria `float32` se a precisão disponível for suficiente e `float64` quando o cálculo exigir mais precisão.

### R6 — Tipos da `SerieTemporal`

| Expressão | Tipo observado |
|---|---|
| `s + s` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` |
| `s.sum()` | `SerieTemporal` |
| `s[0]` | `float64` |

O resultado que mais me surpreendeu foi o de `s.sum()`. Por ser uma subclasse de `numpy.ndarray`, a operação preserva a subclasse e devolve um array de dimensão zero, em vez de um escalar Python convencional. A indexação de um elemento, por outro lado, devolve `numpy.float64`.

### R7 — Issue #4

Os testes de regressão são `test_media_movel_tem_n_menos_janela_mais_um_resultados` e `test_media_movel_com_janela_igual_ao_tamanho`. O código original subtraía fatias de `cumsum` sem incluir o zero inicial, calculando `n − janela` resultados em vez de `n − janela + 1`. A correção acrescentou zero ao início da soma acumulada e manteve as operações vetorizadas do NumPy. O teste foi executado temporariamente contra a fórmula original e falhou. Os testes de aceitação verificavam o tipo e a validação da janela, mas não a quantidade e os valores de todas as janelas. Os testes `test_reamostrar_descarta_sobra_final` e `test_ler_log_conta_data_impossivel_como_invalida` cobrem, respectivamente, a sobra de pontos e uma data impossível.

## Marco 2

### Ambiente

C:\Users\sdani\AppData\Local\Python\pythoncore-3.14-64\python.exe
Python 3.14.2 | NumPy 2.4.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3494

### R8 — Derivada numérica

Quando `h` diminui de 1 até aproximadamente `10⁻⁵`, o erro de truncamento da diferença adiante diminui. Para passos ainda menores, o arredondamento e o cancelamento passam a dominar e o erro volta a crescer. Em `h = 10⁻¹⁴`, somar `h` a `x = 1000` não altera o número representado (`1000 + 10⁻¹⁴ == 1000`), o numerador da diferença fica zero e a derivada aproximada é zero. O erro absoluto torna-se a derivada exata, aproximadamente 0,213432888873.

### R9 — Issue #7

Os testes de regressão são `test_kahan_compensa_muitas_parcelas_de_decimo` e `test_kahan_tem_erro_menor_que_soma_ingenua`. A expressão original `t - (s + y)` refazia a soma já arredondada e resultava em zero, assim, a compensação não armazenava a parte perdida. A forma correta é `(t - s) - y`. Os testes de aceitação somavam poucas parcelas, situação em que o erro é pequeno demais para revelar o defeito, os testes novos usam muitas parcelas. O teste principal foi executado contra a expressão original e falhou com erro de aproximadamente 1,33×10⁻⁶.

### R10 — Precisão × exatidão

Para PT102, a curva linear produziu média de aproximadamente 378,2 kPa, desvio 0,536 kPa e viés −1,840 kPa. A spline produziu aproximadamente 380,0 kPa, desvio 0,537 kPa e viés −0,010 kPa. Os desvios praticamente iguais indicam precisão semelhante. Os vieses diferentes mostram que a spline é mais exata em relação ao valor de referência. Aumentar o número de leituras reduz a incerteza aleatória da média, mas não elimina o viés sistemático introduzido pela curva linear.

## Marco 3

### Ambiente

C:\Users\sdani\AppData\Local\Python\pythoncore-3.14-64\python.exe
Python 3.14.2 | NumPy 2.4.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3494

### R11 — Bissecção × Newton

A bissecção usa o mesmo intervalo inicial e a mesma tolerância. A cada iteração reduz a largura pela metade. Por isso, para os parâmetros usados na Etapa 2(a), precisou de 44 iterações independentemente do Reynolds. Ordem 2 significa que, perto da raiz e sob as hipóteses do método, o erro seguinte é aproximadamente proporcional ao quadrado do erro atual. Newton pode falhar se a derivada for nula ou o chute levar a uma sequência divergente. A bissecção continua funcionando quando há continuidade e mudança de sinal no intervalo.

### R12 — Issue #9

Os testes de regressão são `test_newton_recalcula_derivada_a_cada_iteracao` e `test_newton_converge_quadraticamente_em_raiz_simples`. O código original calculava `f'` apenas no ponto médio inicial e a mantinha fixa, transformando a atualização em uma iteração de inclinação constante, com convergência linear. A correção recalcula a derivada em cada aproximação. Os testes de aceitação verificavam se o método chegava à raiz dentro do limite máximo de iterações, mas não exigiam poucas iterações nem verificavam chamadas repetidas da derivada. Contra a versão original, o teste de chamadas da derivada falha porque ela é calculada somente uma vez.

## Marco 4

### Ambiente

C:\Users\sdani\AppData\Local\Python\pythoncore-3.14-64\python.exe
Python 3.14.2 | NumPy 2.4.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3494

### R13 — Integração e descontinuidade

A tarifa muda bruscamente às 18 h e às 21 h. Ao integrar o custo do dia como uma única função, a regra atravessa pontos de descontinuidade, reduzindo a ordem observada: aproximadamente 1,00 para o trapézio e 0,65 para Simpson. Ao separar a integral nos limites das faixas, cada trecho tem tarifa constante e a função fica suave por partes. As ordens observadas voltam a aproximadamente 2 e 4, respectivamente.

### R14 — Issue #11

Os testes de regressão são `test_integracao_tabela_irregular_linear` e `test_integracao_tabela_irregular_com_mais_lacunas`. O código original usava a primeira largura `x[1]−x[0]` em todos os trapézios, embora a perda de oito leituras produza intervalos de 15 e 30 minutos. A correção soma as áreas locais usando cada `np.diff(x)`. Os testes de aceitação usavam malhas uniformes e não revelavam o defeito. Contra a versão original, o teste linear da malha irregular retornou 7 em vez de 12. Simpson não serve para o registro do dia porque a implementação em tabela exige pontos igualmente espaçados. A malha real é irregular.
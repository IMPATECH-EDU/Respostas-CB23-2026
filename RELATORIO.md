# Relatório — Enrico Ferraroni Maiali (3528)

IMPA Tech · Programação 2 · Professor Emilio Vital Brazil · Período 1.2  
E-mail: al.enrico.maiali@impatech.edu.br · GitHub: enrico-impatech

## Marco 1

### Ambiente

Execução em Linux, com ambiente `venv` fora do repositório, criado com
`--system-site-packages` para aproveitar as bibliotecas instaladas no ambiente de execução.
Saída de `which python`, com o ambiente ativado, e da Etapa 0:

```text
/workspace/scratch/373109ec75cb/venv/bin/python
=== Etapa 0: ambiente ===
Python 3.12.14 | NumPy 2.3.5 | fornecido 4.0
```

### R1 — Expressões regulares

`PT101extra` é aceita por `re.match(r"[A-Z]{1,2}[0-9]{1,3}", ...)`, pois o prefixo `PT101` casa.
`re.fullmatch` rejeita a string porque ainda sobram caracteres.
Usar apenas `match` em `valida_tag` permitiria identificadores malformados, incluindo `PT1010`.

### R2 — Linhas inválidas

A execução teve 2.404 registros válidos e 4 linhas inválidas, conservadas para diagnóstico.
Se uma falha de comunicação interrompesse as leituras de pressão, descartá-las silenciosamente
poderia fazer um intervalo sem informação parecer operação normal.
Devolver o texto original permite localizar a falha e distinguir ausência de dados de ausência de alarmes.

### R3 — Late binding

As lambdas da versão errada consultam a mesma variável `k` quando são chamadas.
Ao terminar a compreensão, `k` vale `0.1`, o fator de FT201; portanto, `4095 * 0.1 = 409.5`.
Em `criar_conversores`, o argumento padrão `fator=fator` guarda o valor de cada iteração.
Assim, o conversor de PT102 usa `600/4095` e devolve `600.0` para 4.095 contagens.

### R4 — Escala nominal

A pressão nominal foi `261.966448 kPa`, contra `380.000000 kPa` de conferência.
A hipótese é que a relação entre contagens e pressão não seja linear.
Em `fornecido/simulador.py`, `p_real(c)` usa `600*sin(π*c/(2*4095))`; `c_real` usa a inversa.
A calibração deve representar essa resposta, em vez de supor uma reta entre os extremos.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit local `96abf35`, antes da implementação e da medição.
Os tempos correspondem a uma execução com um milhão de contagens e dez repetições por método.

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 vezes | 18,000028 vezes |
| Tempo do laço / tempo vetorizado | 30 vezes | 83,373649 vezes |
| Tempo da compreensão / tempo do laço | 0,8 | 0,935300 |

| Estrutura | Bytes por elemento | Bytes totais | Bytes / bytes da lista |
| --- | ---: | ---: | ---: |
| `list` | 36,000056 | 36.000.056 | 1,000000 |
| `array('H')` | 2 | 2.000.000 | 0,055555 |
| `uint16` | 2 | 2.000.000 | 0,055555 |
| `int32` | 4 | 4.000.000 | 0,111111 |
| `int64` | 8 | 8.000.000 | 0,222222 |
| `float32` | 4 | 4.000.000 | 0,111111 |
| `float64` | 8 | 8.000.000 | 0,222222 |

| Método | Tempo médio (ms) | Aceleração em relação ao laço |
| --- | ---: | ---: |
| Laço | 65,393480 | 1,000000 |
| Compreensão | 61,162551 | 1,069175 |
| `map` + lambda | 75,553656 | 0,865524 |
| Vetorizado | 0,784342 | 83,373649 |

A maior diferença foi a aceleração: o NumPy evita o custo de executar operações e criar floats no laço Python.
Ela foi maior que a prevista; tempos também dependem da máquina e de sua carga, portanto não são constantes universais.
Em `uint16`, `4095*20 = 81900` ultrapassa 65535 e resulta em `81900 mod 65536 = 16364`.
Usaria `uint16` para armazenar contagens de 12 bits e `float64` para pressões e cálculos intermediários.
A conversão vetorizada promove os dados para `float64` antes de multiplicar, evitando esse estouro.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

A previsão que não se confirmou foi `s.sum()`: a redução preserva a subclasse em um array de dimensão zero.
Embora represente um único número, seu tipo é `SerieTemporal`; `float(s.sum())` extrai o escalar Python.
Já a indexação de um elemento, `s[0]`, devolve diretamente um escalar `float64`.

### R7 — Issue #4

O sintoma era receber 570 médias de janela 30 para 600 pontos, em vez de 571.
`test_primeira_janela_preservada` detecta a perda da primeira janela; `test_janela_igual_serie` detecta o resultado vazio.
A soma acumulada começava em `s[0]`, sem o prefixo zero necessário para representar a primeira soma de janela.
Acrescentei esse zero antes de subtrair os prefixos; o resultado mantém `SerieTemporal` e não altera a entrada.
A aceitação verificava tipo, erros e imutabilidade, mas não o comprimento nem os valores das médias.
Outro extremo ausente na aceitação é janela 1, coberto por `test_janela_unitaria`.

## Marco 2

### Ambiente

```text
=== Etapa 0: ambiente ===
Python 3.12.14 | NumPy 2.3.5 | SciPy 1.17.0 | fornecido 4.0 | matrícula 3528
```

### R8 — Derivada numérica

O erro caiu de `1.658e-5`, com `h=1`, para `6.224e-10`, com `h=1e-5`, pois diminuiu o truncamento da diferença adiante.
Com passos ainda menores, o arredondamento e o cancelamento na subtração passam a dominar, amplificados pela divisão por `h`.
Em `h=1e-14`, o float de `1000 + 1e-14` é o próprio `1000`, então o numerador é zero.
A derivada aproximada fica zero e o erro absoluto é `0.213432888873`, o módulo da derivada exata.

### R9 — Issue #7

As regressões são `test_pulsos_decimais` e `test_parcelas_menores_que_ulp`.
Como `t` já recebeu a soma arredondada `s + y`, repetir a mesma soma em `t - (s + y)` subtrai valores idênticos e zera a correção.
Em `(t - s) - y`, os parênteses mudam a sequência de arredondamentos e permitem recuperar a parcela perdida.
A aceitação somava apenas dez parcelas e usava `math.isclose`, tolerando o erro minúsculo da soma ingênua.
Com um milhão de parcelas, Kahan devolveu `100000.0 L`; a soma ingênua errou `1.333e-6 L`.

### R10 — Precisão × exatidão

Para PT102, os desvios foram `0.560 kPa` (linear) e `0.561 kPa` (spline): dispersões quase iguais, portanto precisões semelhantes.
Os vieses foram `-1.844 kPa` e `-0.014 kPa`, respectivamente; a spline ficou mais próxima da referência e foi mais exata.
Depois de excluir cinco espúrias, restaram 595 leituras, mas a média reduz o erro aleatório, não o erro sistemático da interpolação.
A altura com spline foi `35.74 ± 0.22 m`, compatível com a referência de `35.749 m`.

## Marco 3

### R11 — Bissecção × Newton

Colebrook usa sempre `[2,15]` e tolerância `1e-12`: são `ceil(log2(13/1e-12)) = 44` divisões, independentemente do Reynolds.
Para Re = 10⁴, Newton precisou de 5 iterações; seus erros passaram por `5.0e-2`, `2.3e-5` e `5.0e-12`, dando ordem estimada `2.00`.
Ordem 2 significa que, perto de uma raiz simples, o próximo erro é aproximadamente proporcional ao quadrado do anterior.
Newton pode falhar por derivada nula: para `f(x)=x³-1` em `[-2,2]`, o ponto inicial é zero e `f'(0)=0`.
A bissecção funciona nesse intervalo porque a função é contínua e há troca de sinal.

### R12 — Issue #9

As regressões são `test_derivada_analitica_atualizada` e `test_derivada_numerica_atualizada`, ambas com limite de seis iterações.
O código congelava a derivada no ponto inicial; perto da raiz, sobrava em geral um termo linear no erro, em vez do cancelamento de Newton.
Mover a avaliação da derivada para dentro do laço restaura sua atualização em cada aproximação.
A aceitação conferia convergência e valor final, mas permitia até 100 iterações e não verificava a ordem.
As ordens observadas para Colebrook foram `2.00`, `1.98` e `2.00`; o ponto com spline foi `64.910 L/s` e `35.761 m`.

## Marco 4

### R13 — Integração e descontinuidade

O salto da tarifa viola as hipóteses de suavidade necessárias às ordens 2 e 4; o intervalo que atravessa o salto pode dominar o erro.
Na execução, integrar o dia de uma vez deu ordem `1.00` no trapézio e `0.65` em Simpson, não exatamente 1 para este último.
A posição dos saltos em relação às malhas também afeta essa estimativa com poucos valores de `n`.
Separar as faixas mantém a tarifa constante em cada integral e recuperou ordens `2.00` e `4.00`.
Para `n=110`, os erros por faixa foram `6.3e-4` e `8.1e-8`, respectivamente.

### R14 — Issue #11

As regressões são `test_constante_com_lacunas` e `test_reta_com_primeiro_intervalo_largo`.
O defeito aplicava a largura do primeiro intervalo a todos os trapézios; a correção usa `np.diff(x)` em cada área.
A aceitação testava o trapézio apenas em malhas uniformes, nas quais a hipótese incorreta não altera o resultado.
O registro teve 89 leituras e intervalos de 15, 30 e 45 minutos, incompatíveis com a exigência de malha uniforme do Simpson fornecido.
O balanço foi `3896.28 m³`, `655.42 kWh` e `R$ 416.13`, com erros relativos de `0.21%`, `0.02%` e `0.03%`.
O ajuste usa `np.polynomial.polynomial.polyfit`, que resolve mínimos quadrados e entrega os coeficientes na ordem crescente exigida.

## Verificação dos marcos 1 a 4

- `python -m unittest discover -v`: 91 testes aprovados, incluindo 37 testes novos, além dos quatro exemplos e dos 50 de aceitação.
- `python marco1.py` a `python marco4.py`: todos os asserts passaram com matrícula 3528.
- As nove regressões foram executadas e falharam antes das correções, no commit local `6d2c26f`.
- `fornecido/`, `README.md`, os enunciados, `calibracao.py` e `marco2.py` a `marco4.py` foram preservados em relação ao ZIP recebido.
- O material recebido não contém um enunciado específico do Fechamento; esta versão cobre integralmente os quatro marcos disponíveis.

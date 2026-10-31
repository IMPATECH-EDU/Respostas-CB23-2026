# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
/opt/anaconda3/envs/ambiente_aluno/bin/python

=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.3 | fornecido 1.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
A string "EX248!" é aceita por re.match, uma vez que sua forma satisfaz a regra de começar com uma ou duas letras maiúsculas seguidas por 1,2 ou 3 números. No entanto, re.full.match a rejeitaria, pois possui um caractere "!" que está além das regras.
Como consequência, vê-se que re.fullmatch é mais restritivo e garante a padronização de tags, enquanto que re.match permitiria adições aleatórias no final e comprometeria a organização interna ao não garantir o padrão esperado.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
ler_log devolve as linhas descartadas para que seja possível analisar defeitos de comunicação ou dados corrompidos no monitoramento do sistema. Um exemplo realista em que isso é pertinente seria o caso de uma unidade perder contato com o sistema e passar a não conseguir produzir respostas válidas.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
O resultado final é 409,5 porque a função lambda só é chamada posteriormente, utilizando como fator de multiplicação do argumento c não pelo fator associado a cada item de "escalas", mas pelo último com que terminou o ciclo de criação de "errados": 0,1.

A implementação resolve o problema utilizando um argumento padrão que avalia e liga o valor de `fator` no momento exato da definição da função, preservando o fator individual de cada tag.
### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
A discrepância surge pela diferença entre a escala senoidal do medidor real e a linear utilizada no cálculo da nominal

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18.000028 |
| Tempo do laço / tempo vetorizado | 20 | 19.20 |
| Tempo da compreensão / tempo do laço | 0.7 | 0.86 |

2351a64
<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
A multiplicação direta de $4095 \times 20$ dá $81900$, que excede o limite máximo suportado. Quando ocorre um estouro no NumPy, o valor equivale a tirar o resto da divisão por $65536$, retornando $16364$.
O tipo a ser escolhido deve ser o uint16, pois os valores utilizados encontram-se dentre do intervalo de 0 a 4095, dentro dos limites do uint16 sem desperdiçar memória.

Não houve uma grande discrepância entre o previsto e o obtido, mas a maior, que foi a razão de tempo da compressão pelo tempo do laço, mas podem ser explicadas por processos computacionais internos. A discrepância na memória pode ser explicada pela necessidade de ocupar memória para outros processos além de somente os ponteiros e dados da lista, como o cabeçalho e outros dados da estrutura interna da lista. As discrepâncias nas razões dos tempos, por outro lado, são um pouco maiores por dercorreram de chutes menos precisos, baseados apenas no conhecimento teórico da otimização de cada implementação, mas passíveis de alteração devido à natureza dinâmica e inconstante do tempo de execução.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | Float64 | SerieTemporal |
| `s[0]` | Float64 | Float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
O fato de que s.sum() é do tipo SerieTemporal e não float64. 

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
O sintoma era que media_movel(30) retornava 570 valores para uma série de 600 pontos, quando deveria retornar 571. O teste de regressão test_media_movel_quantidade_correta detecta esse erro. A causa era o uso de acumulada[janela:] - acumulada[:-janela], que descartava uma média válida. Corrigi o problema acrescentando zero ao início da soma acumulada e usando acumulada[janela-1:] no primeiro termo da subtração. Os testes de aceitação não detectaram o defeito porque não cobriam esse caso: detectam se há tipo de retorno adequado, se levanta ValueError em caso de janela maior do que o tamanho da lista e se algumas operações mantêm o tipo SerieTemporal. Além disso, testei uma janela igual a 1 (test_media_movel_janela_um) e uma janela igual ao tamanho da série (test_media_movel_janela_igual_tamanho), casos que verificam os limites da operação.



## Marco 2

### Ambiente

=== Etapa 0: ambiente ===
Python 3.14.3 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 3.0 | matrícula 3519

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

O erro diminui de $h=1$ até $h \approx 10^{-5}$ porque é dominado pelo erro de truncamento ($O(h)$ da série de Taylor), que reduz à medida que $h$ diminui; a partir desse ponto, o erro de arredondamento passa a dominar devido ao cancelamento catastrófico na subtração $f(x+h) - f(x)$ amplificado pela divisão por $1/h$. Por fim, em $h = 10^{-14}$, a limitação de precisão do ponto flutuante de 64 bits faz com que $1000.0 + 10^{-14} == 1000.0$, zerando o numerador e resultando em uma derivada numérica igual a $0.0$, o que torna o erro absoluto exatamente igual ao valor da própria derivada exata ($|0.0 - f'(x)| = f'(x)$).

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->
### R9 — Issue #7

**Testes de regressão:** `test_kahan_soma_de_pequenos` e `test_kahan_pequeno_com_grande`.

**Causa:** No código original, a correção era calculada como `self._correcao = t - (self._soma + y)`. Como `t` havia acabado de ser definido como `self._soma + y`, os parênteses faziam o Python reavaliar essa soma primeiro, resultando em `t - t = 0.0`. Sem a ordem correta das operações `(t - self._soma) - y` para isolar a perda de precisão, a correção zerava e o algoritmo se comportava exatamente como o `AcumuladorIngenuo`.

**Testes de aceitação:** O teste de aceitação original totalizava apenas 10 parcelas de `0.1` [2]. Com poucas iterações, o erro acumulado em ponto flutuante de 64 bits é ínfimo e cai dentro da tolerância do `math.isclose`. O defeito só se torna visível em somas de grande escala (como $10^6$ ou $10^7$ parcelas) ou ao somar parcelas minúsculas a um acumulador grande.
### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->


A precisão (medida pelo desvio padrão) reflete a dispersão aleatória das leituras e é praticamente idêntica em ambos os modelos (~0,54 kPa), pois alterar a curva não altera o ruído do sensor; já a exatidão (medida pelo viés) é significativamente superior na spline (viés de -0,005 kPa contra -1,835 kPa na linear), pois ela se ajusta à resposta física não linear do transmissor. Tirar a média de 600 leituras reduz apenas as flutuações aleatórias do sinal, mas não elimina o erro sistemático (viés) do modelo linear — a média simplesmente faz a medição convergir com alta precisão para o valor incorreto do modelo.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

A Bissecção reduz a largura do intervalo rigorosamente pela metade a cada passo ($\frac{b - a}{2^k}$), dependendo exclusivamente da largura inicial ($13$) e da tolerância ($\text{tol} = 10^{-12}$). A chance de um ponto médio racional acertar exatamente a raiz e encerrar o laço antes do tempo é praticamente nula. Sem essa parada antecipada, o algoritmo é obrigado a dividir o intervalo até satisfazer $\frac{13}{2^k} < 10^{-12}$, o que resulta matematicamente em exatamente 44.

Ordem de convergência 2 significa que o erro no passo seguinte é proporcional ao quadrado do erro atual.

O Método de Newton falha quando encontra uma derivada nula ou próxima de zero ($f'(x_k) \approx 0$), causando divisão por zero ou arremessando o palpite para fora da região de interesse. A Bissecção não falha porque possui convergência global garantida pelo Teorema do Valor Intermediário desde que haja troca de sinal no intervalo 


### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->

Os testes de regressão criados para evidenciar a falha foram:
1. `test_convergencia`: testa a recuperação e convergência do método na função f(x) = 1 - x² no intervalo [-1, 1.9].
2. `test_newton_quantidade_iteracoes`: verifica se o número de iterações para f(x) = x² - 2 no intervalo [0, 2] é menor ou igual a 6.

Ao calcular a derivada apenas uma vez no ponto médio inicial (x₀), a fórmula aplicada passa a ser x_{k+1} = x_k - f(x_k) / f'(x₀). Isso descaracteriza o Método de Newton verdadeiro (cuja tangente é atualizada a cada ponto x_k). Como a inclinação não acompanha a variação local da função, a redução do erro passa a ser proporcional ao erro do passo anterior (e_{k+1} ≈ C · e_k), tornando a convergência puramente linear (p ≈ 1) em vez de quadrática (p ≈ 2).

Os testes de aceitação fornecidos não capturaram o defeito porque apenas verificavam se o método convergia (resultado.convergiu == True) e se o resultado final estava correto dentro da tolerância. Como o código com a derivada fixa ainda conseguia atingir a tolerância exigida antes de estourar o limite padrão de 100 iterações (levando 26 iterações em vez de 5), o teste passava sem acusar a perda de eficiência.

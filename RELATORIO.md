# Relatório — Pedro Faustino (3535)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/home/al.pedro.esteves/venvs/prog2-venv/bin/python

=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.3 | fornecido 1.0

/home/al.pedro.esteves/venvs/prog2-venv/bin/python

=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.3 | fornecido 1.0


### R1 — Expressões regulares

O `re.match` só confere se o **início** do texto bate certo com o padrão, ignorando se sobram caracteres no fim (por isso aceita `"PT1010"`). Já o `re.fullmatch` exige que a palavra inteira seja idêntica ao padrão. Se usássemos `re.match` na `valida_tag`, o sistema aceitaria tags com dígitos a mais no final por engano.

### R2 — Linhas inválidas

Devolvemos as linhas descartadas para conseguirmos ver exatamente o que falhou e corrigir erros de digitação ou bugs. No mundo real, se um sensor avariar e começar a enviar datas malucas ou dados corrompidos, apagar isso em silêncio esconderia o problema do equipamento, e os operadores não saberiam que a estação está a perder dados.

### R3 — Late binding

No código errado, a lambda não guarda o valor do `fator` na hora em que é criada; ela só vai procurar a variável quando é executada. Como o laço `for` já acabou nessa altura, ela apanha o último fator do dicionário (`0.1`), dando 409,5. Na nossa `criar_conversores`, usamos `f=fator` no argumento, o que "congela" o número certo para cada tag logo na criação.

### R4 — Escala nominal

A diferença acontece porque mudamos de números inteiros pequenos (`uint16`, de 2 bytes) para números com vírgula (`float64`, de 8 bytes) ao converter contagens em pressão real. Cada número passa a gastar 4 vezes mais memória. No código, a explicação está nas funções de conversão do `dados.py`, que transformam o array para `float64`.

### R5 — Previsão × medição (Etapa 3)

OBS: Esqueci de fazer  a separação em commits, não tenho o commit onde fiz as previsões, porem foram feitas antes.

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ~4.0x | ~4.2x |
| Tempo do laço / tempo vetorizado | ~20.0x | ~18.5x |
| Tempo da compreensão / tempo do laço | ~1.1x | ~1.05x |

A maior diferença foi entre o laço comum e o código vetorizado, porque o NumPy roda em linguagem C super rápida. O valor `uint16 * 20` dá 16364 porque ultrapassa o limite de 16 bits ($4095 \times 20 = 81900$, e ao estourar o máximo de 65535, dá a volta para 16364). Usaria `uint16` para contagens brutas para economizar espaço e `float64` para kPa pela precisão das casas decimais.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `SerieTemporal` | `np.float64` |
| `s[0]` | `SerieTemporal` | `np.float64` |

O que mais surpreendeu foi ver que, ao pegar num só elemento (`s[0]`) ou somar tudo (`s.sum()`), o resultado vira um `np.float64` comum em vez de continuar como `SerieTemporal`. Percebi que isso acontece porque o NumPy mantém a nossa classe quando trabalha com listas ou fatias, mas quando extrai um número isolado, converte-o para o tipo numérico padrão.

### R7 — Issue #4

Sintoma: a média móvel devolvia menos 1 elemento do que devia, "comendo" o primeiro bloco de dados.
Teste de regressão: `test_regressao_media_movel_tamanho`.
Causa: no `np.cumsum`, faltava um zero no início do vetor para conseguir calcular a subtração do primeiro bloco.
Correção: colocámos um zero no começo usando `np.insert(np.cumsum(self), 0, 0)`.
Os testes de aceitação não apanharam isso porque não conferiam o tamanho exato devolvido em todos os cenários. Outro caso não coberto por eles é quando a janela tem o mesmo tamanho da série toda ($k = N$), que cobrimos no `test_regressao_media_movel_valores`.

## Marco 2

### Ambiente

Python 3.14.4 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3535

### R8 — Derivada numérica

O erro diminui inicialmente porque o erro de truncamento (a aproximação matemática da fórmula) domina; à medida que $h$ diminui, a fórmula aproxima-se da definição real de limite. A partir de $h \approx 10^{-5}$, o erro de arredondamento de ponto flutuante passa a dominar, pois o computador perde precisão ao subtrair números muito próximos. 

Quando $h = 10^{-14}$, a soma $x + h$ resulta exatamente em $x$ devido ao limite de casas decimais (tal como $1000 + 10^{-14} == 1000$). Isto faz com que $f(x+h) - f(x)$ seja zero. A derivada calculada passa a ser zero, logo o erro absoluto $|0 - \text{derivada\_real}|$ é exatamente o valor da própria derivada.

### R9 — Issue #7

Os nomes dos testes de regressão criados foram `test_um_milhao_de_decimos` e `test_soma_absorvida`. 

Em ponto flutuante, a expressão `t - (s + y)` dá zero porque o Python resolve os parênteses primeiro. Como `t` foi definido na linha anterior exatamente como `s + y`, a conta torna-se literalmente $t - t$, descartando o erro de arredondamento. A forma `(t - s) - y` força a extração da diferença real armazenada, recuperando os bits perdidos. 

Os testes de aceitação não apanharam o defeito porque os logs do Marco 1 possivelmente tinham poucas leituras ou valores que não acumulavam erro suficiente para ultrapassar a tolerância dos testes (o `assertAlmostEqual`).

### R10 — Precisão × exatidão

A **precisão** refere-se à dispersão dos dados: as leituras estão próximas umas das outras, resultando num desvio padrão semelhante (baixo) para ambas as curvas. A **exatidão** é a proximidade ao valor real (viés baixo). 

A média de quase 600 leituras apenas dilui os erros aleatórios (melhora a precisão), mas o viés da curva linear é um erro sistemático inerente ao modelo matemático. A curva linear desloca sistematicamente todos os pontos para longe do valor verdadeiro, e nenhuma quantidade extra de dados consegue corrigir esse desvio central.

## Marco 3

### R11 — Bissecção × Newton

A bissecção gasta sempre 44 iterações independentemente do número de Reynolds porque o seu avanço baseia-se unicamente na geometria do intervalo. A cada passo, o intervalo é dividido exatamente ao meio. Logo, o número de iterações necessárias para atingir a tolerância depende apenas da largura do intervalo inicial ($b - a$) e da tolerância ($tol$), seguindo a relação $n \approx \log_2(\frac{b-a}{tol})$. O formato da curva ou os parâmetros físicos da função não alteram este cálculo matemático.Uma ordem de convergência 2 (quadrática) significa que, assim que o método se aproxima da raiz, o erro de cada iteração é proporcional ao quadrado do erro da iteração anterior ($e_{k+1} \approx C \cdot e_k^2$). Na prática, isto traduz-se na duplicação do número de casas decimais corretas a cada passo: um erro de $10^{-3}$ cai para $10^{-6}$, e depois para $10^{-12}$.O método de Newton falha e a bissecção funciona em cenários onde a função possui um ponto de inflexão com derivada nula (causando divisão por zero no Newton) ou quando a inclinação tangencial é tão horizontal que atira a próxima estimativa para fora do domínio (causando erros de avaliação). A bissecção é imune a tangentes cegas e garante a raiz desde que o intervalo inicial contenha uma troca de sinal.

### R12 — Issue #9

Os testes de regressão elaborados para expor a falha foram o test_newton_itera_rapido e o test_newton_ordem_quadratica (além dos testes de fronteira test_newton_foge_do_intervalo e test_newton_derivada_nula).Ao calcular a derivada apenas uma vez (no ponto inicial), o método de Newton perde a sua característica fundamental: a adaptação iterativa à curvatura local. Ao usar uma inclinação constante, o algoritmo transforma-se numa variante do método das cordas (ou Newton modificado). Sem a atualização da reta tangente para o ponto $x_k$ atual, o salto em direção à raiz deixa de ser otimizado, e o erro passa a decrescer apenas por um fator constante a cada passo (convergência linear).Os testes de aceitação não detetaram o defeito porque avaliavam exclusivamente o valor final devolvido pelo método. Eles garantiam que o resultado numérico estava correto e dentro da tolerância, mas não inspecionavam o percurso feito para lá chegar (como o contador de iterações da resposta ou o histórico de erros). Um método lento que chegue ao resultado certo passará sempre num teste que avalia apenas o destino e ignora a viagem.
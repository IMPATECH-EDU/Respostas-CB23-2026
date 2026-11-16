# Relatório — João Batista de Sousa Silva (3500)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

D:\Projetos\IMPATech\Programacao_2\Respostas-CB23-2026\.venv\Scripts\python.exe

=== Etapa 0: ambiente ===
Python 3.12.10 | NumPy 2.5.3 | fornecido 1.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

" PT101", é aceita por re.match, pois a expressão regular "[A-Z]{1,2}\d{1,3}" é encontrada. Porém, re.fullmatch a rejeita, pois é verificado se a string inteira corresponde a expressão regular, e um caractere em branco no começo torna a string incompatível com o padrão.
Se valida_tag usasse match, aceitaria strings que apenas começam com uma tag válida, como "PT101X" ou "PT1015", e tags inválidas passariam como válidas.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
ler_log devolve as linhas inválidas para que não se perca a informação de que há sensores defeituosos.
Descartar em silêncio as linhas inválidas impossibilita a verificação da integridade total das informações recebidas.

Podemos exemplificar com uma situação em que um sensor se desconecta.
Várias linhas, como "### falha de comunicacao com a RTU ###", serão registradas no log, porém, caso o leitor de log apenas ignore todas elas, ninguém saberá do problema e o mesmo poderá não ser resolvido.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Ao implementar a função lambda como (`lambda c : c \* k`), a variável c será parâmetro de lambda, mas a variável k - que não é parâmetro - será a que estiver definida no escopo e no momento em que a função for chamada.
O laço for modifica a variável k a cada iteração, e na última volta o valor de k fica definido como 0.1, pelo que a função lambda fará 4095 \* 0,1 e isso dá 409,5.

A função criar_conversores não possui esse problema, porque cria lambda's como (`lambda c k_=k: c * k_`).
Dessa forma, o valor de k estará definido no dentro do escopo da função lambda, e não no escopo externo.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
Hipótese: a resposta do transmissor não é linear, mas a escala nominal (c * 600 / 4095) supõe uma reta entre 0 e 4095 contagens.
A explicação está em 'fornecido/simulador.py', na função p_real (linha 33), que define a resposta verdadeira como 600 * sin(0.5 * pi * c / 4095).
Como o seno fica acima da reta nesse intervalo, a escala nominal subestima a pressão: as contagens que correspondem a 380 kPa (cerca de 1788) dão só cerca de 262 kPa na escala nominal.
O valor de conferência vem de PRESSAO_RECALQUE = 380.0, na linha 25 do mesmo arquivo.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 5a436f9

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 14 | 18 |
| Tempo do laço / tempo vetorizado | 14 | 22.17 |
| Tempo da compreensão / tempo do laço | 1 | 0.67 |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

A maior diferença entre previsão e medição está em tempo do laço / tempo vetorizado. O NumPy é muito mais otimizado para operações em sequência, pois está implementado em baixo nível em C compilado, e não precisa passar pelo interpretador do Python.
O NumPy também utiliza setores contíguos na memória, o que deixa o acesso mais eficiente, pois elimina a necessidade de buscar por uma referência.

O uint16 armazena os números em 16 bits, sem indicar se é positivo ou negativo; portanto, pode armazenar de 0 até 2^(16)-1 = 65535.
Como 4095 \* 20 dá 81.900, que ultrapassa o limite, acontecerá o erro de overflow e o valor armazenado será 81900 − 65.536 = 16364.

Para as contagens eu escolheria 'uint16', pois são inteiros de 0 a 4095 e cabem em 2 bytes cada. Para as pressões em kPa, escolheria 'float32', pois a conversão das contagens em kPa gera números decimais (floating points) e a precisão de 32 bits já é suficiente para armazenar os valores que serão resultados da precisão do sensor.
O float64 utilizaria muito mais espaço sem necessidade.

### R6 — Tipos da SerieTemporal (Etapa 4d)

Previsões registradas no commit: baffd37

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | np.ndarray | SerieTemporal |
| `s[1:]` | np.ndarray | SerieTemporal |
| `s * 2` | np.ndarray | SerieTemporal |
| `s.sum()` | np.int64 | SerieTemporal |
| `s[0]` | np.int64 | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->

Quase todos os resultados me surpreenderam. Todas as operações analisadas são herdadas de ndarray, do NumPy, e todas são out-of-place, pois retornam um novo objeto como resultado da operação, sem modificar os objetos de entrada.

Como uma implementação do NumPy retornou um objeto SerieTemporal, suponho que por baixo dos panos esteja sendo criado uma cópia da instância passada como parâmetro, e as modificações sejam feitas in-place nessa cópia.

De acordo com a biblioteca do NumPy, é usado um método `ndarray.__array_wrap__(array, [context, [return_scalar, ]]/)`, que retorna uma visualização array com o mesmo tipo que o próprio objeto.

O resultado que mais me surpreendeu é `s.sum()` retornar um array de dimensão zero do tipo SerieTemporal.
Em todos os casos, o tipo do resultado depende de como foi feita a implementação da operação no NumPy.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

Observação: Abaixo, indice tem contagem iniciando em 0, e posição tem contagem iniciando em 1.

A função media_movel de SerieTemporal, recebe um array, digamos que de tamanho n, e um valor k inteiro que será o tamanho da janela da média.

Essa função deve iterar sobre o array recebido, e em cada etapa i, deve calcular a média dos k elementos subsequentes (a contar da posição i) no array original e armazenar na posição i de um novo array. E esse novo array (com as médias) deve ser retornado.

Note que ao chegar na iteração de numero n-k+2, haverá n-(n-k+2)+1 = k-1 elementos (incluindo o atual). Nesse ponto, não poderá ser calculada a média de k elementos.
Portanto, ao terminar a iteração de nº n-k+1, a função deve interromper a iteração e retornar o array construído com as médias.


Sintoma: Ao invés de retornar um array com n-k+1 elementos, era retornado apenas n-k.


Teste de regressão:
Atualmente há dois testes. O primeiro chamado test_media_movel que verifica o tamanho e cada um dos valores retornados por média móvel com n=50 e k=3.
E outro chamado test_media_movel_600_pontos_janela_30 que faz a verificação do tamanho da media movel, e do primeiro e ultimo valor retornado, desta vez com n=600 e k=30.
O primeiro teste já detecta o problema, pois a implementação retorna 47 valores em vez dos 48 esperados.


Causa do Problema:
media_movel é implementada da seguinte forma:
É chamada a função cumsum do NumPy, que cria um novo array - chamemos de acumulada - com n elementos, onde o elemento de índice i é exatamente o resultado da soma de todos os elementos do array original do indice 0 até o indice i, inclusive. Acumulada possui, também, n elementos.

Em seguida, a implementação calcula:
`(acumulada[k:] - acumulada[:-k]) / k`

Como os dois intervalos possuem n-k elementos, o resultado também possui apenas n-k valores.
Além disso, a diferença entre as somas acumuladas desloca as janelas em uma posição: o primeiro resultado corresponde à janela iniciada no índice 1, e não no índice 0. Portanto, a primeira janela válida é omitida.


Correção:
A solução consiste em acrescentar um zero antes da soma acumulada, usando np.concatenate.
Desta forma, a soma acumulada passa a ter os n+1 elementos, e o calculo `(acumulada[k:] - acumulada[:-k]) / k` passa a retornar a media movel incluindo a primeira janela válida.

Posteriormente, a função converte o array de médias em um objeto SerieTemporal com o método SerieTemporal.de_lista(), e o retorna.


Por que os testes de aceitação não pegaram o defeito:
Os testes de aceitação não pegaram o defeito porque nenhum deles verificava se a quantidade de elementos retornados era condizente com o contrato da função. Portanto, as verificações não identificavam quando a primeira janela válida era omitida.

Mais um caso que eles não cobrem e qual teste seu o cobre:
Outro caso não coberto pelas verificações anteriores é a verificação numérica de cada valor retornado.
O teste test_media_movel que foi implementado, passa a verificar numericamente - usando np.allclose - cada um dos valores retornados por media_movel, tendo como parametro um array de tamanho 50 e janela de tamanho 3. Além de verificar a quantidade.
Deste modo, detecta erros numéricos que poderiam passar despercebidos ainda que o tamanho estivesse correto.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->

=== Etapa 0: ambiente ===
Python 3.12.10 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 2.0 | matrícula 3500

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

      k        h         erro
      0    1e+00    1.658e-05
      1    1e-01    1.657e-06
      2    1e-02    1.657e-07
      3    1e-03    1.654e-08
      4    1e-04    1.367e-09
      5    1e-05    6.224e-10
      6    1e-06    5.062e-09
      7    1e-07    6.191e-08
      8    1e-08    2.780e-06
      9    1e-09    1.415e-05
     10    1e-10    5.826e-04
     11    1e-11    2.701e-04
     12    1e-12    1.394e-02
     13    1e-13    7.078e-02
     14    1e-14    2.134e-01
    menor erro: h = 1e-5, erro = 6.224e-10


Quando h é grande, ocorre o erro de truncamento. A fórmula ignora os termos de Taylor de ordem h, então o erro cai proporcionalmente a h: de 1.658e-05 em h = 1 para 1.654e-08 em h = 1e-3, 10 vezes a cada linha.

Quando h é muito pequeno, f(x+h) e f(x) ficam muito próximos, e acontece um erro de arredondamento, onde o resultado perde dígitos significativos. Esse erro aumenta, porque é dividido por um h cada vez menor, e chega a 2.134e-01 em h = 1e-14. O menor erro (6.224e-10) ocorre em h = 1e-5, onde os dois erros se equilibram.

Quando h fica menor que o espaçamento entre os floats perto de 1000 (cerca de 1.1e-13), x + h é arredondado para x (1000 + 1e-14 == 1000 dá True), e o cálculo f(x+h) - f(x) retorna 0. Nesse caso, o erro corresponde a |0 - derivada|, que é a própria derivada.


### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes de aceitação não pegaram o defeito. -->

Os testes são: test_soma_float e test_parcelas_pequenas_nao_se_perdem. Ambos falham com o código original (o primeiro obtém 100000.00000133288 em vez de 100000.0).
t é definido como s+y. t - (s + y) dá sempre zero porque é equivalente a (s + y) - (s + y), onde as duas operações entre parênteses produzem exatamente o mesmo erro.
Inverter a ordem das operações faz com que seja calculado ((s + y) - s) - y: (s + y) - s recupera a parte de y que realmente entrou na soma arredondada, e subtrair y dela dá o que se perdeu, que é a correção descontada da parcela seguinte.

Os testes de aceitação não pegaram porque somam só 10 parcelas de 0.1: o erro (cerca de 1e-16) fica muito abaixo da tolerância do math.isclose, e até a soma ingênua passa. Nenhum deles compara o Kahan com o valor exato numa soma longa.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e por que a média de quase 600 leituras não elimina o viés da curva linear. -->

Precisão mede quão próximas as medidas estão da média delas. Exatidão (ou acurácia) mede o quão próximas estão as medidas do valor que elas deveriam ter.

As duas curvas convertem as mesmas contagens (com o mesmo ruído) portanto, devem ter a mesma dispersão. De fato, as curvas lineares tiveram desvios 0.706 (PT101) e 0.515 (PT102) e as spline 0.710 e 0.517.

A linear teve viés -1.840 e a spline -0.010 em PT102: a resposta do transmissor é curva, e a linear a aproxima por retas entre os pontos da tabela, errando sempre para o mesmo lado. A média de quase 600 leituras reduz só o erro aleatório (o erro padrão é de cerca de 0.02 kPa), mas não elimina o viés da curva linear, pois ele é igual em toda leitura, então não se cancela.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

A cada iteração do método da bissecção, o intervalo em que a raiz está é dividido exatamente por duas metades.
Assim, em 44 iterações o comprimento do intervalo vai ser exatamente $\dfrac{b-a}{2^44}$.
Como o intervalo inicial e a tolerância são os mesmos para todos os Reynolds, a quantidade de iterações necessária é sempre a mesma.
Em $n$ iterações, o intervalo em que sabemos que a raiz está é de tamanho $\dfrac{b-a}{2^n}$.
Ordem de convergência 2 significa que, perto da raiz, o erro seguinte é aproximadamente proporcional ao quadrado do atual, dobrando aproximadamente os dígitos corretos por passo.
Newton pode falhar quando a derivada no ponto inicial é nula. Para $f(x)=x^3 + 1$ em $[-2,2]$, o ponto médio do intervalo é 0, $f'(0)=0$ e o método de Newton falha, enquanto a bissecção converge.

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->
A derivada é usada no método de Newton, porque fornece a inclinação da melhor aproximação linear da curva em um determinado ponto. 
Calcular a derivada uma vez só deixa a convergência linear, pois não estaremos utilizando calculando a melhor aproximação lienar sempre, e sim pegando uma reta com direção constante. Os testes de aceitação não pegaram o defeito porque, apesar de ter menor eficiência, o algorítmo encontrava a raiz que procurava; e nenhum teste verificava a eficiência.
Testes de regressão: test_aproximacoes_usam_derivada_no_ponto_atual, test_colebrook_converge_em_ate_cinco_iteracoes

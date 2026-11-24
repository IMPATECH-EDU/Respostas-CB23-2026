# Relatório — Francisco Renan Vale Cardoso (3523)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

```
/home/renan/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.4 | fornecido 4.0
```

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

A string "PT101 ", uma das inválidas, é aceita por re.match e rejeitada por re.fullmatch. Isso
ocorre pois o re.match busca se a string começa com um trecho que casa com a expressão regular. 
Por outro lado, o re.fullmatch exige que a string inteira case com o padrão da expressão regular.
Se usássemos re.match em valida_tag, strings que começam com uma sequência válida mas possuem um
resto qualquer passariam na validação. Isso viola o contrato, que diz que a tag tem de ter 1 ou 2
letras maiúsculas e de 1 a 3 dígitos, e não mais que isso.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

A função ler_log devolve as linhas descartadas devido a integridade da informação: jogar fora os logs inválidos estaria 
jogando informação fora, não sendo possível resgatar parte dela ou entender um erro que possa estar ocorrendo com os dados,
de modo que a investigação é sobre a captação ou transmissão deles. Uma situação real para exemplificar o problema de jogar
os dados fora seria um eventual pico de dados ser considerado inválido e descartado, mas esse pico de dados pode nos estar
informando que algum aparelho de captação como o RTU dos dados ou alguma rede de comunicação está defeituosa. Com meus dados
recebi 4 linhas avisando sobre invalidades de dados, onde elas apontam falha na comunicação com o RTU, e isso é importante saber.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

A forma errada é escrita assim `errados = {tag: (lambda c: c * k) for tag, k in escalas.items()}`. Como k sempre varía e não é
fixo para cada tag, logo quando a comprehesion acaba o valor de k é último possível. Se o último valor foi para um sensor de fluxo,
logo ele guarda k = 0.1, e então o cálculo sai errado para os sensores de pressão, e por isso temos 409,5, que é 4095 * 0.1. A
minha criar_conversores guarda o k junto com a lambda, logo não há o problema da variação de k influenciar a lambda: a lambda guarda
a sua constante que será usada na hora. Esse problema também ocorre pel fato de criar_conversores ser uma função que apenas cria as
conversões: se ela criasse uma conversão e a aplicasse em seguida ainda daria certo.

### R4 — Escala nominal

A primeira função em fornecido/simulador.py, p_real, retorna
`600.0 * np.sin(0.5 * np.pi * np.asarray(c, dtype=float) / 4095.0)`, uma função não linear, diferente da modelagem linear nominal,
com c * 600 / 4095. A escala nominal dá 262,0 kPa, a conferência 380,0 kPa, por que a reta subestima pressão devido ao transmissor
real seguir um seno.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: R5: e2a60c2, R6: 90fc0f5

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 4 | 18 |
| Tempo do laço / tempo vetorizado | 4 | 26 |
| Tempo da compreensão / tempo do laço | 1 | 1,1 |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

A lista apresenta 36 bytes por número (8 da referência mais 28 do objeto int), enquanto que uint16 2 apenas bytes. O laço interpreta cada
operação enquanto que o vetorizado aplica de uma vez. Vetorizado mais rápido. A compreenssão e laço interpretam elemento a elemento, possuindo
então tempo parecido (aproximadamente 1 como previ). Respondendo as perguntas: A maior diferença foi entre o tempo do laço e o vetorizado, que é
compilado, enquanto que o laço passa pelo interpretador do Python a cada elemento. 20 * uint16 dá 16364 por que a contagem dá a volta, ela
supera o máximo possível que esse tipo pode guardar e inicia do zero novamente (81.900 - 65.536 = 16364). Para guardar as contagens que vão de 0
a 4095 uint16 basta, mas para a pressão necessita ser um float, pois há casas decimais, e o float32 já basta, sendo mais econômico.


### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal| SerieTemporal |
| `s[1:]` | ndarray| SerieTemporal |
| `s * 2` | SerieTemporal| SerieTemporal |
| `s.sum()` | float | SerieTemporal |
| `s[0]` | float | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
O resultado mais surpreendente para mim foi s.sum() retornar um SerieTemporal, e não um número, que deveria é a natureza do
resultado do .sum()

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

Para a média móvel de 30 pontos da PT102, temos 570 valores, mas o esperado dado a docstring é 571. Os testes de regressão:
`test_media_movel_tem_n_menos_janela_mais_um_valores`, `test_media_movel_inclui_a_primeira_janela`(e `test_media_movel_janela_igual_ao_tamanho`).
A soma de cada janela é a diferença entre duas posições do `cumsum`, e na primeira janela faltava o termo 0. A resolução seria por um 0 no
início da soma acumulada, com `np.concatenate(([0.0], np.cumsum(self)))`. Os testes de aceitação não detectam tal erro porque eles não medem
o tamanho. Caso a janela seja igual ao tamanho da série, o código devolvia 0 ao invés de devolver 1 valor, a média de toda a série.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->

```
=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3523
```

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

Faz sentido, inicialmente, o erro diminuir quando h diminui, pois na prática o computador nunca fará h = 0. Esse é um erro de
truncamento (o erro do lado maior que 1e-5) pois temos uma limitação da fórmula para sua aplicação. Quando h diminui demais, ocorre
o erro de arredondamento, que é quando f(x+h) é quase igual a f(x) e a subtração deixa o ruído do arredondamento. Diminuir h amplifica
o erro (o do lado menor que 1e-5). Para h = 1e-14 ocorre que o numerador da derivada irá zerar, pois f(x+h) = f(x), então como o erro é
f'(x) - (f(x+h) - f(x))/h, logo o erro será f'(x). Fazer 1000 + 1e-14 == 1000 retorna True, porque para c tão grande o menor passo cai
muito, e então a diferença dos dois valores da função é nula. Da tabela: h=1, erro=1,658e-05; h=1e-5, erro=6,224e-10; h=14, erro=2,134e-14.

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->

Nome dos testes: test_um_milhao_de_decimos_da_exatamente_cem_mil, test_kahan_erra_menos_que_a_soma_ingenua,test_parcela_pequena_depois_de_uma_grande_nao_se_perde. 
O motivo de dar sempre zero é a ordem das operações que geram dado arredondamento. t = s + y, logo s + y sempre gera o mesmo arredondamento
e t - (s + y) = t - t = 0 sempre. Mas ao fazermos (t - s) - y retira a parte de cada uma das parcelas da soma total sobrando apenas o que o
arredondamento havia descartado, mas veja que é importante que se subtraia t - s primeiro para que que a subtração seja entre números de ordens
parecidas, então a ordem importa. O defeito não foi pego pelos testes porque ele só ocorre para pequenas parcelas, pois assim o arredondamento é
muito pequeno e então o resultado sai correto.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->

Temos que precisão é quando os dados concordam entre si, ou seja, há um desvio padrão pequeno. Já exatidão é quando o resultado se aproxima
do valor real. Temos que os desvios são muito parecidas (0.698 para linear e 0.702 para spline), logo ambas são precisas na mesma ordem, mas o
viés, ou seja, a diferença para o valor real, é menor na spline (0.015), então ela é a mais exata. A média de 600 linhas é boa para diminuir os 
ruídos, diminuindo o erro aleatório da media, que seria maior em um número menor de de medições, mas o víes na linear vem de um erro sistemático 
que afeta todo dado tomado, um erro que diminui o valor de todos os dados, então irá diminuir também a média deles.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

A bissecção itera sobre o intervalo, sempre o dividindo na metade, de modo que só para quando este fica menor que a tolerância, então ela não
depende da função ou do Reynolds, sempre dando 44 interações. Uma ordem de convergência 2 quer dizer que cada erro é perto do quadrado de seu
anterior, como vemos no output, temos que 5.0e-02 ~ (2.9)², 2,3e-05 ~ (5.0e02)². Output completo: 2.9e+00 5.0e-02 2.3e-05 5.0e-12 8.9e-16 0.0e+00
Para Newton, temos que se o chute inicial for muito longe da raiz, pode ocorrer divergência e oscilações, e uma situação onde Newton falha é
quando a derivada é 0 ou quase 0, por que ai o termo f(x)/f'(x) explode.

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->

Testes: test_raiz_de_dois_em_no_maximo_seis_iteracoes e test_digitos_corretos_dobram_a_cada_iteracao. Calcular a derivada uma vez e usá-la ira
implicar em menos informação sobre a curva perto da raiz, de modo que cada passo irá errar o valor da raiz na mesma proporção, uma proporção linear, em vez de ser elevada ao quadrado. Os teste de aceitação não detectavam isso porque eles apenas avaliam se a raiz estava certa, e de
fato ela estava, mas demorava mais para chegar nela, e essa demora não era avaliada (o número de iterações).
## Marco 4

### R13 — Integração e descontinuidade

<!-- Na Etapa 1(b), integrando o custo do dia de uma vez, a ordem observada cai para cerca
de 1, no trapézio e no Simpson; integrando cada faixa separadamente, voltam as ordens 2 e 4.
Por quê? -->

### R14 — Issue #11

<!-- Os nomes dos seus testes de regressão; a causa do defeito; por que os testes de
aceitação não o pegaram; por que a regra de Simpson não serve para o registro do dia. -->


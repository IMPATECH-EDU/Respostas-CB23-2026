# Relatório — Gabryel Rodrigues Ferreira (3547)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

~/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.14.7 | NumPy 2.5.4 | fornecido 3.0


### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

s = "BO1234"
Vai ser aceito pelo match e nao será aceito pelo fullmatch.
pois o fullmatch só aceita se a palavra toda seguir o padrão.
já o match corresponde ao inicio da string.



### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Para que a equipe possa reconhecer erros de leituras de pressão etc..
por exemplo, uma falha pode causar que uma leitura de pressão não seja registrada.


### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Porque foi usada a compreensão para criar aas conversões, isso faz com que todas acabem usando o mesmo fator.
Na minha implementação eu usei funções lambdas, evitando esse problema.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
Essa diferença provavelmente veio devido a uma diferença entre a escala nominal do transmitor e a calibração utilizada para gerar os dados de referencia.


### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 874246b5479ac8811b3240530c30f8b7e43cb976 <!-- cole o hash curto do commit de previsões -->
###

(prog2-venv) gabryel@Gabryel:~/Documentos/Respostas-CB23-2026$ python3 -c 'import numpy as np; from elevatoria.dados import medir_memoria, medir_tempos; c = np.random.default_rng(1).integers(0, 4096, 1_000_000); print("MEMÓRIA:", medir_memoria(c)); print("TEMPOS:", medir_tempos(c, k=10))'
MEMÓRIA: {'list': 36000056, "array('H')": 2000000, 'uint16': 2000000, 'int32': 4000000, 'int64': 8000000, 'float32': 4000000, 'float64': 8000000}
TEMPOS: {'laço': 0.14117228409886592, 'compreensão': 0.12800499930090153, 'map+lambda': 0.14699144629994407, 'vetorizado': 0.00287036209992948}
(prog2-venv) gabryel@Gabryel:~/Documentos/Respostas-CB23-2026$

###

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | A lista vai ocupar mais memória que o array uint16.|A lista ocupou 36.000.056 bytes, enquanto array uint16 ocupou 2.000.000 bytes (18 vezes a mais).|
| Tempo do laço / tempo vetorizado |Espero que a vetorização seja mais rápida em muitos casos. |O laço levou 141ms, enquanto a vetorizada levou 2.87ms, a vetorizada foi muito mais rapida(~=49 vezes mais rápido). |
| Tempo da compreensão / tempo do laço | Acho que a compreensão será muito mais rápida do que laço. | O tempo de compreesão foi 128ms já o laço levou 141ms, acho que essa diferença foi muito menor do que eu esperava (0.90) |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->


### R6 — Tipos da SerieTemporal (Etapa 4d)
###
(prog2-venv) gabryel@Gabryel:~/Documentos/Respostas-CB23-2026$ python3 -c 'from elevatoria.serie import SerieTemporal; s = SerieTemporal.de_lista([1, 2, 3]); print("s + s:", type(s + s).__name__); print("s[1:]:", type(s[1:]).__name__); print("s * 2:", type(s * 2).__name__); print("s.sum():", type(s.sum()).__name__); print("s[0]:", type(s[0]).__name__)'
s + s: SerieTemporal
s[1:]: SerieTemporal
s * 2: SerieTemporal
s.sum(): SerieTemporal
s[0]: float64
###

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` |SerieTemporal|SerieTemporal|
| `s[1:]` |SerieTemporal|SerieTemporal|
| `s * 2` |SerieTemporal|SerieTemporal|
| `s.sum()` |Float|SerieTemporal|
| `s[0]` |Float|float64|

<!-- Explique o resultado que mais surpreendeu você. -->
Acho que o que me mais me surpreendeu fooi o s.sum() ser serieTemporal. Pelo que entendi isso acontece porquea classe herda numpy e o numpy pode preservar a subclasse(ndarray) em operações como sum(), dependendo de como estão implementadas.
### R7 — Issue #4
O sintoma é que a media movel retorna 570 invés de 571.
O teste de regressão (test_media_move) avalia se a função retorna a quantidade correta.
A causa foi que uso de acumulada[janela:] descartava um valor da soma acumulada, reduzindo em um a quantidade de resultados. Além disso, a primeira janela precisa ser tratada separadamente, pois não existe uma soma anterior a subtrair.
Para corrigir isso utilizei acumulada[janela - 1:].copy() e subtraí as somas acumuladas anteriores apenas das posições seguintes. A solução não utiliza laços, não modifica a série original e retorna uma SerieTemporal.

## Marco 2

### Ambiente

Python 3.14.10 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3547

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->
O erro de 1 a 1e-5 é o erro de truncamento. que diminui junto com h a cada passo que a secante se aproxima da tangente.
a partir de 1e-5, o erro de arredondamento domina. subtrai algo pequeno de algo grande perde precisão por causa do limite de digitos no ponto flutuante.



### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->
test_desoma e test_cancelamento.
no test de soma, tentei acumular 1000 numeros 0.1.
a causa do erro é que s+y é arredondado para t em ponto flutuante. fazendo com que dê zero. a ordem da operação muda os resultados. operar t-s primeira não arrendonda para y. não vai dar zero.

no test cancelamento,
o float nao tem casas para guardar 1e16 e 1.0 ao mesmo tempo, os numeros 1.0 sao perdidos no arredondamento. fazendo com que 1e16+1.0+1.0-1e16 resulte em 0.0



### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->

Fazer a média de quase 600 leituras não elimina o viés da curva linear porque a média só cancela o ruído aleatório, que varia para cima e para baixo. Como a aproximação por reta da interpolação linear empurra todas as leituras para baixo nessa faixa, o erro é sistemático e a média continua deslocada.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

A bissecção divide o intervalo ao meio a cada passo isso resultan em um número fixo de iterações. A ordem de convergência 2 significa que o erro atual é proporcional ao quadrado do erro anterior. O Newton falha se a derivada inicial for zero, se tiver muitas oscilações bruptas ou se o chute inicial estiver distante da raiz, enquanto a bissecção sempre converge se houver troca de sinal.



### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->

test_regressao_newton_convergencia_rapida
test_regressao_newton_atualiza_derivada
test_ordem_convergencia_quadratica
test_ordem_convergencia_lanca_erro_poucos_erros

Derivar uma vez fixa a inclinação. OS testes de aceitaçao nao pegaram porque eles verificavam se o método encontra a raiz correte. nao testaram restrições para velocidades nem o número exato de intereações.

## Marco 4

### R13 — Integração e descontinuidade

<!-- Na Etapa 1(b), integrando o custo do dia de uma vez, a ordem observada cai para cerca
de 1, no trapézio e no Simpson; integrando cada faixa separadamente, voltam as ordens 2 e 4.
Por quê? -->

A variação abrupta das tarifas nas fronteiras das faixas quebra a suavidade da função. Integrar o dia todo de uma vez faz o erro dominar e cair para ordem 1. Integrando por faixa, cada trecho é contínuo e recupera as ordens 2 e 4.


### R14 — Issue #11

<!-- Os nomes dos seus testes de regressão; a causa do defeito; por que os testes de
aceitação não o pegaram; por que a regra de Simpson não serve para o registro do dia. -->

test_integracao_com_falhas_multiplas
test_integracao_com_valores_nan

A causa foi o passo constante no trapezio, quebrava em malhas irregulares. Simpson serve porque exige que a malha seja perfeitamente uniforme e um número impar de pontos
# Relatório — Augusto Schaefer Huff (3527)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente
#### Output do Which Python
(prog2-venv) (ambiente_aluno) al.augusto.huff@C1-14-15-16124:~/Documentos/Respostas-CB23-2026$ which python
/home/al.augusto.huff/venvs/prog2-venv/bin/python

#### Output do marco1.py - Etapa 0
(prog2-venv) (ambiente_aluno) al.augusto.huff@C1-14-15-16124:~/Documentos/Respostas-CB23-2026$ python marco1.py 
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 2.0

### R1 — Expressões regulares
<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
"PT101 " e "PT1010"
O valida_tag aceitaria ambas como True se usassemos o re.match, o que iria em desacordo com o enunciado que especifica que ambas são inválidas.


### R2 — Linhas inválidas
<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Por que é importante saber quais linhas estão sendo descartadas, para poder identificar a causa dessas linhas inválidas. Um exemplo de situação real é algum sensor que não está funcionando ou algum erro de configuração/digitação na hora de digitar as tags, o que causaria o descarte das linhas.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Porque a lambda guarda só o nome da variável k, e não o seu valor. Ela só procura o valor de k quando é chamada, e nesse momento a compreensão já terminou com o último valor, k = 0.1 (o fator do FT201). Por isso 4095 * 0.1 = 409.5.
A minha criar_conversores usa o argumento padrão f=escalas[tag], que é calculado no momento em que a lambda é criada, então cada lambda guarda o fator da sua própria tag.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
Hipótese: o transmissor de pressão não é linear. Em fornecido/simulador.py, a função p_real mostra que a resposta verdadeira é p = 600 * sen(pi/2 * c/4095), mas a escala nominal supõe uma reta (p = c * 600/4095).
Para 380 kPa o A/D lê cerca de 1788 contagens, que a reta converte em cerca de 262 kPa. A tabela_calibracao existe para corrigir essa diferença.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 15x | 18,0x |
| Tempo do laço / tempo vetorizado | 50x | 40,1x |
| Tempo da compreensão / tempo do laço | 0,8 | 0,90 |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
A maior diferença foi no tempo vetorizado (previ 50x, medi 40x): com 1 milhão de elementos a conta em si é tão rápida que o custo fixo de criar o array de saída pesa mais. Na memória a lista gasta 36 bytes por elemento (8 do ponteiro + 28 do objeto int), contra 2 do uint16, por isso 18x.
O uint16 só guarda valores de 0 a 65535; 4095 * 20 = 81900 passa do limite e "dá a volta": 81900 - 65536 = 16364 (overflow).
Para guardar contagens eu escolheria uint16 (0 a 4095 cabe, 2 bytes cada). Para pressões em kPa, float64, porque são números com casas decimais e as contas (médias, somas) ficam mais precisas.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float | SerieTemporal |
| `s[0]` | float | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
O que mais surpreendeu foi s.sum() devolver SerieTemporal: como a classe é uma subclasse de ndarray, o NumPy mantém o tipo da subclasse até no resultado da soma, que vira uma "série" de dimensão zero. Já s[0] devolve float64, um número do NumPy e não um float comum do Python.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
Sintoma: media_movel(30) na série de 600 pontos devolvia 570 valores, e não 571 (n - janela + 1). Testes de regressão: test_media_movel_tamanho_n_menos_janela_mais_um, test_media_movel_valores_incluem_primeira_janela e test_media_movel_janela_igual_ao_tamanho.
Causa: acumulada[i] era a soma de x[0] até x[i] inclusive, então acumulada[janela:] - acumulada[:-janela] só dá as janelas que começam em 1, 2, ...; a primeira janela (que começa em 0) precisaria de uma soma "antes do início", que não existia.
Correção: coloquei um 0 no início da soma acumulada (np.concatenate), com .view(SerieTemporal) para manter o tipo. Assim a primeira janela entra e saem n - janela + 1 valores.
Os testes de aceitação só conferiam o tipo do retorno e os erros para janela 0 e 6, nunca o tamanho nem os valores. Outro caso que eles não cobrem: serie com leitura de valor 0 (contagens=0), que a versão antiga descartava; está coberto por test_serie_mantem_valor_zero.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->
=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3527

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->
De h = 1 até h = 1e-5 domina o erro de truncamento (a diferença adiante ignora os termos de ordem h da série de Taylor): ele cai 10 vezes a cada vez que h cai 10 vezes (1,66e-5 em h = 1 até 6,2e-10 em h = 1e-5, o menor erro).
Depois disso domina o erro de arredondamento: f(x + h) e f(x) ficam quase iguais e a subtração perde algarismos, e esse erro é dividido por h, então cresce quando h diminui (chega a 0,355 em h = 1e-13).
Em h = 1e-14, 1000 + 1e-14 == 1000 é True: o h é menor que o espaçamento entre floats perto de 1000, então x + h vira o próprio x, a diferença f(x + h) - f(x) dá 0 e o erro é |0 - derivada| = a própria derivada (0,2134).

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->
Testes de regressão: test_kahan_um_milhao_de_decimos_da_exato, test_kahan_erro_bem_menor_que_o_ingenuo e test_kahan_guarda_parcelas_pequenas.
Causa: t já é o resultado arredondado de s + y. Calcular s + y de novo dá exatamente o mesmo arredondamento, então t - (s + y) = t - t = 0 sempre e a correção nunca guardava nada. Já em (t - s) - y, a conta t - s recupera a parte de y que realmente entrou na soma, e tirando y sobra o que se perdeu no arredondamento.
Os testes de aceitação só somavam 10 parcelas de 0,1 e comparavam com math.isclose, que tem tolerância grande; com tão poucas parcelas o ingênuo e o Kahan defeituoso passam do mesmo jeito.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->
Precisão é o quanto as leituras se espalham (o desvio), e exatidão é o quanto a média fica perto do valor verdadeiro (o viés). Para PT102 as duas curvas têm quase o mesmo desvio (0,525 kPa na linear e 0,527 kPa na spline), então são igualmente precisas, mas o viés da linear é -1,819 kPa e o da spline é 0,011 kPa: só a spline é exata.
Tirar a média de 595 leituras diminui o erro aleatório (o erro padrão fica em torno de 0,525 / raiz(595) ≈ 0,02 kPa), mas o viés da curva linear é um erro sistemático: a reta erra para o mesmo lado em todas as leituras, então ele não se cancela na média.
## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->
A bissecção divide o intervalo ao meio a cada iteração e para quando a largura fica menor que tol. Então o número de iterações só depende da largura inicial e da tolerância (cerca de log2((b - a)/tol)), e não da função: por isso dá 44 para qualquer Reynolds.
Ordem 2 quer dizer que cada erro é mais ou menos o quadrado do anterior (e_{k+1} ≈ C·e_k²), ou seja, o número de dígitos corretos dobra a cada iteração. Para Re = 1e4 os erros do Newton foram 5,0e-2, 2,3e-5 e 5,0e-12: 2, 5 e 11 dígitos corretos.
O Newton falha quando a derivada é zero ou quase zero perto do ponto (a tangente fica horizontal e o próximo x vai para muito longe), ou quando o chute inicial está longe e ele diverge ou fica oscilando. A bissecção não tem esse problema: se f(a) e f(b) têm sinais opostos, ela sempre converge.

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->
Testes de regressão: test_newton_raiz_de_2_em_poucas_iteracoes, test_newton_converge_quadraticamente e test_colebrook_re_1e4_em_poucas_iteracoes.
Com a derivada calculada só no ponto inicial, o método usa sempre a mesma inclinação f'(x0) em vez da tangente no ponto atual. Perto da raiz, o erro passa a ser multiplicado por um fator constante (1 - f'(raiz)/f'(x0)) a cada passo, e isso é convergência linear: os dígitos corretos crescem de pouco em pouco em vez de dobrar. A correção foi calcular a derivada dentro do laço, a cada iteração.
Os testes de aceitação só conferiam que o Newton converge e chega na raiz certa; eles não olhavam o número de iterações nem a ordem de convergência, e um método lento também acaba chegando na raiz.

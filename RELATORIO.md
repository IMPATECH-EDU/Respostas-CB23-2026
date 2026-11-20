# Relatório — <seu nome> (<sua matrícula>)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

Path do python e Etapa 0:

No linux do IMPATECH.
``` 
-> which python                               
/home/al.souza.pedro/venvs/prog2-venv/bin/python
```
``` 
-> python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 4.0
``` 
No meu windows pessoal.
``` 
-> (Get-Command python).Path
C:\Users\pedro\venvs\prog2-venv\Scripts\python.exe
```
```
-> python marco1.py
=== Etapa 0: ambiente ===
Python 3.13.5 | NumPy 2.4.6 | fornecido 4.0
```

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
re.match aceita 'PT103weubcwo9ien\n\nscv658212r5', mas re.fullmatch rejeita. Usar re.match permite falsos positivos, já todos os positivos de fullmatch está contido em todos os positivos de match (O contrário não vale).

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Ainda que uma linha não seja útil para as medições, o sensor pode comunicar um erro por mensagem. Essa linha é corrompida do ponto de vista do tratamento dos dados, mas contém informação relevante. Basta ver uma das linhas corrompidas "### Falha de comunicação com o RTU ###" de exemplo.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Ao definirmos uma função lambda, criamos um escopo onde podemos definir variáveis. Errados define a variável de entrada, mas usa diretamente o k definido no escopo do for in line. Então quando chamamos a função, ela tenta usar uma variável que não existe no seu escopo e segue procurando nos escopos que contêm a função. No escopo do for in line, k refere-se ao último valor acessado. Na nossa função, k é definido no escopo de lambda.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
Nossa função de conversão é linear, mas a conversão real se dá pela expressão c = 4095 · (2/π) · arcsin(p / 600), como pode ser visto em c_real em simulador.py.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: abaa37e <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 36000056/2000000 ~ 18.000028 | 18.000028 |
| Tempo do laço / tempo vetorizado  | ~35 | 34.54 | 
| Tempo da compreensão / tempo do laço  | ~0.71 | 1/1.07 = 0.93|

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
Tinha colocado a previsão na coluna errada, mas corrigi. A memória deu exata pois .tolist() cria uma lista com allocated = ob_size. Então o tamanho da lista será 56 + 8*N + 28*N (tamanho dos ponteiros + tamanho de um int). Já uint16 ocupa 2 bytes/elemento. Os tempos de laço/vetorizado deram consistentes, não há como encontrar o valor exato, mas usei dis.dis pra ver os processos de um laço, estimei o tempo de cada ação em unidades genéricas. Considerei que o vetorizado levava uma unidade/elemento. O compr/laço deu bastante diferente. Eu achei que ia ser bem mais rápido por não usar nenhum CALL, mas acho que superestimei. Também: 4095 * 20 = 81900 > 2**16. O NumPy tira o mod. Por isso seria mais apropriado usar int64. Em dados.py, linha 245 tomamos cuidado para converter para float64 antes de multiplicar. 

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | SerieTemporal (0-d) | SerieTemporal (0-d, `ndim == 0`) |
| `s[0]` | float64 | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
Previsões no commit 92f6ee2. O que mais chama atenção é `s.sum()`: o resultado é um número, mas continua sendo `SerieTemporal` (com `ndim == 0`). A soma é uma redução de ufunc (`np.add.reduce`), e o NumPy devolve o resultado passando pelo `__array_wrap__` da subclasse, que mantém o tipo mesmo sem dimensão. Já `s[0]` é indexação de um elemento só, que devolve um escalar do NumPy (`float64`), e não uma view. Por isso o `marco1.py` usa `float(...)` antes de comparar ou formatar médias e somas: senão estaríamos passando uma "série" de zero dimensões.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
Sintoma: com a série de PT102 (600 leituras) e janela 30, `media_movel` devolvia 570 valores, e não 571. Teste de regressão: `TestRegressaoMediaMovel.test_quantidade_de_valores` (falhava com `570 != 571`), junto com mais três da mesma classe. Causa: `np.cumsum` dá `A[i] = s[0] + ... + s[i]`, então `A[j+w] - A[j]` é a soma de `s[j+1 .. j+w]`. A primeira janela, `s[0:w]`, precisaria de um "A[-1] = 0" que não existe: ela some, e todas as médias ficam deslocadas um ponto para frente. Correção: colocar um 0 na frente da soma acumulada (`np.insert(np.cumsum(self), 0, 0.0)`), daí `A[j+w] - A[j]` passa a ser exatamente a soma de `s[j : j+w]`.
Os testes de aceitação só conferiam o tipo do retorno e o `ValueError` para janelas 0 e 6, nunca o tamanho nem os valores. Outro caso que eles não cobrem: janela igual ao tamanho da série, que deve dar um único valor (a média de tudo); o código antigo devolvia uma série vazia. Coberto por `test_janela_igual_ao_tamanho`.

## Marco 2

### Ambiente

No meu windows pessoal (SciPy instalado no mesmo venv com `python -m pip install scipy`).
```
-> python marco2.py
=== Etapa 0: ambiente ===
Python 3.13.5 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3472
```

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->
De h = 1 até 1e-5 domina o erro de truncamento da diferença adiante, que é ~ h·|f''|/2: cai uma casa decimal por casa de h (1.66e-5, 1.66e-6, 1.66e-7...). Depois domina o arredondamento: f(1000) ≈ 225 kPa tem erro ~ eps·225 ≈ 5e-14, e a subtração f(x+h) − f(x) cancela quase todos os dígitos, então o erro vira ~ 5e-14/h e cresce quando h diminui (6.2e-10 em 1e-5, 2.8e-6 em 1e-8, 1.4e-2 em 1e-12). O mínimo fica perto de h ~ sqrt(eps·|f|/|f''|) ≈ 1e-5, que bate com a tabela. Em h = 1e-14, `1000 + 1e-14 == 1000` dá `True` (1e-14 é menor que meio ulp de 1000, que é ~5.7e-14), então x + h é o próprio x, o numerador é 0 e a aproximação é 0: o erro é a derivada inteira, 0.2134.

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->
Testes: `TestRegressaoKahan.test_pulsos_de_um_decimo`, `test_parcelas_menores_que_meio_ulp` e `test_concorda_com_fsum` (os três falhavam). A causa: `t` já é o resultado arredondado de `s + y`. Quando o código calcula `s + y` de novo, o computador faz a mesma conta com o mesmo arredondamento e chega no mesmo `t`, então `t - (s + y)` é `t - t = 0` sempre, e a correção nunca guarda nada. Em `(t - s) - y`, a conta `t - s` é exata e devolve a parte de `y` que de fato entrou na soma; tirando `y`, sobra (com sinal trocado) o pedaço que se perdeu, que é descontado na parcela seguinte. A ordem das operações importa porque em ponto flutuante a soma não é associativa. Os testes de aceitação só somavam 10 parcelas de 0,1 e comparavam com `math.isclose`, que tem tolerância relativa de 1e-9: o ingênuo passa, então o Kahan defeituoso (que é igual ao ingênuo) também passa. Nenhum teste comparava o Kahan com o ingênuo ou exigia o resultado exato.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->
Precisão é o quanto as leituras se espalham entre si; exatidão é o quanto a média fica perto do valor verdadeiro. Para PT102, o desvio é 0.523 kPa na linear e 0.524 kPa na spline: as duas curvas têm quase a mesma inclinação perto de 380 kPa, então espalham o ruído das contagens do mesmo jeito (mesma precisão). Já o viés é −1.841 kPa na linear e −0.012 kPa na spline: a resposta real (um seno) é côncava, e a reta entre dois pontos da tabela fica abaixo dela, então a linear subestima toda leitura nessa região. A média das 595 leituras válidas reduz o erro aleatório (o erro padrão fica ~0.524/√595 ≈ 0.02 kPa), mas o viés é sistemático: todas as leituras são convertidas pela mesma curva errada e erram para o mesmo lado, então a média herda o erro inteiro.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->
A bissecção não olha para a forma de g, só para o sinal: cada iteração corta o intervalo ao meio, e ela para quando a largura fica abaixo de tol. Começando em [2, 15] (largura 13) com tol = 1e-12, são precisas n iterações com 13/2^n < 1e-12, ou seja n > log2(1.3e13) ≈ 43.6, logo 44, para qualquer Reynolds. Ordem 2 quer dizer e_{k+1} ≈ C·e_k²: o número de dígitos corretos dobra a cada passo. Em Re = 1e4, os erros do Newton foram 5.0e-2 → 2.3e-5 → 5.0e-12, e as razões e_{k+1}/e_k² dão 0.0092 e 0.0095, praticamente constantes. O Newton falha quando a reta tangente manda o próximo ponto para longe: se a derivada for quase nula (f plana) ou o chute estiver longe, ele pode divergir ou sair do domínio, como na curva da bomba, que não extrapola e levanta `ValueError` fora de [0, 100] L/s. A bissecção, com troca de sinal em [a, b], nunca sai do intervalo e sempre converge.

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->
Testes: `TestRegressaoNewton.test_colebrook_re_1e4_em_poucas_iteracoes` (10 iterações em vez de no máximo 6), `test_raiz_de_dois_converge_quadraticamente` (32 iterações) e `test_derivada_reavaliada_em_cada_aproximacao` (a df era chamada em 1 ponto só, em 27 iterações). Com a derivada d0 = f'(x0) fixa, o método vira a iteração de ponto fixo x_{k+1} = g(x_k), com g(x) = x − f(x)/d0. Perto da raiz r, e_{k+1} ≈ g'(r)·e_k, com g'(r) = 1 − f'(r)/d0, que só é zero se d0 = f'(r). Como d0 é a derivada do ponto inicial, g'(r) ≠ 0 e a convergência é linear, com taxa |1 − f'(r)/f'(x0)| (em x² − 2 a partir de 1, a taxa é |1 − 2√2/2| ≈ 0.41, por isso 32 iterações). O Newton de verdade recalcula a derivada e consegue g'(r) = 0, que é o que dá a ordem 2. Os testes de aceitação só conferiam que o método convergia e que a raiz estava certa; como a versão linear também converge para a raiz certa, só que mais devagar, eles passavam. Nenhum teste conferia o número de iterações nem a ordem.

## Marco 4

### R13 — Integração e descontinuidade

<!-- Na Etapa 1(b), integrando o custo do dia de uma vez, a ordem observada cai para cerca
de 1, no trapézio e no Simpson; integrando cada faixa separadamente, voltam as ordens 2 e 4.
Por quê? -->
As ordens 2 e 4 valem para integrandos suaves: o erro de cada subintervalo é O(h³) no trapézio e O(h⁵) no Simpson, e somando os n = 24/h subintervalos sobram O(h²) e O(h⁴). O custo de uma vez é potência × tarifa, e a tarifa salta às 18 h e às 21 h. Com n = 30, 50, 70, 90 e 110, h = 24/n, e 18 h só seria nó se n fosse múltiplo de 4 (nenhum desses é: todos dão resto 2), então os saltos caem no meio de subintervalos. Nesses dois subintervalos a regra "espalha" o salto, com erro proporcional a (salto)·h, e como são sempre dois, o erro total fica O(h): ordem ~1 (deu 1.00 no trapézio e 0.65 no Simpson, que oscila conforme onde o salto cai). Integrando por faixa, cada integral é de uma função suave (a tarifa é constante dentro dela) e os limites 18 e 21 viram extremos, então voltam as ordens 2.00 e 4.00 (erro 6.3e-4 e 8.1e-8 em n = 110).

### R14 — Issue #11

<!-- Os nomes dos seus testes de regressão; a causa do defeito; por que os testes de
aceitação não o pegaram; por que a regra de Simpson não serve para o registro do dia. -->
Testes: `TestRegressaoTrapezioTabela.test_reta_em_malha_irregular` (dava 9.5 em vez de 16.5), `test_constante_com_leitura_perdida` (0.75 em vez de 1), `test_registro_do_dia_com_vazao_constante` (1100 em vez de 1200) e `test_primeiro_passo_maior_que_os_outros` (3.5 em vez de 2). Causa: `integrar_tabela` usava `h = x[1] - x[0]` para todos os trapézios, supondo leituras a cada 15 min. No meu registro, 8 das 97 leituras se perderam e há 8 intervalos de 30 min; cada um entrava como se fosse de 15 min, perdendo cerca de 8/96 ≈ 8% da área (o volume deu 3577.7 m³, 7.98% abaixo de 3888.0). A correção usa `np.diff(x)`, a largura de cada trapézio. Os testes de aceitação só chamavam `integrar_tabela` com malhas uniformes (`linspace` e passo de 1,5 h), onde o passo fixo é o passo certo: o mesmo motivo de "em dias sem falhas, as contas batem". O Simpson composto ajusta uma parábola a cada par de subintervalos iguais, e a fórmula 1-4-2-4-...-1 só vale com passo constante e número par de subintervalos; o registro mistura passos de 15 e 30 min (e a ponta tem 12 pontos, número par), por isso `integrar_tabela` do Simpson recusa a tabela com `ValueError`.

# Relatório — Vitor Marian (3518)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Saída de `which python`: /c/Users/vitor/venvs/prog2-venv/Scripts/python

Etapa 0 do `python marco1.py`: 
=== Etapa 0: ambiente ===
Python 3.14.3 | NumPy 2.5.4 | fornecido 1.0

### R1 — Expressões regulares

Com o padrão `[A-Z]{1,2}\d{1,3}`, `re.match` aceita `"PT1010"` (casa o prefixo `PT101`), e `re.fullmatch` rejeita porque sobra o `0`. Se `valida_tag` usasse `match`, tags com sobra no fim, como `"PT1010"` e `"PT101 "`, seriam consideradas válidas.

### R2 — Linhas inválidas

Para que as falhas possam ser contadas e auditadas, em vez de sumirem. Se a comunicação com a RTU cair repetidamente durante um alarme de pressão alta, descartar essas linhas em silêncio faria parecer que a estação operou normalmente, quando na verdade ficou minutos sem leituras.

### R3 — Late binding

A lambda guarda a variável `k`, não o seu valor; `k` só é lido quando a função é chamada, e aí já vale o último fator do laço (`0.1`, de `FT201`): 4095 × 0,1 = 409,5. Em `criar_conversores`, o parâmetro padrão `fator=escalas[tag]` é avaliado na criação de cada lambda, então cada uma fica presa à sua própria tag.

### R4 — Escala nominal

O transmissor não é linear, pois a escala nominal supõe `p = c × 600 / 4095` e a resposta real é `p = 600 · sen(π/2 · c / 4095)`, que cresce mais rápido nas contagens médias. Por isso ~1788 contagens dão 262 kPa pela escala linear e 380 kPa pela curva real. A explicação está em `p_real` e `tabela_calibracao`, em `fornecido/simulador.py`.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d050c9b

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 16 | 18,0 |
| Tempo do laço / tempo vetorizado | 20 | 15,5 |
| Tempo da compreensão / tempo do laço | 0,5 | 0,97 |

**Justificativa da previsão** O `uint16` ocupa 2 bytes por elemento, e a lista padrão do Python certamente ocupa muito mais, o que torna a razão alta. Como o NumPy é otimizado para operações numéricas, a versão vetorizada deve ser a mais rápida. As versões com `list` e `map` devem ser mais lentas que o NumPy e ficar um pouco atrás da compreensão, que o Python também otimiza. Por fim, o laço `for` deve ter o pior desempenho, pois laços em Python não são adequados para tratamentos de dados simples como esse.

**Maior diferença** Considerando a diferença relativa entre o previsto e o medido, a maior diferença foi entre a compreensão e o laço de repetição. A compreensão só economiza a busca e o append no fim da lista; o maior custo, que é calcular `c * 600 / 4095` e criar um novo `float` por elemento, continua o mesmo, por isso o ganho foi bem menor que os 50% estimados.

**Estouro do `uint16`** O `uint16` guarda de 0 a 65535; 4095 × 20 = 81900 estoura e dá a volta: 81900 − 65536 = 16364. Para contagens (0 a 4095), pode-se usar `uint16`; já para pressões em kPa, `float64`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

**Justificativa da previsão** `s + s`, `s * 2` e `s[1:]` devem ser `SerieTemporal`, pois são operações ou fatiamentos sobre o próprio objeto da classe, então não há mudança de tipo. Já `s.sum()` e `s[0]` devem ser `float`: `s.sum()` é a soma dos itens de `s`, que são `float`, e `s[0]` é justamente um desses itens.

**Maior diferença** O `s.sum()` devolve uma `SerieTemporal` de dimensão 0, e não um número, porque o numpy repassa a subclasse no resultado das reduções. Note que `s[0]` devolve um escalar conforme previsto, porque referenciar um único elemento não usa esse mecanismo.

### R7 — Issue #4

Sintoma: `media_movel(30)` em 600 pontos devolvia 570 valores, e não 571. Teste de regressão: `test_quantidade_de_valores`. Causa: `acumulada[i]` é a soma de `self[0..i]`, então `acumulada[janela:] - acumulada[:-janela]` começa na janela `self[1:janela+1]` e perde a primeira. Correção: pôr um `0` no início da soma acumulada. A aceitação só confere o tipo e os erros, nunca o tamanho nem os valores. Outro caso não coberto: `janela == len(self)`, que devolvia 0 valores; é coberto por `test_janela_igual_ao_tamanho`.

## Marco 2

### Ambiente

Etapa 0 do `python marco2.py`: 
=== Etapa 0: ambiente ===
Python 3.14.3 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 3.0 | matrícula 3518

### R8 — Derivada numérica

De h = 1 até h = 1e-5 o erro cai de 1,66e-05 para 6,2e-10, e o erro dominante é o truncamento da diferença adiante, que é proporcional a h. 

Depois de 1e-5, o erro volta a crescer (5,1e-09 em 1e-6, 2,1e-01 em 1e-14), pois o dominante é o erro de arredondamento, já que `f(x + h) - f(x)` subtrai dois números quase iguais e perde algarismos significativos, então esse erro é dividido por um h cada vez menor. 

Em h = 1e-14, `1000 + 1e-14 == 1000` é `True`, pois o espaçamento entre floats perto de 1000 é ~1,1e-13. Por isso `f(x + h) - f(x)` vira 0 e a aproximação vale 0, tornando o erro igual à própria derivada: 0,2134.

### R9 — Issue #7

* Testes de regressão: `test_acumulador_kahan_1000` e `test_acumulador_kahan_2997`. 
* Causa: `t = soma + y` já é o resultado arredondado, por isso a conta `soma + y` é sempre o mesmo float `t`, daí `t - (soma + y)` é sempre 0. Quando `(t - soma) - y`, `t - soma` é exato e recupera a parte de `y` que de fato entrou na soma. Os testes de aceitação só somam `0.1` dez vezes e comparam com `math.isclose` e o erro da soma ingênua ali é pequeno, e o Kahan errado passa igual.

### R10 — Precisão × exatidão

* Precisão = dispersão das leituras em torno da própria média; Exatidão = proximidade dessa média ao valor real. 
* Para PT102 as duas curvas têm a mesma precisão/desvio, mas exatidões/viéses bem diferentes: desvio de 0,508 na linear e 0,510 na spline; viés de −1,874 na linear e −0,044 na spline.
* A média de aproximadamente 600 leituras reduz só o erro aleatório, já que seu sinal é variável e se cancela. O viés da curva linear é sistemático, note que todas as leituras por volta de 380 kPa passam pelo mesmo trecho da reta, o que erra a curva real sempre na mesma direção, assim a média converge para o valor errado.

## Marco 3

### R11 — Bissecção × Newton

* A bissecção só depende do intervalo e de `tol`, uma vez que `[2, 15]` cai à metade a cada iteração até a largura ficar menor que 1e-12, e log2(13 / 1e-12) ≈ 43,6 dá 44 iterações, portanto a função e o Reynolds não interferem nesse resultado.
* Ordem 2 significa `e_{k+1} ≈ C·e_k²`, ou seja, o número de dígitos corretos dobra a cada iteração. Para Re = 1e4, os erros vão de 5,0e-02 para 2,3e-05 e depois 5,0e-12, com ordem estimada 2,00.
* A situação que o Newton falha e a bissecção não falha pode ser a função `arctan(x)` no intervalo `[-2, 5]`: aqui, o Newton parte de 1,5, a tangente quase horizontal o joga cada vez mais longe da raiz, e em x ≈ 3,9e6 a derivada numérica dá zero (`ValueError`). Enquanto isso, a bissecção só precisa da troca de sinal para achar a raiz 0.

### R12 — Issue #9

* Testes de regressão: `test_colebrook_re_1e4_em_ate_6_iteracoes` e `test_derivada_reavaliada_a_cada_iteracao`.
* Causa: com a derivada `d` fixa em `x_0`, o erro segue `e_{k+1} ≈ (1 - f'(r)/d)·e_k`, que é um fator constante e não `e_k²`, e daí a convergência linear. Antes da correção, para Re = 1e4, cada erro era cerca de 0,04 vezes o anterior (1,9e-03, 7,6e-05, 2,9e-06), com ordem 0,99 e 10 iterações. Calculando a derivada em cada `x_k`, são 5 iterações e ordem 2,00.
* Os testes de aceitação só olham `convergiu` e o valor da raiz, que continua certo porque a iteração ainda converge para ela; nenhum confere o número de iterações nem a ordem.

## Marco 4

### R13 — Integração e descontinuidade

* As ordens 2 e 4 supõem um integrando suave em cada subintervalo. O custo de uma vez tem saltos às 18 h e às 21 h, quando a tarifa muda entre 0,50 e 1,50 R$/kWh.
* Nos n da Etapa 1(b), o salto cai dentro de um subintervalo, e o erro ali é proporcional a h × salto, não importa a regra. Por isso a ordem observada foi 1,00 no trapézio e 0,65 no Simpson, que fica irregular porque o peso dos nós vizinhos ao salto alterna entre 4 e 2.
* Por faixa, a tarifa é constante e a potência é suave em cada integral, então o salto fica nos extremos dos intervalos e não dentro deles. Voltam as ordens 2,00 e 4,00, com erro em n = 110 de 6,3e-04 no trapézio e 8,1e-08 no Simpson.

### R14 — Issue #11

* Testes de regressão: `test_trapezio_malha_nao_uniforme` e `test_volume_do_dia_com_leituras_perdidas`.
* Causa: `Trapezio.integrar_tabela` usava `h = x[1] - x[0]` em toda a tabela, supondo que as leituras eram sempre a cada 15 min. O problema é que tem 89 de 97 leituras, com intervalos de 15 e 30 min, e cada intervalo de 30 min era contado como 15. O volume deu 3547,37 m³ contra 3888,00 m³ (erro de 8,76%), mas considerando a largura de cada intervalo, deu 3896,50 m³ e erro de 0,22%.
* Os testes de aceitação só chamam `integrar_tabela` em malhas uniformes (`np.linspace` e `T` a cada 1,5 h), em que o passo fixo dá o resultado certo.
* A regra de Simpson exige malha uniforme, porque os pesos 1, 4, 2, ..., 4, 1 supõem o mesmo h em toda a tabela. O registro tem dois intervalos diferentes, então `Simpson.integrar_tabela` levanta `ValueError`, embora 89 seja ímpar.

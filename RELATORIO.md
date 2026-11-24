# Relatório — Gabriel Cypreste (3517)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente
(prog2-venv) Gabriels-MacBook-Air:Respostas-CB23-2026 ogabrielcypreste$ python marco1.py 2>&1 | head -3
=== Etapa 0: ambiente ===
Python 3.9.6 | NumPy 2.0.2 | fornecido 4.0

### R1 — Expressões regulares

Com o padrão de tag, a string "PT1010" é aceita por re.match e rejeitada por re.fullmatch. O match só exige que o começo da string case (PT101) e ignora o 0 que sobra, enquanto o fullmatch exige que a string inteira case. Se valida_tag usasse match, ela devolveria True para "PT1010", que não é uma tag válida.

### R2 — Linhas inválidas

ler_log devolve as linhas descartadas para que quem opera a estação possa contá-las e olhar o que veio corrompido, em vez de perdê-las sem aviso. Aqui foram 4 em 2404. Se derrepente centenas de linhas viessem corrompidas, seria sinal de falha de comunicação com a RTU, e descartar em silêncio deixaria lacunas nas séries de pressão sem que ninguém notasse.

### R3 — Late binding

A lambda c: c * k não guarda o valor de k, e sim uma referência à variável. Ela só lê k quando é chamada, e nessa hora o laço já terminou e k vale 0.1, o fator do FT201. A minha criar_conversores chama uma função auxiliar, _conversor(fator), que cria um escopo novo a cada chamada, então cada lambda guarda o fator da sua própria tag.

### R4 — Escala nominal

A escala nominal supõe que a pressão cresce em linha reta com a contagem ((c * 600) / 4095), mas o transmissor não responde assim. Em fornecido/simulador.py, a função p_real calcula 600 * sin((π/2) * (c/4095)), uma curva de seno. Na região perto de 1790 contagens, a curva real está bem acima da reta, por isso a conta linear dá cerca de 262 kPa e o valor de conferência é 380 kPa. Confirme olhando p_real e c_real antes de escrever.

### R5 — Previsão × medição (Etapa 3)

Não houve commit separado, as previsões foram feitas antes de rodar as medições e entram junto com o relatório.

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` |18|17.8|
| Tempo do laço / tempo vetorizado |10|49.9|
| Tempo da compreensão / tempo do laço |1|1.4|

A maior diferença foi no laço contra o vetorizado: previ 10 vezes e medi 49.9. Subestimei o custo do interpretador: no laço, cada um dos 1 milhão de elementos passa por instruções do Python e por objetos int e float criados a cada volta, enquanto o NumPy faz o mesmo laço em C, sobre memória contígua. O uint16 * 20 dá 16364 porque o uint16 só vai até 65535 e 4095 * 20 = 81900, então o valor dá a volta e faz 81900 − 65536 = 16364. Eu guardaria as contagens em uint16 (cabem em 2 bytes) e as pressões em kPa em float64 (ou float32, se a memória importar mais), porque têm casas decimais.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` |SerieTemporal|SerieTemporal|
| `s[1:]` |SerieTemporal|SerieTemporal|
| `s * 2` |SerieTemporal|SerieTemporal|
| `s.sum()` |Float|SerieTemporal|
| `s[0]` |float64|float64|

O resultado que mais me surpreendeu foi s.sum(), que devolve uma SerieTemporal de 0 dimensões e não um float. Eu achava que somar uma série daria um número comum. A soma continua correta, mas o NumPy mantém a subclasse até em resultados de um único valor, enquanto s[0] já volta como float64.

### R7 — Issue #4

O sintoma era a média móvel de 30 pontos de uma série de 600 devolver um valor a menos. Escrevi test_tamanho_do_resultado e test_valores_incluem_a_primeira_janela, que falhavam antes da correção. Isso porque np.cumsum não começa com um zero, então a soma da primeira janela (acumulada[janela-1] não tem um "antes" para subtrair e a diferença só produz as janelas seguintes. A correção foi colocar um 0.0 na frente da soma acumulada. Os testes de aceitação só conferem o tipo e os erros, nunca o tamanho nem os valores. Outro caso que eles não cobrem é a janela igual ao tamanho da série, que deve dar um único valor, e é coberto pelo meu test_janela_igual_ao_tamanho.


## Marco 2 

### Ambiente 
=== Etapa 0: ambiente ===
Python 3.9.6 | NumPy 2.0.2 | SciPy 1.13.1 | fornecido 4.0 | matrícula 3517

### R8 — Derivada numérica
De h = 1 até h = 1e-5, o erro cai de 1.66e-5 para 6.2e-10, cerca de 10 vezes a cada passo. Isso é o erro de truncamento, que é proporcional a h: a diferença adiante ignora os termos de ordem superior da série de Taylor, e eles diminuem com h. Depois de 1e-5, o erro volta a crescer (2.3e-8 em 1e-6, até 3.6e-1 em 1e-13). Aí domina o erro de arredondamento: f(x+h) e f(x) ficam quase iguais, a subtração perde algarismos significativos, e esse erro é dividido por um h cada vez menor. O melhor passo é h = 1e-5, onde os dois erros se equilibram. Em h = 1e-14, x + h arredonda para o próprio x: no terminal, 1000 + 1e-14 == 1000 dá True. Então f(x+h) − f(x) = 0, a aproximação vale 0, e o erro é |0 − derivada|, ou seja, a própria derivada (0.2134, o valor da tabela).

### R9 — Issue #7
Testes de regressão: test_um_milhao_de_pulsos, test_melhor_que_o_ingenuo e test_recupera_parcelas_menores_que_a_precisao. O código calculava t - (soma + y), e soma + y é exatamente o t que acabou de ser calculado. Em ponto flutuante o resultado é sempre zero, então a correção nunca guardava nada e o Kahan se comportava como a soma ingênua (a Etapa 2 mostra 100000.00000133288 contra 100000.0 depois da correção). Logo, corrigimos com (t - soma) - y. Algebricamente é o mesmo zero, mas em ponto flutuante a primeira subtração recupera o que foi arredondado, e a segunda isola a parte de y que se perdeu. Já a aceitação não pegou, porque o teste dela soma só 10 parcelas e compara com isclose, uma tolerância larga demais para o erro de cerca de 1e-6.

### R10 — Precisão × exatidão
Precisão é o espalhamento das leituras: o desvio de PT102 é 0.525 (linear) e 0.527 (spline), que é, praticamente, igual. Exatidão é a proximidade do valor verdadeiro (380 kPa): o viés da curva linear é −1.834 kPa e o da spline é −0.005 kPa. Em outras palavras, as duas curvas são igualmente precisas, mas só a spline é exata. A curva linear erra até 2.88 kPa na Etapa 1, contra 0.025 da spline, porque o transmissor segue um seno e a reta ignora a curvatura. A média de cerca de 595 leituras válidas reduz o erro aleatório, o erro padrão fica em torno de 0.525/√595 ≈ 0.02 kPa. Mas o viés da linear é um erro sistemático, que desloca todas as leituras para o mesmo lado, e a média não o corrige.


## Marco 3

### R11 — Bissecção × Newton
Sempre 44, pois, a bissecção divide o intervalo ao meio a cada passo e só para quando a largura fica menor que tol. O intervalo inicial é [2, 15], então o número de passos é cerca de log2(13 / tol), que dá 44 para a tolerância usada. Isso só depende da largura e da tolerância, e não da função nem do Reynolds. Ordem 2 com os seus erros: em Re = 1e4, os erros são 2.9, 5.0e-2, 2.3e-5, 5.0e-12. Cada erro é aproximadamente uma constante vezes o quadrado do anterior. Na prática, o número de dígitos corretos dobra a cada iteração. A ordem estimada deu 2.00. Tem uma situação em que o Newton falha e a bissecção não: quando a derivada é zero (ou quase) no ponto inicial ou durante o caminho, o passo f/f' explode ou nem existe (o código levanta ValueError), e há funções em que o Newton fica oscilando entre dois pontos. A bissecção só precisa que f(a) e f(b) tenham sinais opostos, então ela não depende da derivada.


### R12 — Issue #9
test_poucas_iteracoes_em_colebrook, test_raiz_de_dois_em_poucas_iteracoes e test_erro_cai_mais_rapido_que_linear são os testes de regrewsão. Contra o raizes.py original, os três falham. Calcular a derivada uma vez só deixa a convergência linear, uma vez que o passo vira x − f(x)/f'(x_0), com a derivada congelada no ponto inicial. Esse é o método da corda: a inclinação usada fica cada vez mais diferente da inclinação verdadeira perto da raiz, e o erro cai por um fator aproximadamente constante a cada passo, em vez de ser elevado ao quadrado. A aceitação não pegou, porque os testes de aceitação só conferem se o resultado final está certo (a raiz, o fator de atrito), e nunca o número de iterações nem a velocidade de convergência. O Newton com defeito chega à resposta certa, só que bem mais devagar.


## Marco 4

### R13 — Integração e descontinuidade

Integrando o custo de uma vez, o trapézio deu ordem 1,00 e o Simpson 0,65, em vez de 2 e 4. A tarifa muda de valor em 18 h e 21 h, então a função integrada é descontínua. As fórmulas de erro do trapézio e do Simpson supõem uma função suave, com derivadas limitadas. Com o salto, quase todo o erro vem do intervalo que contém a descontinuidade, e esse erro é proporcional à largura h. Por isso a ordem cai para cerca de 1 e a regra de ordem maior perde a vantagem. No Simpson a ordem ficou ainda abaixo de 1, provavelmente porque a posição do salto em relação aos painéis muda com n. Integrando cada faixa separadamente, a tarifa é constante dentro de cada uma e a função volta a ser suave. As ordens voltam a 2.00 (trapézio) e 4.00 (Simpson), e com n = 110 o erro do Simpson é 8.1e-08, contra 6.3e-04 do trapézio.

### R14 — Issue #11
Testes de regressão (classe TestTrapezioMalhaIrregularRegressao): test_malha_com_um_intervalo_maior, test_funcao_constante_em_malha_irregular e test_registro_do_dia_com_falhas. Os três falhavam antes da correção. Há também test_malha_uniforme_continua_igual, que garante que a malha uniforme não mudou. Isso porque Trapezio.integrar_tabela calculava um único h a partir do primeiro intervalo e o usava para todos. Em malha irregular, os intervalos maiores eram contados com a largura errada. A correção usa a largura real de cada intervalo, np.diff(x). Os testes de aceitação não pegaram por usarem malhas uniformes. Nelas, o único h tem a mesma largura de cada intervalo, então o defeito não aparecia.E por que o Simpson não serve para o registro do dia? Bem, ele exige pontos igualmente espaçados. O registro tem 89 leituras de 97 possíveis, com intervalos de 15, 30 e 45 min, então a malha é irregular. O Simpson se recusa a rodar (ValueError), e o trapézio com largura por intervalo dá 3874.0 m³, contra 3888.0 m³ de conferência (erro de 0.36%).

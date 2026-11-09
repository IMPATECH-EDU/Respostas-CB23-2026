# Relatório — Maria Eduarda Teixeira de Araujo Dantas (3476)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
### Ambiente

Usei Windows, então no lugar de `which python` usei `(Get-Command python).Source`.

```text
C:\Users\dudad\venvs\prog2-venv\Scripts\python.exe
Python 3.14.4 | NumPy 2.5.4 | fornecido 3.0
```

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
Uma string que re.match aceita e re.fullmatch rejeita é "PT1010". O match só exige que o começo case, então aceita PT101 e ignora o 0 que sobra. Se valida_tag usasse match, aceitaria "PT1010" e "PT101 ", que estão na lista de inválidas do enunciado.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Eu tive 4 inválidas em 2408 linhas. Devolvê-las permite contar e auditar a falha. Situação possível: se um transmissor ou a comunicação falhar por vários minutos, todas as linhas dele chegam corrompidas, e descartar em silêncio esconderia o instrumento morto.

### R3 — Late binding

<!-- Por que `errados["PT102"](4095)` dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Na compreensão, cada lambda guarda a variável `k`, não o valor dela. Quando as lambdas são chamadas, `k` já terminou o laço valendo 0,1 (a escala de FT201, a última do dicionário), e por isso errados["PT102"](4095) dá 4095 × 0,1 = 409,5. A minha criar_conversores usa `f=fator` como argumento padrão, que é avaliado na criação de cada lambda e fixa o fator de cada tag.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. --> 
Hipótese: o transmissor não responde linearmente. A escala nominal assume pressão = contagens * 600 / 4095 (uma reta), mas a curva real é curvada, e no meio da faixa ela dá valores maiores que a reta. A média de PT102 (cerca de 1791 contagens) dá 262 kPa pela escala nominal e 380 kPa de conferência.
Onde está: em fornecido/simulador.py, na função p_real, que calcula 600 * sin(0.5 * pi * c / 4095). A função tabela_calibracao() fornece justamente pontos dessa curva, o que sugere que, no mundo real, a conversão deveria usar a calibração (por exemplo, interpolando) em vez da escala nominal.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 2ee94cd

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ~18x | 18,0x (36.000.056 / 2.000.000) |
| Tempo do laço / tempo vetorizado | ~100x | 12,5x (94,10 ms / 7,53 ms) |
| Tempo da compreensão / tempo do laço | ~0,8 | 0,83 (77,88 ms / 94,10 ms) |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
A maior diferença foi no tempo vetorizado: previsto ~100x, medido 12,5x. A memória bateu: a lista usa 36 B por elemento, 8 B do ponteiro + 28 B do objeto int, contra 2 B do uint16, o que dá 18x. O vetorizado ganhou menos que o esperado porque a conta c * 600 / 4095 é muito simples, então o laço já gasta pouco por elemento, e o vetorizado ainda paga a conversão com astype e cria arrays temporários, provavelmente. A compreensão ficou perto do laço (0,83) porque as duas fazem a mesma conta em Python, e a compreensão só evita o append. O map com lambda foi o mais lento (106 ms) porque chama uma função Python por elemento.
uint16 * 20 dá 16364 porque 4095 * 20 = 81900 não cabe em 16 bits (máximo 65535), e o NumPy dá a volta: 81900 - 65536 = 16364. Para contagens eu escolheria uint16 (0 a 4095, 2 B por valor). Para pressões em kPa eu escolheria float64: uso float32 só se a memória for um problema, porque a precisão dele é menor e pode se acumular em somas longas.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | numpy.float64 | SerieTemporal |
| `s[0]` | numpy.float64 | numpy.float64 |

<!-- Explique o resultado que mais surpreendeu você. -->
O que mais me surpreendeu foi o s.sum() devolver uma SerieTemporal e não um número comum. É por isso que o marco1.py usa float(...) ao imprimir, já o s[0] volta como float64, um escalar do NumPy.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
- Sintoma: media_movel(30) sobre PT102 (600 leituras) devolvia 570 valores; a docstring prevê 571.
- Testes de regressão: test_media_movel_quantidade_de_valores (3 != 4), test_media_movel_janela_igual_ao_tamanho (0 != 1), test_media_movel_valores e test_media_movel_janela_1_devolve_a_propria_serie.
- Causa: acumulada[i] inclui self[i]. A soma da janela i é acumulada[i+janela-1] − acumulada[i-1], mas o código usava acumulada[i+janela] − acumulada[i], deslocando tudo um ponto e perdendo a primeira janela.
- Correção: um 0 no início da soma acumulada (faz o papel de acumulada[-1]) e .view(SerieTemporal), porque o concatenate devolve ndarray.
- Por que a aceitação não pegou: test_media_movel_tipo_e_erros só confere o tipo e os ValueError (janela 0 e 6); o outro uso só confere que self não muda. Nenhum confere tamanho nem valores.
- Caso não coberto: janela == len(serie) (devolvia 0 valores); coberto por test_media_movel_janela_igual_ao_tamanho.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. --> === Etapa 0: ambiente ===
Python 3.14.4 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3476

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) --> Para h grande domina o erro de truncamento, a diferença só aproxima a derivada e o erro é proporcional a h, de 1.658e-05 em h = 1 a 1.654e-08 em h = 1e-3, caindo cerca de 10 vezes a cada passo. Para h muito pequeno domina o erro de arredondamento, f(x+h) e f(x) ficam quase iguais, a subtração perde algarismos significativos e a divisão por h amplifica isso. O menor erro foi em h = 1e-5, com 6.224e-10, onde os dois efeitos se equilibram. Em h = 1e-14, "1000 + 1e-14 == 1000" dá "True", h é menor que metade do espaçamento entre floats perto de 1000, então x+h é o mesmo float que x e f(x+h) − f(x) = 0. A derivada numérica vale 0 e o erro é |0 − 0.2134|.



### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. --> Meus testes de regressão são "test_um_milhao_de_pulsos" e "test_mais_preciso_que_o_ingenuo", falhavam com o código original e passam depois da correção. Causa: "t = soma + y" já é o resultado arredondado, e na linha com defeito "soma + y" é calculado de novo e dá exatamente o mesmo float, então "t - (soma + y)" é sempre 0 e a correção nunca existe. Algebricamente isso é igual a (t - soma) - y, mas em ponto flutuante só essa ordem recupera a parte que o arredondamento perdeu. Os testes de aceitação não pegaram o defeito porque somam só 10 parcelas e comparam com "math.isclose", cuja tolerância esconde um erro dessa ordem. Ele só aparece com muitas parcelas, como no 1 000 000 da issue (total 100000.00000133288, erro de 1.333e-06 L).

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. --> Precisão é a dispersão das leituras, o desvio de PT102 é 0.522 kPa (linear) e 0.523 kPa (spline), praticamente iguais, porque o ruído aleatório do transmissor é o mesmo nas duas curvas. Exatidão é a proximidade do valor verdadeiro, a spline tem viés de 0.000 kPa e a linear, de −1.829 kPa, porque a curva linear erra a forma da calibração. A média de 595 leituras válidas reduz só o erro aleatório: o erro padrão é 0.523/√595 ≈ 0.021 kPa. O erro sistemático é igual em todas as leituras, então a média herda o viés inteiro, mais de 80 vezes maior que o erro padrão. Por isso "medir" soma a "u_sistematica" (1.5 kPa), que não diminui com o número de leituras.


## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. --> A bissecção parte de [2, 15], de largura 13, e a cada iteração a largura cai pela metade. Ela para quando 13/2^k < 1e-12, ou seja, k > log2(1,3e13) ≈ 43,6, então k = 44. Esse número só depende da largura e da tolerância, e não do Reynolds. Ordem de convergência 2 significa e_{k+1} ≈ C·e_k²: o número de dígitos corretos dobra a cada passo. Para Re = 1e4, os erros foram 5.0e-02, 2.3e-05 e 5.0e-12, cerca de 1, 4 e 11 dígitos corretos, com ordem estimada de 2.00. O Newton falha e a bissecção não quando a derivada é zero no ponto atual, então o código levanta "ValueError", ou quando o ponto inicial está longe da raiz e a iteração diverge, como em f(x) = x^(1/3) com x₀ ≠ 0, em que x_{k+1} = −2·x_k. A bissecção só exige f contínua e troca de sinal em [a, b].

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. --> Meus testes de regressão são 'test_recalcula_a_derivada_a_cada_iteracao' e 'test_converge_em_poucas_iteracoes': os dois falhavam com o código original e passam depois da correção. Com a derivada calculada uma vez só, em x₀, a iteração vira x_{k+1} = x_k − f(x_k)/f'(x₀). Como f'(x₀) ≠ f'(raiz), o erro só é multiplicado por uma constante menor que 1 a cada passo, então a convergência é linear. Recalculando f'(x_k) a cada iteração, essa constante tende a zero perto da raiz e a convergência fica quadrática. Para Re = 1e4, o relato da issue dava 10 iterações e, depois da correção, a tabela 2(a) mostra 5. Os testes de aceitação não pegaram o defeito porque só conferem se a raiz está certa, e o Newton defeituoso ainda chega à raiz certa. Nenhum deles verifica o número de iterações nem a ordem de convergência.

## Marco 4

### R13 — Integração e descontinuidade

O erro O(h²) do trapézio e O(h⁴) do Simpson só vale quando o integrando é suave. A tarifa dá saltos em 18 h e 21 h (0,50 → 1,50 → 0,50), então o custo é descontínuo. O subintervalo que contém o salto é aproximado por uma parábola ou uma reta que não enxerga o degrau, e esse erro local é proporcional a h. O erro total cai então como h, o trapézio deu ordem 1.00 e o Simpson, 0.65, menos regular porque o erro depende de onde o salto cai dentro do subintervalo para cada n. Integrando faixa por faixa, o salto fica nas extremidades e cada integrando é suave. A ordem volta a 2.00 e 4.00 (erro de 6.3e-04 e 8.1e-08 com n = 110).

### R14 — Issue #11

Meus testes de regressão são `test_reta_em_malha_irregular`, `test_constante_com_leitura_perdida` e `test_parabola_em_malha_irregular`: os três falhavam com o código original e passam depois da correção. A causa: `Trapezio.integrar_tabela` usava um passo único, `h = x[1] - x[0]`, para todos os trapézios, o que só vale com leituras igualmente espaçadas. No registro com 8 leituras perdidas, os intervalos são de 15 ou 30 min, e a conta errava o volume. Os testes de aceitação não pegaram isso porque só passam tabelas de passo constante ao trapézio, e com passo constante a fórmula errada dá o mesmo resultado da certa. A regra de Simpson não serve para o registro porque exige pontos igualmente espaçados, e `Simpson().integrar_tabela` recusa a tabela (Etapa 2a: 89 leituras, intervalos de 15 e 30 min). Com o trapézio corrigido, o volume é 3881.5 m³, com erro de 0.17%.
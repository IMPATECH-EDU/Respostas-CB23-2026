# Relatório — Wilian Martins da Silva (3551)


Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/usr/bin/python3
Python 3.14.4 | NumPy 2.3.5 | fornecido 3.0

### R1 — Expressões regulares

O `re.match` procura correspondência apenas no início, aceitando "PT101 " (com um espaço no fim). O `re.fullmatch` exige que a string inteira corresponda ao padrão. Se usássemos `match` em `valida_tag`, as strings com lixo ou espaços extra no final seriam aceites indevidamente como tags válidas, o que iria corromper a filtragem dos dados.

### R2 — Linhas inválidas

Devolver as linhas descartadas permite que o sistema seja auditado. Se o `ler_log` as ignorasse em silêncio, a equipa não conseguiria distinguir entre um período sem eventos e uma falha crítica, como uma perda de pacotes de rede ou um sensor avariado a enviar dados truncados que precisaria de intervenção de manutenção.

### R3 — Late binding

A versão `errados["PT102"](4095)` dá 409.5 porque o Python avalia a variável `k` apenas quando a lambda é chamada (*late binding*), usando o último valor assumido no laço (0.1). A nossa `criar_conversores` resolve isto com um argumento padrão (`fator=fator`), forçando a avaliação imediata (*early binding*) na criação da lambda.

### R4 — Escala nominal

A escala nominal de `PT102` supõe que a pressão é proporcional às contagens (600/4095 kPa por contagem), mas o transmissor não é linear: em `fornecido/simulador.py`, `p_real(c) = 600·sin(0,5·π·c/4095)`, uma curva senoidal. Com 380 kPa o A/D marca cerca de 1788 contagens, e a reta nominal converte isso em 261,99 kPa, mais de 100 kPa abaixo. A hipótese é erro de modelo (não linearidade), e não ruído: por isso a tabela de calibração com interpolação é necessária.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ~ 18.0x 18| ~ 18.0x (36.000.056 / 2.000.000) |
| Tempo do laço / tempo vetorizado | ~37.22 ms | ~ 33.7x (37.33 ms / 1.11 ms) |
| Tempo da compreensão / tempo do laço | 36.00 ms| ~ 1.0x (37.61 ms / 37.33 ms) |

A maior diferença reside na aceleração da versão vetorizada face ao laço (33.7x), pois o NumPy roda as operações em C compilado, ignorando o *overhead* do interpretador Python. O valor `16364` surge porque 81900 excede o limite do `uint16` (65535), causando um *overflow* ($81900 \pmod{65536} = 16364$). Escolheria `uint16` para as contagens A/D e `float32` ou `float64` para pressões em kPa.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `float` |
| `s[0]` | `float` | `float` |

O resultado que mais me surpreendeu foi que `s.sum()` e o acesso ao índice `s[0]` devolvem o tipo primitivo `float` do Python, em vez de retornarem uma série unitária ou um tipo nativo do NumPy (como `numpy.float64`).

### R7 — Issue #4

O sintoma era que a `media_movel` devolvia um valor a menos: 570 em vez de 571 para 600 pontos e janela de 30. Os meus testes de regressão são `test_600_pontos_janela_30_devolve_571`, `test_ultima_janela_e_incluida` e `test_janela_do_tamanho_da_serie`. A causa era o limite `len() - w` no `range`, que deixava de fora a última janela; o número de janelas é `len() - w + 1`, e a correção usa `sliding_window_view`, sem laço. Os testes de aceitação não falharam porque só conferiam o tipo do retorno e os erros de janela inválida, nunca o tamanho. Outro caso que eles não cobriam é a janela igual ao tamanho da série (uma única janela), coberto pelo `test_janela_do_tamanho_da_serie`.

## Marco 2

### Ambiente

Python 3.14.4 | NumPy 2.3.5 | SciPy 1.15.0 | fornecido 3.0 | matrícula 3551

### R8 — Derivada numérica

Para $h$ grande (até $\approx 10^{-5}$), domina o erro de truncamento matemático (a secante afasta-se da tangente real). Para $h$ muito pequeno, domina o erro de arredondamento de ponto flutuante. Em $h = 10^{-14}$, a limitação de precisão do `float` faz com que `1000 + 1e-14` seja exatamente `1000.0`; logo, $f(x+h) - f(x)$ dá $0$. Como a fórmula resulta em zero, a diferença entre a aproximação (0) e a derivada exata é, naturalmente, o próprio valor da derivada exata.

### R9 — Issue #7

O meu teste de regressão para esta correção foi o `test_01_kahan_regressao`. A falha ocorria porque, em `t - (s + y)`, o Python reavalia a soma `s + y` sofrendo exatamente o mesmo arredondamento que gerou `t` na linha anterior, resultando em `t - t = 0.0`. A forma correta, `(t - s) - y`, remove primeiro a parte inteira/maior, deixando o resíduo isolado. Os testes de aceitação falharam em detetar o defeito porque provavelmente testavam com poucas parcelas ou com números inteiros, onde o erro flutuante não se manifesta.

### R10 — Precisão × exatidão

A precisão está ligada ao desvio (dispersão dos dados) e reflete o ruído aleatório do sensor; como os dados brutos são os mesmos, o desvio pouco muda. Já a exatidão reflete a proximidade com a pressão real (viés). A curva linear gera um viés alto (> 0.5) porque falha em modelar a curvatura natural da resposta física do transmissor. A média de 600 leituras consegue atenuar a incerteza aleatória (melhora a precisão da média), mas é matematicamente incapaz de anular um erro sistemático intrínseco (a má calibração da curva linear).

## Marco 3

### R11 — Bissecção × Newton

A bissecção gasta sempre 44 iterações porque o seu critério de parada olha só para a largura do intervalo, nunca para `f`: o Colebrook parte sempre de `[2, 15]` (largura 13) com `tol = 1e-12`, e `13 / 2^k < 1e-12` só vale a partir de `k = ⌈log2(1,3·10¹³)⌉ = 44`, para qualquer Reynolds.
Ordem de convergência 2 quer dizer que cada erro é proporcional ao **quadrado** do anterior, `e_{k+1} ≈ C·e_k²`. Na Etapa 2(b), para Re = 10⁴, os erros foram 2,9; 5,0·10⁻²; 2,3·10⁻⁵; 5,0·10⁻¹²: o número de dígitos corretos vai de 1 para 4 e para 11, ou seja, mais que dobra a cada passo (ordem estimada: 2,00).
O Newton falha onde a bissecção não em `f(x) = x³ − 2x + 2` no intervalo `[−2, 2]`: ele parte do ponto médio, 0, vai para 1, volta para 0 e fica oscilando para sempre (`convergiu = False`), enquanto a bissecção, garantida pela troca de sinal entre `f(−2) < 0` e `f(2) > 0`, acha a raiz −1,769292.

### R12 — Issue #9

Testes de regressão (escritos antes da correção, e que falhavam no código original): `test_regressao_derivada_recalculada_a_cada_iteracao` (a derivada foi avaliada 1 vez em 23 iterações: `1 != 23`) e `test_regressao_colebrook_re_1e4_converge_quadraticamente` (o Newton levava 10 iterações; o limite do teste é 7, e depois da correção são 5).
Calcular a derivada uma vez só, em `x0`, transforma a iteração em `x_{k+1} = x_k − f(x_k)/f'(x0)`, o método da corda: um ponto fixo cuja derivada na raiz vale `1 − f'(r)/f'(x0)`, que não é zero. O erro então só é multiplicado por uma constante a cada passo (convergência linear). No Newton de verdade `f'` é reavaliada em `x_k` e essa derivada na raiz vale 0, o que dá a convergência quadrática.
Os testes de aceitação não pegaram o defeito porque só conferem o **valor final** (a raiz e o fator de atrito), que o método da corda também atinge, só que com mais iterações; nenhum deles verifica o número de iterações nem a ordem de convergência.

## Marco 4

### R13 — Integração e descontinuidade

As duas regras supõem um integrando suave dentro de cada subintervalo; a tarifa salta às 18 h e às 21 h. O subintervalo que contém o salto tem erro da ordem de h (e não de h² ou h⁴), e como há um desses subintervalos por salto, o erro global cai como O(h): a ordem observada ficou em 1,00 no trapézio e em 0,65 no Simpson (n = 30 a 110), e o Simpson perde toda a vantagem sobre o trapézio. O erro também varia conforme a posição do salto dentro do subintervalo, o que explica a ordem do Simpson ter saído abaixo de 1 num ajuste com poucos valores de n. Integrando faixa por faixa, a tarifa é constante e o integrando é suave em cada pedaço, e voltam as ordens 2,00 (trapézio) e 4,00 (Simpson), com erro de 8,1e-08 no Simpson em n = 110.

### R14 — Issue #11

**Testes de regressão** (em `testes/test_dia.py`, falhavam no código original): `test_malha_irregular_funcao_linear` (deu 3,0625 em vez de 8) e `test_leitura_perdida_na_vazao_constante` (deu 15 em vez de 20).
**Causa:** `Trapezio.integrar_tabela` usava `h = x[1] - x[0]` para todos os trapézios, supondo leituras a cada 15 min. Onde o SCADA perdeu leituras o intervalo é de 30 min, mas contava como 15, e esse trecho era subestimado. Com a minha matrícula, o volume do dia saía 3526,7 m³ contra 3888,0 m³ de conferência (erro de 9,29%). A correção usa a largura real de cada trapézio, `Σ np.diff(x)·(y[i]+y[i+1])/2`, e o volume passou a 3877,5 m³ (erro de 0,27%).
**Por que a aceitação não pegou:** todos os testes dela usam malhas uniformes (`np.arange(…, 1.5)`, `np.linspace`), em que `x[1] - x[0]` é igual a todos os passos; o caso de `vazao_registrada` só era testado quanto ao tamanho.
**Simpson:** a regra composta exige passo uniforme e número par de subintervalos. O registro tem 89 leituras com intervalos de 15 e 30 min, então a regra não se aplica e `Simpson().integrar_tabela` recusa a tabela com `ValueError`.

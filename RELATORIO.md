<<<<<<< HEAD
# Relatório — Wilian Martins da Silva (3551)
=======
# Relatório — <Wilian Martins da Silva> (3551)
>>>>>>> da03db36e70bcda7d3abf5944ceec2b439d1deda

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

A versão `errados["PT102"](4095)` dá 409.5 porque o Python avalia a variável `k` apenas quando a lambda é chamada (*late binding*), usando o último valor assumido no laço (0.1)[cite: 15]. A nossa `criar_conversores` resolve isto com um argumento padrão (`fator=fator`), forçando a avaliação imediata (*early binding*) na criação da lambda.

### R4 — Escala nominal

A escala nominal resulta em 261.99 kPa contra os 380.00 kPa de referência[cite: 7, 14]. A diferença deve-se ao facto do instrumento `PT102` estar a simular um desvio real (ruído ou falta de calibração) face à equação ideal. A explicação codificada para esta perturbação nos dados encontra-se no ficheiro da base `fornecido/simulador.py`[cite: 15].

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | [Sua Previsão] | ~ 18.0x (36.000.056 / 2.000.000) |
| Tempo do laço / tempo vetorizado | [Sua Previsão] | ~ 33.7x (37.33 ms / 1.11 ms) |
| Tempo da compreensão / tempo do laço | [Sua Previsão] | ~ 1.0x (37.61 ms / 37.33 ms) |

A maior diferença reside na aceleração da versão vetorizada face ao laço (33.7x)[cite: 7], pois o NumPy roda as operações em C compilado, ignorando o *overhead* do interpretador Python. O valor `16364` surge porque 81900 excede o limite do `uint16` (65535), causando um *overflow* ($81900 \pmod{65536} = 16364$)[cite: 7]. Escolheria `uint16` para as contagens A/D e `float32` ou `float64` para pressões em kPa.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | [Sua Previsão] | `SerieTemporal` |
| `s[1:]` | [Sua Previsão] | `SerieTemporal` |
| `s * 2` | [Sua Previsão] | `SerieTemporal` |
| `s.sum()` | [Sua Previsão] | `float` |
| `s[0]` | [Sua Previsão] | `float` |

O resultado que mais me surpreendeu foi que `s.sum()` e o acesso ao índice `s[0]` devolvem o tipo primitivo `float` do Python[cite: 7, 14], em vez de retornarem uma série unitária ou um tipo nativo do NumPy (como `numpy.float64`).

### R7 — Issue #4

O sintoma era que o tamanho da série resultante na `media_movel` tinha um valor a menos do que o tamanho matematicamente correto[cite: 15]. O meu teste de regressão é o `test_tamanho_media_movel`. A causa era o uso de `len() - w` no limite do `range`, que exclui a última iteração. A correção foi alterar o iterador para `len(self._valores) - w + 1`[cite: 13]. Os testes de aceitação não falharam porque não faziam validação ao tamanho da lista[cite: 15]. Outro caso que não cobriam era passar um tamanho de janela inválido (ex: `w <= 0`), algo que eu cobri no `test_media_movel_w_invalido`.

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
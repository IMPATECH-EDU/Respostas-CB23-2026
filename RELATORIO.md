# Relatório — Lucas Rafael Barbosa (3503)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/home/lucas/venvs/prog2-venv/bin/python

=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 1.26.4 | fornecido 3.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

"PT1010", pois, com o padrão [A-Z]{1,2}\d{1,3}, apenas a correspondência inicial é exigida pelo re.match, enquanto re.fullmatch exige que a string inteira case. Se vlaida_tag usasse match, ela diria que tags como "PT1011" passariam e os assert da 1(d) falhariam.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

Para quem chama ler_log possa contar, registrar e investigar, porque ignorar em silêncio apagaria a evidência. No log da hora vieram 4 linhas corrompidas (falhas de comunicação com a RTU e linhas truncadas). Se a RTU de uma bomba comçasse a falhar e as linhas fossem jogadas foram sem aviso, o operador só iria ver uma série com buracos, sem saber que a comunicação está caindo.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

Errados é um dicinário de lambdas que usam a váriavel k do laço de compreensão. A lambda não gaurda o valor de k, só a variável. Quando ela é chamada, o laço já terminou e k vale o último fator, 0,1 (do FT201). Então errados["PT102"](4095) = 4095 * 0,1 = 409.5. Na criar_conversoes, cada lambda é criado dentro de _conversor(fator), e cada chamada tem seu próprio fator, que não muda depois (cada tag usa o fator da sua entrada), o que não gera o problema. 

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

O transmissor não responder linearmente às contagens, e a escala nomial (600/4095) supõe uma reta. Indo para fornecido/simulador.py, p_real(c) = 600*sin(0,5*pi*c/4095) não é linear. Para c ~1800 (média das contagens normais de PT102) a reta dá ~ 260 kPa e a curva verdadeira dá ~ 380 kPa. A escala nomial só acerta nos extremos (o e 600) e subestima no meio da faixa. (Usei o simulador só para entender a diferença, não para calcular).

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 16ceca0

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 36,000,056/2,000,000 = 18 |
| Tempo do laço / tempo vetorizado | 30 | 67.06/1.08 = 62 |
| Tempo da compreensão / tempo do laço | 0,8 | 63.37/67.06 = 0,94  |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

A maior diferença foi o tempo laço/vetorizado: foi quase o dobro. O vetorizado foi mais rápido do que eu esperava. o laço roda no interpretador, elemento por elmento, criando um float a cada conta, mas o numpy faz o laço em memória contígua. (add: estava testando o código e passar uma lista no lugar do ndarray para o vetorizado fazia o tempo ser 33x maior!). 
O uint16 guarda de 0 a 65535 e 4095 * 20 = 81900 passa, mas o numpy não avisa e pega o módulo (65536), que é 16364. Com o int do python dá certo. Assim, para contagens o uint16, e para pressão o float64.


### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | Serie Temporal | SerieTemporal |
| `s * 2` | Serie Temporal | SerieTemporal|
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->

O que mais me surpreendeu foi o s.sum(). Esperava que o tipo fosse um número simples do python, e não uma SerieTemporal de zero dimensões (um ponto?). Operações e reduções do numpy usam a classe do array original para criar o resultado, e a subclasse se mantém. Para usar o total como um número comum faço float(s.sum()).

### R7 — Issue #4

Quando fazíamos media_movel(30) ao invés de 571 = 600 - 30 + 1 valores, obtíamos só 570. Isso acontecia porque a soma acumulada estava começando do índice 0, e não no valor 0, então acumulada[janela:] - acumulada[:-janela] perde a primeira janela. Então, foi
colocado um 0 no começo e retorno como SerieTemporal. Os testes estavam pegando porque estavam conferindo só tipos, erros, sem ver o tamanho dos intervalos. Um caso legal é
que a janela igual a 1 deve ser do tamanho da série, e é coberto pelo teste teste_janela_igual_ao_tamanho.

# Relatório — Esley Pires de Figueirêdo Lemos (3461)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

which python: /home/al.esley.lemos/venvs/prog2-venv/bin/python \
Etapa 0: Python 3.13.15 | NumPy 2.5.4 | fornecido 1.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
A string `"PT101 extra"` é aceita por `re.match(r"[A-Z]{1,2}\d{1,3}", s)` porque ele casa a tag no início do texto ignorando o sufixo. Contudo, `re.fullmatch` a rejeita por exigir o casamento da string inteira. Se `valida_tag` usasse `match`, aceitaria tags seguidas de lixo ou espaços (como `"PT1010"` ou `"PT101 "`), violando as regras da estação.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Retornar linhas descartadas permite monitorar a integridade física da rede SCADA. Se houver ruído, cabo solto ou interferência na linha de comunicação, o transmissor enviará pacotes truncados/corrompidos. Se o sistema descartar em silêncio, falhas graves na transmissão ficariam ocultas até a perda total do instrumento.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
Em `errados["PT102"](4095)`, a lambda lê a variável `k` do escopo externo no momento da chamada, quando o laço já terminou e `k` vale `0.1` (fator de `FT201`). Por isso devolve `4095 * 0.1 = 409.5`. Minha `criar_conversores` evita isso usando argumento padrão (`f=fator`), avaliando e fixando o valor exato no momento da criação da lambda.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
A escala nominal considera a contagem bruta do conversor A/D (0 a 4095 em 0-600 kPa). A diferença para a conferência ocorre porque o sensor `PT102` requer ajuste de calibração física (offset/ganho) e compensação atmosférica. No código da base, a explicação está no simulador (`fornecido/simulador.py`), na função de geração da pressão física.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `2041cac`

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | Aproximadamente 18 vezes maior | 18.00 vezes maior |
| Tempo do laço / tempo vetorizado | Maior que 5; espero que o laço seja muito mais lento | 21.95 vezes mais rápido |
| Tempo da compreensão / tempo do laço | Menor que 1; espero que a compreensão seja mais rápida | 1.08 vezes (0.92x o tempo do laço) |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
A maior diferença foi o ganho de desempenho da vetorização NumPy, que opera diretamente em blocos C continuos de memória. Em `uint16`, `4095 * 20` dá `81900`, estourando o limite de 65535 (`81900 % 65536 = 16364`). Escolheria `uint16` para guardar contagens cruas (0 a 4095) e `float32` para pressões em kPa.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float64` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

<!-- Explique o resultado que mais surpreendeu você. -->
O resultado mais surpreendente foi `s.sum()` retornar `SerieTemporal` em vez de um escalar nativo (`float64`), devido ao comportamento do NumPy ao invocar reduções numéricas sobre subclasses diretas de `ndarray`.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
Sintoma: `media_movel(30)` de 600 pontos devolvia 570 valores em vez dos 571 esperados. Teste de regressão: `test_media_movel_tamanho_correto`. Causa: a diferença entre os fatiamentos da soma acumulada (`acumulada[janela:] - acumulada[:-janela]`) perdia um elemento na contagem de intervalos. Correção: inserção do elemento neutro `0.0` no início com `np.insert(self, 0, 0.0)`. Os testes de aceitação originais usavam listas curtas e não verificavam o tamanho exato relativo ao contrato. Outro caso não coberto é o teste de retenção de tipo da classe e a reamostragem com sobras descartadas, coberto por `test_reamostrar_com_sobra`.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->
Python 3.14.6 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3461

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->
Para h variando de 1 até 1e-5, domina o erro de truncamento da diferença finita (da ordem de O(h)), diminuindo à medida que h se reduz. Abaixo de 1e-5, passa a predominar o erro de arredondamento da máquina gerado pelo cancelamento catastrófico ao subtrair números quase idênticos e dividir por um h extremamente pequeno. Em h = 1e-14, como 1000 + 1e-14 == 1000 no padrão IEEE 754 de 64 bits, a diferença f(x+h) - f(x) resulta exatamente em zero; logo, a derivada aproximada é 0 e o erro é a própria derivada exata (0.2134).

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->
Testes de regressão: `test_kahan_um_milhao_de_pulsos` e `test_kahan_difere_de_acumulador_ingenuo`. Na expressão `t - (s + y)`, como `t` foi atribuído como `s + y`, recalcular `s + y` gera exatamente `t`, zerando a correção e anulando a compensação de Kahan. Já na ordem `(t - s) - y`, `t - s` cancela os bits mais significativos e recupera a parcela de `y` efetivamente absorvida pela soma; ao subtrair `y`, resta a fração perdida pelo arredondamento. Os testes de aceitação não capturaram o defeito por testarem apenas 10 parcelas de 0.1, magnitude em que o erro acumulado ainda não surge.

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->
Precisão diz respeito à repetibilidade e dispersão aleatória das leituras, refletida no desvio padrão praticamente idêntico em ambas as curvas (~0.52 kPa). Exatidão corresponde à aderência ao valor real da grandeza física, caracterizada pelo viés (-1.866 kPa na linear vs -0.037 kPa na spline). A média de 600 pontos reduz a incerteza estatística proveniente do ruído aleatório das medidas (erro padrão da média), mas não é capaz de diminuir o erro sistemático inerente ao modelo linear de interpolação, que possui um viés fixo frente à resposta não linear do transmissor.


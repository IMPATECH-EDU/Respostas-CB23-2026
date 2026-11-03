# Relatório — Felipe Beck Santor (3549)

<!--Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.-->

## Marco 1

### Ambiente

- Saída de "which python":
```bash
/home/al.felipe.santor/venvs/prog2-venv/bin/python`
```
- Etapa 0 do marco1.py:
```bash 
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 2.0
```

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

### R1 — Expressões regulares

- Exemplo que "re.match" aceita e "re.fullmatch" não aceita:
`AB123 coisa`

Isso implica que a função "valida_tag" irá apenas aceitar tags que cumprirem com os requisitos e não se extenderem para além do tamanho requisitado.

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

"ler_log" deve devolver as linhas descartadas pois é uma boa prática mostrar ao usuário a razão do erro, ou ao menos, o que resultou em erro. Por exemplo, se uma tag for lançada de maneira incorreta, e não soubermos qual tag foi, precisariamos analisar todas as tags e fazer uma verificação manual em cada uma para poder corrigir o erro.
<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

### R3 — Late binding

"errados\["PT102"](4095)" tenta converter as contagens em kPa, porém, devido ao Late Binding, este guarda uma função lambda c: c * k, com k = 0.1, ao invés de k = 600/4095, pois k recebe o valor 0.1 em sua última atribuição de "escalas". Já em "criar_conversores", consertamos esse erro ao criar uma variável auxiliar e determinar o valor do parâmetro da função lambda igual à essa variável (como default value), ao invés de passar essa variável diretamente como parâmetro, lambda c, f=fator: c * f [...], assim evitando o Late Binding. 
<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

A diferença é esperada pelo assert: o item 2(f) usa uma conversão linear nominal para calcular a pressão, enquanto o simulador gera as contagens com um modelo não linear.

Em marco1.py, o fator de PT102 é 600 / 4095. Aplicado à média das contagens normais, ele dá cerca de 261,9 kPa. O valor de referência é 380 kPa, então a diferença é de aproximadamente 118,1 kPa — e por isso abs(p_nominal - verdade["pressao_recalque"]) > 100 passa.

Em simulador.py temos as seguintes funções com as suas respectivas funcionalidades:
- `p_real` calcula a pressão com uma função seno.
- `c_real` calcula a operação inversa para gerar contagens a partir da pressão de referência.
- `gerar_log` usa esse modelo para gerar as leituras de PT102 e acrescenta cinco leituras falsas; a condição <= 2000 em marco1.py as exclui da média.

Com a minha matrícula, a média das contagens normais é aproximadamente 1787,8. Pelo modelo real, isso corresponde a cerca de 380 kPa; pela escala linear simplificada, dá aproximadamente 261,9 kPa. A comparação mostra que a escala nominal não representa a curva real do transmissor nessa faixa.
<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 909ed5f <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` |cerca de 18x               |17,85x |
| Tempo do laço / tempo vetorizado       |vetorizado é bem mais veloz|25.9x  |
| Tempo da compreensão / tempo do laço   |tempos similares           |1.1x   |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s`   |SerieTemporal  |SerieTemporal| 
| `s[1:]`   |float          |SerieTemporal|
| `s * 2`   |SerieTemporal  |SerieTemporal|
| `s.sum()` |float          |SerieTemporal|
| `s[0]`    |float          |float64      |

Fique surpreso que previ três floats, mas só veio um. O resultado que mais me supreende é como s.sum() retorna uma SerieTemporal. Pensava que estariamos somando os floats contidos em uma SerieTemporal, e portanto iriamos receber um float em retorno. Vou ter que dar uma olhada nessa função.

<!-- Explique o resultado que mais surpreendeu você. -->

### R7 — Issue #4

**Sintoma:**
Função `media_movel` em `elevatoria\serie.py` estava retornando um dado a menos do que deveria, de acordo com docstring. Mas apesar disso, passsava nos testes de aceitação. 
**Causa:**
Havia um deslocamento de índice em `np.cumsum`, por isso, a função não estava considerando a primeira janela.
**Correção:**
Adicionamos um zero no início da variável `acumulada`, para evitar esse deslocamento de índice. Além disso, tive que garantir que a função retornava uma `SerieTemporal`, pois sem essa parte, não passava nos testes.
**Por que os testes não pegaram o defeito antes?**
Isso aconteceu porque o teste não verifica se os valores estão certos, nem se a quatidade de valores está certa, apenas verifica se janelas inválidas realmente estão sendo tratadas como inválidas, levantando `ValueError`, e se o tipo que a função retorna está correto (ou seja, retorna uma `SerieTemporal`)
**Testes que implementei:**
Os testes que implementei em `testes\test_dados.py` cobrem tanto o tamanho da janela quanto os valores que a função retorna, assim garantindo o bom funcionamento da função.

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

## Marco 2

### Ambiente
```bash
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.3 | SciPy 1.18.0 | fornecido 4.0 | matrícula 3549
<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->
```
### R8 — Derivada numérica

Para calcular a derivada, estamos tomando a definição $\frac{f(x+h) - f(x)}{h}$, e diminuindo os valores de $h$, tomando uma espécie de limite.
Conforme $h$ diminui a partir de um valor relativamente grande, o erro também diminui, até alcançar um ponto de equilíbrio entre o truncamento e o erro de arredondamento ($h$ = 1e-05), depois volta a aumentar para $h$ pequeno, onde a diferença entre $f(x+h)$ e $f(x)$ fica muito pequeno, e é aumentado pela divisão por $h$.
Temos $c = 1000$, onde $c$ é um `float` de precisão dupla. E o intervalo entre números que podemos representar com esse tipo de dado é da ordem de $10^{-13}$, assim, quando $h = 10^{-14}$, a soma em ponto flutuante arredonda de volta para 1000, de onde $x + h = x$. Tomando então $f(x+h) - f(x) = f(x) - f(x) = 0$, temos que a derivada zera, e portanto o erro é a própria derivada.
Adicionei um teste em `testes\test_medicao`, verificando que `1000 + 1e-14 == 1000` retorna `True`.
<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

### R9 — Issue #7

Para determinar o problema da Issue #7, montei os seguintes testes em `test_medicao`: `test_soma_1000x1e_6`; `test_soma_um_milhao_de_decimos`; `test_soma_dez_mil_de_decimos`.
A causa do erro estava no fato de que `t` recebia o valor `self._soma + y` e depois `correção` recebia `t - (self._soma + y)`, ou seja, `t - t = 0`. Portanto, `self._correcao` permanecia zerada e a correção da soma de Kahan não era utilizada.
Trocando a outra expressão por `self._correcao = t - self._soma - y`, fazemos as contas em uma ordem diferente, assim garantindo que a corração pegue o erro e corrija logo a seguir.
Os testes de aceitação não pegam o erro porque somam apenas 10 termos e utilizam `math.isclose()` para fazer a verificação, assim passam. Por isso fiz testes que somam mais termos e utilizam `AssertAlmostEqual` para fazer a verificação.

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->

### R10 — Precisão × exatidão

A aproximação linear traça linhas retas entre os pontos da função, enquanto o spline aproxima a função por um polinômio. Além disso, sabemos que o desvio padrão é uma medida de precisão, e também que, o viés é uma medida de exatidão, é a diferença entre a média estimada e a pressão de referência, ou seja, mede o quanto que a estimativa difere do valor verdadeiro.
A partir disso, notamos que a spline consegue fazer aproximações mais exatas, já que aproxima a função por um polinômio. Ao mesmo tempo, ambas possuem um desvio padrão semelhante, ou seja, têm a capacidade de aproximar os pontos de uma função com uma precisão semelhante.
A média de quase 600 leituras reduz a variação aleatória, mas não corrige o erro sistemático da curva, já que, se cada leitura, convertida com uma curva, tende a "subestimar" a o valor da pressão, a média dos pontos dessa curva manterá essa subestimação, assim propagando o erro. E é por isso que a spline pode ter média e desvio bastante parecidos mas um viés bem diferente.


<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->
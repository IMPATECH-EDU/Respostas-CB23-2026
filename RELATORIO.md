# Relatório — WEDYSON DOUGLAS DA SILVA BEM (3490)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
Saida de `which python`: `/home/al.wedyson.bem/venvs/prog2-venv/bin/python`
Saida de Etapa 0 do `python marco1.py`: `=== Etapa 0: ambiente === Python 3.13.15 | NumPy 2.5.4 | fornecido 4.0`

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
Sabemos que `re.match` verifica se apenas o começo da string dada no argumento é igual, enquanto `re.fullmatch` verifica se a string por completo é igual ao padrão que desejamos analisar. Assim, se passarmos a string `"PT101 abc"` temos que o primeiro método aceita, mas o segundo rejeita. Evidentemente, uma consequência disso é que se em `valida_tag` usássemos o primeiro método ocasionaria de não cobrirmos esse caso, ou seja, não validaríamos por inteiro a string analisada, mas analisariamos apenas o seu início.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Além de ser vantajoso termos às linhas onde vemos leituras e/ou dados falhos, se não devolvessemos estaríamos, de certa forma, perdendo uma parcela do conteúdo original das linhas. Com isso, descartaríamos informações que nos permitiria identificar leituras falhas, e, portanto, poderíamos não ser capaz de encontrar uma falha no sistema. Por exemplo, uma linha registra um alarme da estação elevatória, mas está mal formatada. Se ela for descartada sem aviso, a equipe de manutenção pode não perceber que houve uma condição de alarme.
### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
O problema deriva do fato das funções lambdas serem `Late binding`, ou seja, não armazenam automaticamente o valor de `fator` existente no momento em que são criadas. Dessa forma, quando são executadas, todas elas consultam o último valor armazenado pela variável depois do último laço, utilizando o último fator disponível. Por isso, `errados["PT102"](4095)` retorna `409.5`, pois ele é resultado de `4095 * 0.1`, em que `0.1`foi o último valor armazenado.
Por essa razão a função `criar_conversores` é usada para corrigir esse comportamento, fazendo isso através do trecho `f=fator` como argumento padrão da `lambda`. Com isso, cada função captura o fator correspondente à sua própria iteração e realiza a conversão corretamente.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
No código da `Etapa 2(f)`calculamos a pressão nominal de maneira linear. No código, somamos uma certa quantidade de valores que são todos menores ou iguais a 2000, e depois dividimos por 600 (isso se apresenta como uma boa hipótese também), o que evidencia seu caráter linear. Todavia, em `simulador.py` temos a função que calcula o valor real da pressão, onde vemos uma maneira não linear de se calcular. O que indica, possivelmente, que a justificativa dessa diferença estar na maneira a qual ambas são calculadas.
### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- cole o hash curto do commit de previsões -->

Hash Curt do commit: `076e08f`

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | `17 vezes` | `18 vezes`|
| Tempo do laço / tempo vetorizado | `10 vezes`| `|
| Tempo da compreensão / tempo do laço | `1.2 vezes`| |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

Sabemos que o formato uint16 suporta valores de 0 até 65535. Sendo assim, ao realizarmos a linha `estouro = np.array([4095], dtype=np.uint16) * 20`, teriamos 81.900 que é um valor muito maio do que o suportado pelo tipo `uint16` (processo de overflow). Nesse sentido, o numpy não consegue armazenar esse número e "reinicia" a contagem resultando em [81900-65536]=[16364].
Acerca do dtype para contagens e para kPa, uma boa escolha seria, para o primeiro, `uint16`. Isso pois esse dtype só armazena números não negativo (contagens é um número de 12 bits e, logo, entre 0 e 4095) e vai no máximo até 65535. Veja ainda que `uint8` não poderia ser uma escolha já que ele abrange apenas número de 0 até 255. 
Por fim, para a medição de `kPa` poderíamos escolher o dtype de `float64`, que poderia nos fornecer uma boa precisão acerca dos valores captados em `kPa`.
### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | |
| `s[1:]` | `SerieTemporal` | |
| `s * 2` | `SerieTemporal` | |
| `s.sum()` | `SerieTemporal` | |
| `s[0]` | `SerieTemporal` | |

<!-- Explique o resultado que mais surpreendeu você. -->
Espera-se que o tipo a ser observado seja da mesma classe já que na implementação da mesma temos que ela estar a herdar `np.ndarray`. Isto é, essas operações devem estar todas definidas e dadas pela própria classe `np.ndarray`.


### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

O sintoma era a `media_movel` retornar 570 valores para 600 leituras com janela 30, quando deveria retornar 571. O teste de regressão `test_media_movel_tamanho_correto` identifica esse erro, justamente usando, além desse caso como exemplo, uma situação simples com os valores [1, 2, 3, 4, 5]. A causa era o cálculo da soma acumulada sem um zero inicial, que fazia a primeira janela ser perdida. 
Podemos corrigir esse erro ao inserir um `0.0` no início da soma acumulada com `np.insert`, permitindo calcular todas as janelas e mantendo o retorno como `SerieTemporal` ao realizarmos, na linha do return, o método `view(SerieTemporal)`. Os testes de aceitação não detectaram o defeito porque verificavam o tipo de retorno e os erros para janelas inválidas, mas não a quantidade nem os valores calculados. Outro caso não coberto era verificar os valores exatos das médias; isso é coberto pelo teste `test_media_movel_valores_corretos`, usando `[1, 2, 3, 4, 5]` e janela 2.
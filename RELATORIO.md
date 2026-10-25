# Relatório — Marco Antonio Smiguel Dacoregio (3537)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

/home/marco/venvs/prog2-venv/bin/python

=== Etapa 0: ambiente ===
Python 3.12.3 | NumPy 2.5.4 | fornecido 2.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

`"FT201     "` (possui 5 espaços a mais no final). E tomando um padrão igual ao usado em valida_tag: `TAG: re.Pattern = re.compile(r"[A-Z]{1,2}\d{1,3}")`.

O `re.match` verifica se o padrão se cumpre a partir do inicio da string e ignora oque sobrar. Nesse caso o `re.match` SIM aceita a string, pois ignora os 5 espaços a mais.

O `re.fullmatch` verifica se o padrão se cumpre em toda a string. Nesse caso o `re.fullmatch` NAO aceita a string, pois existem espaços a mais.

Se `valida_tag` usasse `re.match` ele iria retornar True para strings que deveria barrar, como: `"PT101 "` (sobra de caracteres).

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

O `ler_log` devolve as linhas descartadas para que quem o chamou possa contá-las e conferi-las, em vez de perdê-las. 
No meu log foram 2404 registros válidos e 4 linhas inválidas. Se, num dia ruim, uma falha de comunicação com os instrumentos deixasse centenas de linhas inválidas e elas fossem ignoradas em silêncio, as médias ainda pareceriam normais, mas a estação ficaria horas sem alguns instrumentos e ninguém seria avisado.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

A lambda `lambda c: c * k` não guarda o valor de `k`: ela lê a variável `k` só no momento em que é chamada. Quando chamo `errados["PT102"](4095)`, o laço já terminou e `k` vale 0,1 (o fator de `FT201`, o último do dicionário), então o resultado é 4095 × 0,1 = 409,5. Na minha `criar_conversores`, cada tag chama `_com_fator(fator)`, e cada chamada tem o seu próprio `fator`, que a lambda de dentro guarda. Por isso `certos["PT102"](4095)` dá 600,0.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

A escala nominal (600/4095) supõe que a pressão é proporcional às contagens. Por ela, a média normal de PT102 dá 261,9 kPa, contra 380 kPa de conferência. 
Minha hipótese é que o transmissor simulado não responde de forma linear, e a reta subestima a pressão. No código da base, em `fornecido/simulador.py`, a função `p_real` calcula `600 * sin(0,5 * pi * c / 4095)`, e `c_real` faz a conta inversa com `arcsin`. Com contagens perto de 1790, essa curva dá cerca de 380 kPa.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 2993572

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | cerca de 1,2 | 18,0 |
| Tempo do laço / tempo vetorizado | cerca de 2 | 43,1 |
| Tempo da compreensão / tempo do laço | cerca de 1 (iguais) | 0,78 |


<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->



### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | ndarray | SerieTemporal |
| `s[1:]` | ndarray | SerieTemporal |
| `s * 2` | ndarray | SerieTemporal |
| `s.sum()` | ndarray | SerieTemporal |
| `s[0]` | ndarray | float64 |

<!-- Explique o resultado que mais surpreendeu você. -->

Previ `ndarray` para tudo e errei: `s + s`, `s[1:]` e `s * 2` devolveram `SerieTemporal`, porque a classe herda de `np.ndarray` e o NumPy mantém o tipo da subclasse nessas operações. O que mais me surpreendeu foi `s.sum()`, que também devolveu `SerieTemporal` e não um número simples, embora seja um valor só. Já `s[0]` devolveu `float64`: um elemento sozinho é um número, e não uma série.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

Sintoma: `media_movel(30)` em 600 pontos devolvia 570 valores, e não 571, e o `assert` do `marco1.py` falhava. Testes de regressão: `test_tamanho_do_resultado` e os outros quatro de `TestMediaMovelRegressao` (5 FAIL antes da correção). Causa: o `np.cumsum` não começa em zero, então `acumulada[janela:] - acumulada[:-janela]` perde a primeira janela. Correção: colocar `0.0` na frente da soma acumulada com `np.concatenate` e devolver `SerieTemporal` com `.view`. Os testes de aceitação só conferem o tipo, as janelas inválidas e que a série original não muda, nunca o tamanho nem os valores. Um caso que eles não cobrem é janela igual ao tamanho da série (dava 0 valores), que o `test_janela_igual_ao_tamanho` cobre.

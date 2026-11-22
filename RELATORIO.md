# Relatório — Angelo José Juvino Berres (3522)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Ambiente `uv` (`venv`) no Windows fora do repositório (`where.exe` / executável):
`C:\Users\angel\AppData\Local\Temp\prog2-venv\Scripts\python.exe`

```text
=== Etapa 0: ambiente ===
Python 3.14.5 | NumPy 2.5.2 | fornecido 4.0
```

### R1 — Expressões regulares

A string `"PT101 "` (ou `"PT1010"`) é aceita por `re.match` porque o padrão casa com o prefixo `"PT101"`, mas é rejeitada por `re.fullmatch`, que exige casamento da string inteira. Se `valida_tag` usasse `re.match`, tags corrompidas ou com sufixos inválidos seriam aceitas silenciosamente como tags válidas.

### R2 — Linhas inválidas

Devolver `invalidas` permite auditar quantas e quais linhas falharam no parser, separando silêncio operacional de perda de telemetria. Se `ler_log` descartasse erros em silêncio, uma RTU com falha intermitente enviando mensagens truncadas durante um pico de recalque esconderia alarmes críticos (`ALARME PT102`) e comprometeria a confiabilidade das médias.

### R3 — Late binding

Na expressão `errados`, todas as lambdas capturam a mesma variável de laço `k`, que ao final do loop vale `0.1` (`FT201`), fazendo `errados["PT102"](4095)` retornar `409.5`. Em `criar_conversores`, a função auxiliar `_criar_multiplicador(fator)` cria um escopo léxico próprio a cada chamada, prendendo o fator da respectiva tag na closure da lambda.

### R4 — Escala nominal

Na Etapa 2(f), a escala nominal produziu `261.97 kPa` contra `380.00 kPa` de referência porque a resposta do transmissor não é linear. A explicação está em `fornecido/simulador.py`, na função `p_real(c) = 600.0 * np.sin(0.5 * np.pi * c / 4095.0)`: a curva senoidal faz cerca de 1788 contagens corresponderem a ~380 kPa, e não à proporção direta.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `b5a2b85`

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ~18× | 18.00× (36 000 056 / 2 000 000 B) |
| Tempo do laço / tempo vetorizado | ~25× | 39.68× (127.272 / 3.207 ms) |
| Tempo da compreensão / tempo do laço | ~0,7× | 0.926× (117.897 / 127.272 ms) |

A maior diferença ocorreu na aceleração do vetorizado (`39.68×` medido vs `~25×` previsto), porque a operação em C sobre memória contígua evita o custo de interpretar 1 milhão de iterações e alocar objetos `float` em Python. Em `uint16`, `4095 * 20 = 81900` ultrapassa `65535` e dá overflow modular (`81900 % 65536 = 16364`). Escolheria `uint16` para contagens (2 B/elem, convertendo para float antes de operar) e `float64` para pressões em kPa pela precisão numérica.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float | SerieTemporal |
| `s[0]` | float | float64 |

O resultado mais surpreendente foi `s.sum()` retornar `SerieTemporal` (um array 0-D), e não `float` nem `float64`: como `SerieTemporal` herda de `np.ndarray` sem customizar `__array_wrap__`, reduções mantêm o tipo da subclasse em 0-D. Já `s[0]` devolve o escalar `np.float64` em vez de `float` nativo, enquanto operações vetorizadas e fatias preservam `SerieTemporal`.

### R7 — Issue #4

O sintoma era `media_movel(30)` sobre 600 pontos devolver 570 valores em vez de 571. Os testes de regressão são `test_media_movel_tamanho_e_primeira_janela`, `test_media_movel_janela_igual_ao_comprimento` e `test_media_movel_janela_unitaria`. A causa era `acumulada[janela:] - acumulada[:-janela]` omitir `S_0 = 0`, descartando a 1ª janela; corrigi prefixando `0.0` em `acumulada`. A aceitação não pegou porque verificou só tipo e exceções, sem checar comprimento nem valores; outro caso omitido foi `ler_log` com linhas vazias ou datas impossíveis, coberto em `TestLerLogContrato`.

## Marco 2

### Ambiente

```text
=== Etapa 0: ambiente ===
Python 3.14.5 | NumPy 2.5.2 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3522
```

### R8 — Derivada numérica

De `h = 1` até `h = 1e-5` (erro cai de `1.658e-05` para o mínimo `6.224e-10`), domina o erro de truncamento `O(h)` da diferença adiante. Para `h < 1e-5`, o erro volta a crescer até `2.134e-01` pelo erro de arredondamento e cancelamento catastrófico em `(f(x + h) - f(x)) / h`, que escala com `O(ε / h)`. Em `h = 1e-14`, `1000.0 + 1e-14 == 1000.0` em `float64` (abaixo da resolução em torno de `1000`), zerando o numerador e tornando o erro exatamente igual à própria derivada (`0.213432888873`).

### R9 — Issue #7

Os testes de regressão são `test_kahan_um_milhao_de_decimos` e `test_kahan_preserva_parcelas_pequenas_apos_numero_grande`. Como `t` já é o resultado arredondado de `self._soma + y`, calcular `t - (self._soma + y)` subtrai dois floats idênticos e devolve sempre `0.0`. Já `(t - self._soma) - y` isola a parcela que realmente alterou `self._soma` e recupera os bits descartados. Os testes de aceitação não detectaram a falha porque somavam apenas 10 parcelas de `0.1` com `math.isclose` (`rel_tol=1e-9`).

### R10 — Precisão × exatidão

Em `PT102` (Etapa 3b), as curvas linear e spline têm desvios quase idênticos (`0.552` e `0.554 kPa`), ou seja, a mesma precisão (baixa dispersão entre leituras). Já a exatidão é muito diferente: o viés frente aos `380.00 kPa` reais é `-1.836 kPa` na linear contra `-0.006 kPa` na spline. A média de quase 600 leituras atenua apenas o ruído aleatório (`σ/√n`), mas não consegue corrigir o erro sistemático introduzido pela aproximação linear sobre a curva senoidal.

## Marco 3

### R11 — Bissecção × Newton

A bissecção gasta sempre 44 iterações porque `Colebrook` fixa `[a, b] = [2, 15]` e `tol = 1e-12`, exigindo `ceil(log2(13 / 1e-12)) = 44` cortes independentemente de `Re`. Nos erros do Newton para `Re = 1e4` (`2.9`, `5.0e-02`, `2.3e-05`, `5.0e-12`), a ordem 2 indica `e_{k+1} ∝ e_k²`: o número de casas decimais corretas aproximadamente dobra a cada passo. Se a função tiver derivada nula no ponto médio ou o passo tangente escapar do domínio/oscilar, o Newton falha, enquanto a bissecção segue garantida pela troca de sinal.

### R12 — Issue #9

Os testes de regressão são `test_newton_colebrook_converge_em_poucas_iteracoes` e `test_newton_reavalia_derivada_em_pontos_distintos`. Avaliar `f'(x_0)` uma única vez fixa a inclinação e transforma o processo em ponto fixo `x_{k+1} = x_k - f(x_k)/f'(x_0)`, cujo fator assintótico `|1 - f'(r)/f'(x_0)| ≠ 0` deixa a convergência linear (levando 10 passos para `Re = 1e4` em vez de 5). A aceitação não pegou o bug porque conferia só `convergiu` e a raiz final, sem verificar iterações nem ordem.

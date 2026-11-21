# Relatório — Arthur Adriano Jacometi Barbosa (3544)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
/home/al.arthur.barbosa/venvs/prog2-venv/bin/python

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

- A string `"PT101 extra"` (ou `"PT101\n"`) é aceita por `re.match(r"[A-Z]{1,2}[0-9]{1,3}", s)` porque `match` ancora apenas no início da string e ignora o sufixo, mas é rejeitada por `re.fullmatch`, que exige correspondência do início ao fim.
- Em `valida_tag`, usar `re.match` aceitaria tags malformadas que começam com um código válido (como `"PT1010"` ou `"PT101 "`), permitindo a entrada de identificadores inválidos no sistema.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
- `ler_log` devolve `invalidas` para permitir auditoria e diagnóstico de falhas de coleta ou formatação sem interromper o processamento dos registros válidos.
- Em uma estação elevatória, descartar linhas em silêncio esconderia falhas intermitentes de um sensor (como perda de comunicação ou firmware enviando campo corrompido), mascarando períodos sem monitoramento de pressão ou nível.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
- Na compreensão `{tag: (lambda c: c * k) ...}`, `k` não é capturado por valor a cada iteração, mas buscado no escopo envolvente apenas quando a função é chamada (*late binding*); ao fim do laço, `k` vale `0.1` (escala de `"FT201"`), fazendo `4095 * 0.1 = 409.5`.
- Em `criar_conversores` (`elevatoria/dados.py`), o parâmetro padrão `f=fator` avalia e vincula o valor numérico atual no momento em que cada `lambda` é criada, preservando a escala correta de cada tag.


### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

- A diferença ocorre porque o transmissor PT102 possui offset de zero vivo (4–20 mA, onde a contagem mínima 819 corresponde a 0 kPa, e não 0) ou curva de calibração distinta da escala linear simples `600 / 4095`.
- No código da base (`fornecido/simulador.py`), a geração das contagens de pressão aplica essa relação afim com offset/calibração real da planta ao calcular `verdade["pressao_recalque"]`.


### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: c6a157d

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ~14x | 18,00x|
| Tempo do laço / tempo vetorizado | ~10x | 21,96x |
| Tempo da compreensão / tempo do laço | ~0,90x | 0,93x |
<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

- **Previsão × medição e overflow:** A maior diferença costuma aparecer na aceleração vetorizada (21,96× medido: 2,077 ms contra 45,599 ms do laço) porque o NumPy executa a operação em C sobre memória contígua sem *overhead* de interpretador nem *boxing* de objetos `int`/`float`; já `np.array([4095], dtype=np.uint16) * 20` resulta em `16364` porque o produto `81900` excede o máximo de 16 bits sem sinal ($65535$) e sofre *wrap-around* módulo $2^{16}$ ($81900 - 65536 = 16364$).
- **Escolha de `dtype`:** Para contagens do ADC (inteiros de 0 a 4095), `uint16` é ideal por representar exatamente o intervalo sem desperdício de memória (2 B/elemento); para pressão em kPa (grandezas físicas contínuas e frações), `float32` ou `float64` evita truncamento decimal e estouro em cálculos intermediários.
### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float` | `float64` |
| `s[0]` | `float` | `float64` |

<!-- Explique o resultado que mais surpreendeu você. -->

O resultado que mais surpreendeu foi `s[0]` e `s.sum()` retornarem `np.float64` em vez do `float` nativo do Python, enquanto operações vetoriais (`s + s`, `s * 2`) e fatiamentos (`s[1:]`) preservam automaticamente a subclasse `SerieTemporal` graças ao mecanismo de `__array_finalize__` / *views* do NumPy.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

- **Sintoma e regressão:** Para uma série de $n$ pontos e janela $k$, `media_movel` devolvia $n - k$ valores em vez de $n - k + 1$ (ex.: 570 para $n=600, k=30$), descartando a primeira janela; coberto pelo teste `TestMediaMovel.test_media_movel_simples`.
- **Causa e correção:** O código original fazia `acumulada[janela:] - acumulada[:-janela]` diretamente sobre `np.cumsum(self)`, omitindo a diferença `acumulada[janela - 1] - 0` da primeira janela; a correção insere `0.0` no início da soma acumulada (`np.insert(np.cumsum(self), 0, 0.0)`), alinhando os índices.
- **Lacuna nos testes:** Os testes de aceitação verificavam apenas propriedades gerais (como tipo de retorno ou valores internos) sem checar o comprimento exato $n - k + 1$ nem casos de borda como $k = n$ (que antes devolvia série vazia), caso coberto pelo meu teste `TestMediaMovel.test_media_movel_janela_total`.

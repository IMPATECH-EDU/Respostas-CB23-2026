# Relatório — Matheus Ferreira Lucena (3548)

## Marco 1

### Ambiente

/home/matheus/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.13.13 | NumPy 2.5.3 | fornecido 1.0

### R1 — Expressões regulares

`re.match` aceita o prefixo `PT101` da string `PT1010`, enquanto `re.fullmatch` rejeita a string inteira; caso `valida_tag` usasse `match`, consideraria válida uma entrada que tem caracteres excedentes.


### R2 — Linhas inválidas

Devolver linhas descartadas possibilita a contagem de falhas e a investigação de sua origem a partir do conteúdo original.
Por exemplo, uma falha de comunicação com a RTU poderia interromper as leituras de pressão de PT102; ignorar essas linhas esconderia a perda de monitoramento da estação.

### R3 — Late binding

As lambdas de `errados` consultam `k` quando são chamadas. Ao terminar a compreensão, essa variável contém o fator 0.1, por isso retorna 409,5 que é resultado de `4095 * 0.1`. 
Em `criar_conversores`, `fator=fator` é avaliado na criação de cada lambda, preservando o fator da tag.

### R4 — Escala nominal

Uma hipótese inicial seria que a escala nominal não representa a resposta real do transmissor.
Em `fornecido/simulador.py`, encontrei `p_real(c) = 600*sin(0.5*pi*c/4095)` e sua inversa, `c_real`.
O simulador gera PT102 com essa curva, mas a conversão nominal usa a relação linear `c*600/4095`.
A diferença entre essas relações explica os aproximadamente 262 kPa nominais diante dos 380 kPa de conferência.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d9bcd37

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18,000028 |
| Tempo do laço / tempo vetorizado | 20 | 55,118618 |
| Tempo da compreensão / tempo do laço | 0,8 | 0,830354 |

A maior diferença foi laço/vetorizado: medi aproximadamente 55,12, contra a previsão de 20.
A execução das operações NumPy em código compilado evita a iteração Python por elemento, ajudando a explicar essa aceleração.
Em `uint16`, `4095*20 = 81900` excede os 16 bits e resulta em `81900 % 65536 = 16364`.
Escolheria `uint16` para contagens de 0 a 4095 e `float64` para representar pressões fracionárias, mantendo a precisão usada pela `SerieTemporal`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `numpy.float64` | `SerieTemporal` |
| `s[0]` | `numpy.float64` | `float64` |

Um resultado interessante é `s.sum()`: eu previa `numpy.float64`, mas observei `SerieTemporal`.
Nesse caso, a redução herdada do NumPy conserva a subclasse, produzindo um array de dimensão zero.
Já `s[0]` devolve um escalar `numpy.float64`, exibido pelo script como `float64`.

### R7 — Issue #4

Com 600 leituras e janela 30, `media_movel` retornava 570 valores em vez de 571.
`test_media_movel_inclui_primeira_janela` detectou a ausência da primeira janela.
Faltava o zero inicial na soma acumulada, fazendo as diferenças começarem na segunda janela.
A correção insere esse zero antes de `np.cumsum` e mantém `SerieTemporal`, sem modificar `self`.
A aceitação conferia tipo, limites inválidos e imutabilidade, mas não tamanho e valores das médias.
A janela igual ao tamanho também não era coberta; `test_media_movel_janela_igual_ao_tamanho` verifica o resultado `[11.0]`.

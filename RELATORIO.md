# Relatório — Mickael Eleakim dos Santos Oliveira Almeida (3492)

Relatório do projeto, preenchido na branch do aluno. Cada marco acrescenta a sua seção.

## Marco 1

### Ambiente

`which python`: `/home/al.mickael.eleakim/venvs/prog2-venv/bin/python`

Etapa 0 de `python marco1.py`: `Python 3.14.4 | NumPy 2.3.5 | fornecido 4.0`.

### R1 — Expressões regulares

A string `PT1010` é aceita por `re.match(r"[A-Z]{1,2}\d{1,3}", ...)`, pois `match` só precisa encontrar um prefixo compatível (`PT101`). `re.fullmatch` rejeita a string porque sobra um quarto dígito. Se `valida_tag` usasse `match`, aceitaria incorretamente essa tag inválida.

### R2 — Linhas inválidas

`ler_log` devolve as linhas descartadas, exatamente como apareceram, para que os erros possam ser investigados e contabilizados; linhas vazias são ignoradas. Por exemplo, se uma falha de comunicação truncar mensagens do transmissor PT102, descartá-las silenciosamente esconderia uma falha da RTU e dificultaria perceber que faltam leituras.

### R3 — Late binding

As lambdas de `errados` fecham sobre a variável `k`, que é consultada quando a função é chamada, e não quando é criada. Ao fim do laço, `k` vale `0,1`, o fator de `FT201`; por isso `errados["PT102"](4095)` resulta em `409,5`. Em `criar_conversores`, o argumento padrão `fator=escalas[tag]` guarda o fator correspondente a cada tag no momento da criação da lambda.

### R4 — Escala nominal

A conversão nominal `c * 600 / 4095` pressupõe uma relação linear entre contagens e pressão, mas o simulador modela o transmissor de forma não linear. Em `fornecido/simulador.py`, `p_real(c)` usa `600 * sin(0.5 * pi * c / 4095)` e `c_real(p)` usa a inversa com `arcsin`; assim, contagens próximas de 1790 correspondem a 380 kPa verdadeiros, mas a escala linear indica cerca de 262 kPa.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `9ed72f0`.

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18× (cerca de 36 MB contra 2 MB) | 18,0× (36.000.056 B / 2.000.000 B) |
| Tempo do laço / tempo vetorizado | ≈ 30 a 40× (laço perto de 0,1 s; vetorizado perto de 3 ms) | 63,1× (37,8 ms / 0,6 ms) |
| Tempo da compreensão / tempo do laço | ≈ 0,8× (compreensão um pouco mais rápida) | ≈ 0,89× (33,6 ms / 37,8 ms) |

A maior diferença foi a aceleração do método vetorizado: 63,1× em vez dos 30–40× previstos. Nesta execução, tanto o laço (37,8 ms, abaixo de 0,1 s) quanto a operação vetorizada (0,6 ms, abaixo de 3 ms) demoraram menos que o estimado; os tempos também variam com a máquina, as versões das bibliotecas e a carga do sistema. `uint16` representa valores de 0 a 65.535: como `4095 * 20 = 81.900`, o resultado sofre redução módulo `2^16` e vira 16.364; inteiros Python não têm esse overflow fixo. Escolheria `uint16` para contagens de 0 a 4095, por ocupar 2 bytes, e `float64` para pressões em kPa, para preservar precisão nas conversões e estatísticas.

### R6 — Tipos da `SerieTemporal` (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `SerieTemporal` (0-d, a subclasse costuma ser mantida) | `SerieTemporal` |
| `s[0]` | `np.float64` | `float64` |

O resultado mais surpreendente é `s.sum()`: embora a soma reduza a série a um único valor, o NumPy mantém a subclasse e devolve um objeto `SerieTemporal` de dimensão zero. Já `s[0]` é um escalar NumPy (`float64`), não uma série.

### R7 — Issue #4

Com 600 leituras e janela 30, `media_movel` devolvia 570 valores, mas o contrato exige `600 - 30 + 1 = 571`. O teste de regressão `test_tamanho_com_600_leituras_e_janela_30` verifica esse tamanho; também cobri o caso-limite em `test_janela_igual_ao_tamanho_da_serie`. A versão defeituosa subtraía `acumulada[:-janela]` de `acumulada[janela:]`, deixando de calcular a primeira janela; corrigi os índices para começar em `acumulada[janela-1:]` e acrescentei zero ao início do vetor de somas acumuladas deslocado. Os testes de aceitação só verificavam o tipo de retorno e as janelas inválidas, não o comprimento nem os valores calculados; `test_primeiro_valor_e_a_media_dos_primeiros_pontos` também verifica as médias esperadas, e `test_janela_1_devolve_a_propria_serie` cobre a janela 1.

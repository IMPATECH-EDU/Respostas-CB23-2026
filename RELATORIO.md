# Relatório — Brenno Oliveira (3502)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
$ which python
~/venvs/prog2-venv/bin/python
$ python marco1.py
=== Etapa 0: ambiente ===
Python 3.10.12 | NumPy 2.2.6 | fornecido 4.0
```

### R1 — Expressões regulares

O `re.match` só verifica o começo da string, e o `re.fullmatch` exige que ela inteira case com o padrão. Por isso `"PT1010"` passa no `match` (o começo `PT101` casa) e falha no `fullmatch`, assim como `"PT101 "`. Se `valida_tag` usasse `match`, aceitaria tags com caracteres sobrando, como `"PT1010"` ou `"B1xyz"`.

### R2 — Linhas inválidas

Devolver as linhas descartadas permite ver quanto se perdeu: neste log são 4 de 2408 linhas, e o `marco1.py` mostra quais são. Se fossem descartadas em silêncio, uma falha de comunicação com a RTU do PT102 que corrompesse parte das linhas deixaria a série de pressão com buracos, e ninguém perceberia. Com a contagem, é possível disparar um alerta quando ela passar do normal.

### R3 — Late binding

A lambda `lambda c: c * k` procura `k` no escopo onde foi criada, só quando é chamada. Na compreensão existe um único `k`, que no fim do laço vale 0,1 (fator do `FT201`, o último do dicionário). Por isso `errados["PT102"](4095)` calcula 4095 · 0,1 = 409,5. Em `criar_conversores`, cada lambda é criada dentro de uma chamada de `_conversor(fator)`, que tem o seu próprio `fator`, e cada tag mantém a sua escala (4095 contagens dão 600,0 kPa).

### R4 — Escala nominal

A média de 1788 contagens normais dá 262,0 kPa pela escala nominal, que supõe uma reta de 0 a 600 kPa, e a conferência é 380,0 kPa. A hipótese é que a resposta do transmissor é uma curva côncava. Isso aparece em `fornecido/simulador.py`: `p_real(c) = 600·sin(π/2 · c/4095)` dá 380,0 kPa para 1788 contagens, e `tabela_calibracao()` amostra essa curva em 9 pontos.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `2c1e0d6`

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18x (lista perto de 36 MB, `uint16` com 2 MB) | 18,0 vezes (35 999 176 B contra 2 000 000 B) |
| Tempo do laço / tempo vetorizado | 40x | 30,3 vezes (91,5 ms contra 3,02 ms) |
| Tempo da compreensão / tempo do laço | 0,7 | 0,77 (70,4 ms contra 91,5 ms) |

Tempos de uma execução com `k = 10`. A maior diferença foi no vetorizado: previ 40 vezes e medi 30. A conta vetorizada não é uma passada só: `converter_vetorizado` converte para `float64`, multiplica e divide, e cada passo percorre o milhão de elementos e aloca um array novo de 8 MB. A compreensão ficou perto do previsto (23% mais rápida que o laço, contra 30%), porque só evita a busca e a chamada de `append`. O `uint16 * 20` dá 16364 porque o NumPy faz a conta em 16 bits sem avisar: 81 900 = 65 536 + 16 364, o resto da divisão por 2^16. Para guardar as contagens, `uint16` (cabem em 12 bits), convertido para `float64` antes de qualquer conta. Para kPa, `float64`, porque médias e desvios de muitas leituras acumulam erro em `float32`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | `SerieTemporal` |
| `s[1:]` | SerieTemporal | `SerieTemporal` |
| `s * 2` | SerieTemporal | `SerieTemporal` |
| `s.sum()` | SerieTemporal (0-d) | `SerieTemporal` (dimensão 0) |
| `s[0]` | numpy.float64 | `float64` |

O resultado que mais chama atenção é `s.sum()` devolver uma `SerieTemporal` de dimensão 0 (`SerieTemporal(6.)` num teste pequeno), enquanto `s[0]` devolve um `float64`. As reduções (`sum`, `mean`, `max`, `std`) passam pelas ufuncs do NumPy, que mantêm a subclasse no resultado, e a indexação por inteiro extrai o elemento como escalar. Para obter um número, usa-se `float(...)` ou `int(...)`, como no total de pulsos do `marco1.py`.

### R7 — Issue #4

Sintoma: `media_movel(30)` em 600 pontos devolvia 570 valores em vez de 571. Testes de regressão: os quatro de `TestRegressaoMediaMovel`, como `test_tamanho_da_serie_do_relato`, todos falhando antes da correção. Causa: com S a soma acumulada, `S[janela:] - S[:-janela]` vale S[i+janela] - S[i], a soma dos pontos i+1 a i+janela, então a janela que começa no ponto 0 (soma S[janela-1]) nunca aparece. Correção: copiar `S[janela-1:]` e subtrair `S[:-janela]` a partir do segundo elemento. A aceitação só verifica o tipo e os `ValueError` de janela 0 e 6, sem olhar tamanho nem valores. Também não cobre `janela == len(s)`, que dava série vazia; `test_janela_igual_ao_tamanho` cobre.

## Marco 2

### Ambiente

```
$ python marco2.py
=== Etapa 0: ambiente ===
Python 3.10.12 | NumPy 2.2.6 | SciPy 1.15.3 | fornecido 4.0 | matrícula 3502
```

### R8 — Derivada numérica

O erro de truncamento da diferença adiante vale cerca de h·f''/2. Com o erro de 1,66e-5 em h = 1, f'' ≈ 3,3e-5, e o erro cai dez vezes a cada passo menor, até 1,7e-9 em h = 1e-4. O erro de arredondamento cresce como ε·|f|/h, com f(1000) ≈ 224,6: sobe de 6,2e-10 em h = 1e-5 para 1,4e-2 em h = 1e-12. O mínimo da tabela fica em h = 1e-5, onde os dois se equilibram. Em h = 1e-14, `1000 + 1e-14 == 1000`, pois o espaçamento dos doubles perto de 1000 é 1,1e-13. Então f(x+h) - f(x) = 0, a diferença dá 0 e o erro é a própria derivada, 0,2134.

### R9 — Issue #7

Testes de regressão: `TestRegressaoKahan.test_um_milhao_de_parcelas_de_um_decimo`, `test_kahan_bem_melhor_que_o_ingenuo`, `test_parcelas_menores_que_meio_ulp_nao_se_perdem` e `test_bate_com_fsum`; os quatro falhavam antes da correção. Em `t - (self._soma + y)`, o parêntese recalcula `soma + y` com o mesmo arredondamento que gerou `t`, então a conta dá `t - t = 0` sempre. A forma `(t - soma) - y` recupera o erro do arredondamento, pois `t - soma` é exato quando |soma| ≥ |y|, caso típico de um totalizador. A aceitação soma só 10 parcelas de 0,1 e confere com `math.isclose(..., 1.0)`, que a soma ingênua também satisfaz.

### R10 — Precisão × exatidão

O desvio é 0,514 kPa na curva linear e 0,516 kPa na spline. A precisão (dispersão das leituras) é a mesma, porque o ruído vem do transmissor. O viés em relação a 380 kPa é -1,852 kPa na linear e -0,022 kPa na spline, e essa é a diferença de exatidão: perto de 1790 contagens a linear converte com erro sistemático. A média de 595 leituras válidas reduz o erro padrão para 0,021 kPa, mas todas passam pela mesma curva e carregam o mesmo erro. Assim a média herda o viés de 1,9 kPa, cerca de 88 vezes o erro padrão.

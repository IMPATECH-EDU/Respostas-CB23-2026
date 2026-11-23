# Relatório — Samuel Faleiro (3512)

Resultados dos quatro marcos do Projeto Elevatória para a matrícula 3512.

## Marco 1

### Ambiente

No PowerShell, o executável usado (equivalente a `which python`) foi:
```text
C:\Users\Samuel\venvs\prog2-venv\Scripts\python.exe
=== Etapa 0: ambiente ===
Python 3.15.2 | NumPy 2.5.5 | fornecido 4.0
```

### R1 — Expressões regulares

A string `PT1010` tem o prefixo válido `PT101`. Com o padrão da tag,
`re.match` aceita esse prefixo e deixa o último dígito de fora. `re.fullmatch` exige a
string inteira, então `valida_tag` rejeita a tag de quatro dígitos.

### R2 — Linhas inválidas

As linhas descartadas permitem contar e investigar falhas de comunicação. O log desta
matrícula teve 2.404 registros válidos e 4 inválidos. Se um cabo começar a falhar e
truncar mensagens de alarme, ignorá-las em silêncio pode dar a impressão de que o
equipamento continua operando normalmente.

### R3 — Late binding

As lambdas em `errados` consultam `k` na hora da chamada. Nesse momento, `k` tem
o último fator, 0,1, de FT201, e o resultado é 409,5. O argumento padrão
`fator=fator` em `criar_conversores` guarda o fator ao criar cada função.
Assim, o conversor de PT102 devolve 600,0 kPa para 4095 contagens.

### R4 — Escala nominal

A escala nominal supõe uma resposta linear e dá 261,944 kPa, contra 380,000 kPa
de referência. Em `fornecido/simulador.py`, `p_real` usa um seno para converter
contagens em pressão e `c_real` usa o arco seno para gerar as contagens do log.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit `e6c413e`.

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18,000028 |
| Tempo do laço / tempo vetorizado | 30 | 14,298612 |
| Tempo da compreensão / tempo do laço | 0.8 | 0,893844 |

A maior diferença foi laço/vetorizado. A conversão vetorizada levou 11,914 ms,
incluindo conversão para float e criação de arrays de resultados, frente a 170,351 ms
do laço. A compreensão levou 152,267 ms e o map, 218,314 ms.
Em `uint16`, 81.900 excede 65.535 e fica 81.900 − 65.536 = 16.364.
Usaria `uint16` para contagens de 12 bits e `float64` para pressões fracionárias em kPa.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | numpy.float64 | SerieTemporal (0D) |
| `s[0]` | numpy.float64 | numpy.float64 |
A surpresa foi `s.sum()`: a redução mantém a subclasse em um array de dimensão
zero. Já indexar uma posição com `s[0]` devolve um escalar `numpy.float64`.

### R7 — Issue #4

A média de janela 30 devolvia 570 pontos em vez de 571. Sem um zero inicial na
soma acumulada, a primeira diferença de prefixos começava no segundo ponto.
O zero inicial permite calcular também a primeira janela. A aceitação verificava tipo
e erros de entrada, sem conferir valores ou tamanho. `test_inclui_primeira_janela`
confere o alinhamento. `test_janela_do_tamanho_da_serie` exige a única média
quando a janela cobre toda a série.


## Marco 2

### Ambiente

```text
=== Etapa 0: ambiente ===
Python 3.15.2 | NumPy 2.5.5 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3512
```

### R8 — Derivada numérica

O erro caiu de 1,658 × 10⁻⁵ em `h = 1` até 6,224 × 10⁻¹⁰ em `h = 10⁻⁵`.
Nesse trecho, diminuir o passo reduz o erro de truncamento da diferença adiante.
Com passos menores, a subtração de valores próximos e a divisão por `h`
amplificam o erro de arredondamento. Em `h = 10⁻¹⁴`, `1000 + h` arredonda para
1000 e a aproximação dá zero. O erro é a própria derivada, 0,213432888873 kPa/contagem.

### R9 — Issue #7

`test_pulsos_repetidos` e `test_parcelas_menores_que_a_resolucao_da_soma` detectam
a perda da compensação. Como `t` já guarda o resultado arredondado de `s + y`,
repetir a soma em `t - (s + y)` sempre dá zero. `(t - s) - y` recupera o resíduo.
O teste de aceitação usa poucas parcelas e não exige precisão suficiente para a
diferença aparecer. Em um milhão de pulsos, a soma ingênua errou 1,333 × 10⁻⁶ L.
Kahan e o acumulador inteiro deram 100.000,0 L, com erro medido zero.

### R10 — Precisão × exatidão

Para PT102, os desvios amostrais foram 0,514 kPa (linear) e 0,515 kPa (spline),
indicando dispersões parecidas. Os vieses foram −1,871 kPa e −0,041 kPa,
respectivamente, então a spline ficou mais próxima da referência de 380 kPa.
A média de 595 leituras reduz o erro aleatório, mas o viés da calibração linear
se mantém. A altura obtida com a spline foi 35,75 ± 0,22 m, ante 35,749 m de referência.

## Marco 3

### R11 — Bissecção × Newton

A bissecção começa em [2, 15] e reduz a largura à metade até ficar abaixo de 10⁻¹².
São 44 iterações para os três Reynolds. Newton levou 5, 4 e 3 iterações.
Para Re = 10⁴, os erros 5,0 × 10⁻², 2,3 × 10⁻⁵ e 5,0 × 10⁻¹² dão ordem 2,00.
Nessa ordem, perto da raiz, o erro seguinte é proporcional ao quadrado do anterior.
Para f(x) = x³ − 1 em [−2, 2], Newton começa em zero com derivada nula, enquanto
a bissecção encontra a raiz porque há troca de sinal.

### R12 — Issue #9

Os testes são `test_passo_quadratico_com_derivada_analitica` e
`test_converge_com_poucas_iteracoes`. Ao fixar a derivada em d, o termo de primeira
ordem do erro é `(1 - f'(raiz)/d) * erro`, geralmente não nulo. Recalcular a
derivada a cada passo cancela esse termo perto da raiz simples. A aceitação
conferia a raiz, mas não os passos nem a rapidez. Com a spline, os dois métodos
concordaram em Q = 64,934 L/s e H = 35,774 m.

## Marco 4

### R13 — Integração e descontinuidade

Integrando tudo de uma vez, as ordens observadas foram 1,00 no trapézio e 0,65
no Simpson. Os saltos da tarifa às 18 h e às 21 h deixam um erro da ordem da
largura dos intervalos que cruzam essas mudanças. Por faixa, a tarifa é constante
e a potência é suave no ensaio de convergência, recuperando as ordens 2,00 e 4,00.
Com a vazão registrada e os ajustes de grau 2, o custo total deu R$ 417,49.
A ponta custou R$ 132,53 (31,7% do total) e a energia do dia foi 658,27 kWh.

### R14 — Issue #11

`test_constante_em_malha_irregular` e `test_rampa_em_malha_irregular` mostram
que reutilizar o primeiro passo distorce as áreas quando as larguras diferem.
A aceitação direta do trapézio usava espaçamento uniforme. A correção usa cada
diferença consecutiva de tempo. Simpson exige espaçamento uniforme, mas as 89
leituras têm intervalos de 15, 30 e 45 min. O trapézio corrigido deu 3.890,53 m³,
com erro de 0,06% em relação aos 3.888,00 m³ de referência.

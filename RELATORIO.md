# Relatório — Nicael Lima Coelho (3513)

## Marco 1

### Ambiente

```text
$ which python
/home/agent/venvs/prog2-venv/bin/python
$ python marco1.py
=== Etapa 0: ambiente ===
Python 3.12.14 | NumPy 2.3.5 | fornecido 4.0
```

### R1 — Expressões regulares

Em `PT1010`, `re.match` encontra o prefixo `PT101` e deixa o último zero de fora.
Se `valida_tag` usasse esse resultado, aceitaria um identificador com quatro dígitos.
Com `fullmatch`, toda a string precisa seguir a regra da tag.

### R2 — Linhas inválidas

Das 2.408 linhas, o leitor aproveitou 2.404 e devolveu as quatro descartadas com o texto original.
Se um transmissor começar a mandar linhas truncadas, a média das leituras que chegaram pode continuar parecendo normal.
Examinar os descartes permite distinguir uma falha de comunicação de um período sem eventos.

### R3 — Late binding

As lambdas de `errados` consultam a mesma variável `k` quando são chamadas. A última escala do dicionário é 0,1,
então `errados["PT102"](4095)` calcula 409,5. Em `lambda c, fator=escala: c * fator`, o valor padrão é avaliado
na criação de cada função. Assim, o conversor de PT102 guarda 600/4095 e devolve 600 kPa.

### R4 — Escala nominal

A escala nominal deu 262,000 kPa para uma referência de 380,000 kPa. A diferença sugere uma resposta não linear.
Em `fornecido/simulador.py`, `gerar_log` usa `c_real` para gerar as contagens. A função inversa,
`p_real(c) = 600 · sen(πc/8190)`, explica por que a reta que une os extremos subestima a pressão entre eles.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit `77cdd3b`.

| Grandeza | Previsão | Medido |
| --- | ---: | ---: |
| Memória da lista / memória do `uint16` | 18 × | 18,0000 × |
| Tempo do laço / tempo vetorizado | 25 × | 122,2749 × |
| Tempo da compreensão / tempo do laço | 0,85 × | 0,7993 × |

A maior diferença foi no tempo do laço (59,6807 ms) em relação ao NumPy (0,4881 ms). A estimativa subavaliou o custo de fazer
um milhão de operações com objetos Python. O NumPy percorre o vetor em código compilado. Em `uint16`, 4095 × 20 = 81900,
que deixa resto 16364 na divisão por 65536. Para guardar contagens de 12 bits basta `uint16`. Para calcular pressões, uso `float64`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

A soma era o caso menos intuitivo. O resultado contém um único número, mas a redução preserva a subclasse
em um array com forma `()`. Ao selecionar um elemento por índice, `s[0]` já devolve o escalar NumPy.

### R7 — Issue #4

Com 600 pontos e janela 30 saíam 570 médias. Faltava a soma vazia antes do primeiro elemento, então desaparecia a primeira janela.
`test_primeira_janela` e `test_janela_do_tamanho_da_serie` reproduziram o erro. Acrescentar o zero inicial recuperou as 571 médias.
A aceitação conferia o tipo, as janelas inválidas e a preservação da entrada, mas não contava as janelas válidas.
Outro caso ausente era uma data impossível com formato correto, coberto por `test_calendario_e_relogio`.

## Marco 2

### Ambiente

```text
$ python marco2.py
=== Etapa 0: ambiente ===
Python 3.12.14 | NumPy 2.3.5 | SciPy 1.17.0 | fornecido 4.0 | matrícula 3513
```

### R8 — Derivada numérica

A diferença adiante tem erro de truncamento de ordem h. O erro caiu de 1,658 × 10⁻⁵ em h = 1 para 6,224 × 10⁻¹⁰ em h = 10⁻⁵.
Com passos menores, a subtração de pressões quase iguais perde algarismos e a divisão por h amplia o arredondamento.
Em h = 10⁻¹⁴, `1000.0 + h == 1000.0`: a aproximação vira zero e o erro absoluto é o módulo da derivada, cerca de 0,213433 kPa/contagem.

### R9 — Issue #7

`test_dez_mil_decimos` e `test_duas_unidades_apos_total_grande` expuseram a perda de parcelas.
Como `t` já guarda a soma arredondada de `s + y`, recalcular essa expressão em `t - (s + y)` produz zero.
Em `(t - s) - y`, mede-se a diferença entre o incremento representado e o pretendido. A parcela seguinte usa essa correção.
A aceitação somava só dez décimos com `isclose`. Em um milhão, a soma ingênua errou 1,333 × 10⁻⁶ L e Kahan chegou a 100000,0 L.

### R10 — Precisão × exatidão

Em PT102, os desvios foram 0,535 kPa (linear) e 0,537 kPa (spline), portanto a dispersão das leituras e a precisão foram semelhantes.
Em relação aos 380 kPa, os vieses foram −1,803 kPa e +0,027 kPa, respectivamente. A spline foi mais exata neste ensaio.
A média das 595 leituras válidas reduz a contribuição do ruído aleatório, mas o erro sistemático da curva linear atua na mesma direção.

## Marco 3

### R11 — Bissecção × Newton

Em Colebrook, o intervalo inicial de x é [2, 15]. Para cada Reynolds, a largura após k cortes é 13/2ᵏ, abaixo de 10⁻¹² pela primeira vez em k = 44.
Para Re = 10⁴, os erros de Newton passaram por 5,0 × 10⁻², 2,3 × 10⁻⁵ e 5,0 × 10⁻¹². Perto de uma raiz simples,
erro seguinte proporcional ao quadrado do atual significa aproximadamente dobrar os algarismos corretos. A ordem estimada foi 2,00.
Em f(x) = x³ − 1 em [−2, 2], Newton com derivada exata para no ponto médio 0, onde a derivada é nula. A bissecção mantém a troca de sinal.

### R12 — Issue #9

`test_segunda_tangente` confere a segunda aproximação e `test_seis_passos_com_derivada_numerica` limita o número de passos.
Com a inclinação inicial fixa, o erro perto da raiz é multiplicado, em primeira ordem, por 1 − f′(r)/f′(x₀). Quando o módulo está entre 0 e 1, a convergência é linear.
Reavaliar a inclinação em cada aproximação cancela o termo linear para uma raiz simples com derivada exata. A aceitação verificava a raiz e a convergência, sem exigir sua ordem.

## Marco 4

### R13 — Integração e descontinuidade

A tarifa muda às 18 h e às 21 h. Um painel que atravessa um salto mistura dois preços e pode introduzir um erro proporcional à largura do painel.
Na integração direta, as ordens estimadas foram 1,00 (trapézio) e 0,65 (Simpson) nas malhas do script. A posição do salto no painel afeta a estimativa.
Separando as faixas, cada integral usa a potência suave e uma tarifa constante. As ordens medidas voltaram a 2,00 e 4,00.

### R14 — Issue #11

`test_constante_com_lacuna` e `test_reta_com_primeiro_passo_igual_ao_medio` detectaram o reuso da primeira largura em toda a soma.
A aceitação testava o trapézio com espaçamento uniforme. No registro de 89 leituras houve intervalos de 15, 30 e 45 minutos.
Com `np.diff(t)`, cada trapézio ganhou sua largura correta e o volume ficou em 3899,55 m³. O Simpson da base exige malha uniforme e número par de subintervalos.

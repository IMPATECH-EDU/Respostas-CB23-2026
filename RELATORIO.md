# Relatório — Paula Pires (3470)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

```
which python
/home/paulapires/venvs/prog2-venv/bin/python

python marco1.py   # Etapa 0
=== Etapa 0: ambiente ===
Python 3.14.4 | NumPy 2.5.3 | fornecido 1.0
```

### R1 — Expressões regulares

Com o padrão de tag `[A-Z]{1,2}[0-9]{1,3}`, a string `"PT101_invalida"` é aceita por `re.match` e rejeitada por `re.fullmatch` (devolve `None`). Se `valida_tag` usasse `match`, aceitaria também `"PT1010"` e `"PT101 "`. `fullmatch` a string inteira precisa ser a tag.

### R2 — Linhas inválidas

Devolver as linhas descartadas permite contá-las, conferir que registros + inválidas = linhas e ler cada uma. No log tem 4 inválidas: duas falhas de comunicação com a RTU e duas linhas truncadas. 

### R3 — Late binding

A lambda `lambda c: c * k` guarda a variável `k`, e não o valor que `k` tinha quando a lambda foi criada: `k` só é consultado na chamada. Ao fim da compreensão, `k` vale 0,1 (a escala de FT201, a última do dicionário), então todas as lambdas usam 0,1 e `errados["PT102"](4095) = 4095 × 0,1 = 409,5`. Em `criar_conversores` uso `lambda c, f=fator: c * f`: o argumento padrão é avaliado na criação de cada lambda, então cada função guarda o fator da sua tag (`certos["PT102"](4095) = 600,0`).

### R4 — Escala nominal

A escala nominal supõe o transmissor linear (`p = c × 600 / 4095`) e dá 262,0 kPa para a média das contagens normais de PT102 (≈ 1788), contra 380,0 kPa de conferência. Parece que resposta do transmissor não é linear, então a reta subestima a pressão no meio da faixa. A explicação está em `fornecido/simulador.py`: `p_real(c) = 600·sin(0,5·π·c/4095)`, com a inversa `c_real`, que dá 380 kPa para c ≈ 1788.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: ee4ea20 

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` |18x|18x |
| Tempo do laço / tempo vetorizado |50x |27,8 |
| Tempo da compreensão / tempo do laço |0,75x |0,92|

A maior diferença foi laço/vetorizado, onde previ ≈ 50× e medi 27,8×. Provavelmente o vetorizado ficou lento porque `converter_vetorizado` faz `astype(float64)`, `* 600` e `/ 4095`. A compreensão ganhou só 8 % do laço (0,92) e o `map` com lambda foi mais lento (0,8×). `uint16` guarda de 0 a 65535 e o NumPy não avisa quando o resultado passa disso: 4095 × 20 = 81900 vira 81900 − 65536 = 16364 (o `int` do Python não tem limite). Escolhi `uint16` para contagens (12 bits, 2 B) e `float32` para kPa (4 B, basta para 0 a 600 kPa), calculando em `float64`.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` |SerieTemporal |SerieTemporal |
| `s[1:]` |SerieTemporal |SerieTemporal |
| `s * 2` |SerieTemporal |SerieTemporal |
| `s.sum()` |numpy.float64 |SerieTemporal |
| `s[0]` |numpy.float64 |float64 |

Eu esperava que `s.sum()` desse um `numpy.float64`, como acontece com um `ndarray` comum, mas deu uma `SerieTemporal`. Provavelmente isso acontece porque, numa subclasse de `ndarray`, as operações e reduções devolvem o resultado no tipo da subclasse, mesmo quando ele tem um único valor. Já `s[0]`, que indexa com um inteiro, devolve um escalar do NumPy. 

### R7 — Issue #4

Sintoma: com 600 pontos e janela 30, `media_movel` devolvia 570 valores, e o certo é (n − k + 1) = 571; os valores também vinham deslocados um ponto porque a janela `s[0:30]` nunca aparecia. 
Teste de regressão: `test_media_movel_tamanho_correto`. 
Causa: `cumsum` dá `acumulada[i] = x[0] + … + x[i]`, então `acumulada[k:] - acumulada[:-k]` soma `x[i+1] … x[i+k]`. Faltava o 0 inicial.
Correção: colocar `0.0` na frente com `np.concatenate`, de modo que a janela i seja `acumulada[i+k] - acumulada[i]`. Os testes de aceitação só conferem o tipo do resultado e os `ValueError` das janelas 0 e 6. O caso dos valores é coberto por `test_media_movel_valores_corretos`.

## Marco 2

### Ambiente
```
=== Etapa 0: ambiente ===
Python 3.14.4 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3470
```

### R8 — Derivada numérica
O erro diminui até 1e-5 pois o erro de truncamento predomina, logo, quando h diminui 10 vezes, o erro também diminui 10x
Quando h fica muito pequeno, f(x+h) e f(x) se tornam praticamente iguais e o que sobra é o erro de arredondamento que é ampliado ao dividir por h, e então o erro passa a crescer. 
Com um h = 1e-14, somado  a 1000, f(x+h) = f(x), dessa maneira, o numerador da derivada é 0 e resta, no erro, o módulo de 0 - a derivada, que é a própria derivada.

números da execução: 1.658e-05 em h =1 e 6.224e-10 em h = 1e-5
2.134e-1 em h=1e-14

### R9 — Issue #7

Nomes dos testes: test_parcelas_pequenas e test_parcelas_muito_pequenas.
t é numericamente idêntico a s+y, então é feito s+y - (s+y), que dá 0. Quando é feito (t-s) -y, não é feita a subtração de dois idênticos. t-s equivale a quanto de y entrou na conta, e, ao subtrair y desse resultado, vê-se o que é perdido no arredondamento
Os testes de aceitação não pegam o defeito pois usam math.isclose, o que apenas olha se é perto o suficiente, e não se é exatamente igual. O teste corrigido usa assertEqual, que olha se é exatamente igual e, por isso, pega o defeito.

### R10 — Precisão × exatidão

Precisão é o quão parecidas as leituras estão (próximas, com desvio padrão baixo). Nesse caso, as curvas possuem praticamente o mesmo desvio, então as suas precisões são praticamente iguais. Exatidão é o quanto o resultado está próixmo do valor correto. Nesse caso, a spline errou apenas 0.008 kpa, enquanto a linear errou em -1.821 kpa. 

O viés da linear é erro sistemático, que vem da interpolação da própria curva. Nessa faixa de contagem, ela erra para o mesmo lado. O comum é que a média cancele erros aleatórios (pois erram para cima e para baixo). Logo, todas as leituras carregam o erro da curva, o que faz com que o seu viés não seja eliminado.

## Marco 3

### R11 — Bissecção × Newton

A bissecção não usa o valor de f, apenas o seu sinal. Cada iteração faz com que o tamanho do intervalo caia pela metade, independente do valor.  O intervalo é sempre [2,15] (com largura 13) e a tolerância é 1e-12. Logo, precisam-se de log2(13/1e-12) = 44 iterações.

Veja Re = 1e4: 5.0e-02 -> 2.3e-05 -> 5.0e-12. A ordem estimada é 2.00. 
Ordem de convergência 2 significa que o erro de cada passo é mais ou menos o quadrado do anterior (com uma constante) 

Na derivada = 0 acontece ValueError, pois Newton divide por f'(x). Se a derivada for quase 0, o próximo x vai muito longe. 
Isso não acontece com a bissecção.

### R12 — Issue #9

test_raiz_de2_poucas_iteracoes e test_colebrook_re

Newton usa a tangente no ponto atual para chegar na raiz que, perto dela, é quase igual à inclinação da função e, por isso, o erro vira o quadrado do anterior. Com a derivada fixa, a tangente é a inclinação longe da raiz e, por isso, cada passo diminui o erro com uma proporção física, que é a convergência linear.

Os testes de aceitação não pegam o defeito pois só medem se converge e a raiz está certa. Isso acontece mesmo com a derivada fixa, mas demora mais.

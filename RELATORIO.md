# Relatório — Aylan da Silva Reis (3468)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Trabalhei no Windows, com PowerShell e venv (`$HOME\venvs\prog2-venv`). No lugar de `which python`, usei
`(Get-Command python).Source`, visto que esse comando não existe no Windows:

    C:\Users\Aylan\venvs\prog2-venv\Scripts\python.exe

Etapa 0 do `python marco1.py`:

    === Etapa 0: ambiente ===
    Python 3.13.13 | NumPy 2.5.4 | fornecido 4.0

### R1 — Expressões regulares

Com o padrão de tag `[A-Z]{1,2}\d{1,3}`, a string `"PT1010"` é aceita por `re.match`, que só exige que o começo, 
mas é rejeitada por `re.fullmatch`, que exige que a string inteira. 
Se `valida_tag` usasse `match`, aceitaria tags inválidas com sobra no fim, 
como `"PT1010"` que seria `"PT101 "`, e assim o teste de aceitação de tags inválidas falharia.

### R2 — Linhas inválidas

Devolver as linhas descartadas permite contabilizar e observar cada uma delas, em vez de perder a informação. No log, 2 das
4 linhas inválidas eram `### falha de comunicacao com a RTU ###`. Se a comunicação com a RTU começasse a falhar
muitas vezes, descartar os dados deixaria oculto possiveis problemas: o software continuaria mostrando dados como se tudo
estivesse normal, mesmo com danos serios no resultado. Uma linha truncada (como `2026-10-05 08:20:4`) também poderia ser um alarme
perdido, e somente a contagem de inválidas mostraria que algo foi descartado.

### R3 — Late binding

Na compreensão `{tag: (lambda c: c * k) ...}`, a lambda não guarda o valor de `k`, 
ela anota o valor e procura ela quando for chamada. Como esse último valor fica guardado por um ponteiro, 
então `errados["PT102"](4095)` dá 4095 × 0,1 = 409,5. Na minha `criar_conversores`, 
uso `lambda c, f=fator: c * f`: o argumento padrão é avaliado quando cada lambda é criada, 
então cada uma guarda o fator da própria tag (PT102 dá 600,0).

### R4 — Escala nominal

Na escala nominal, estamos supondo que o transmissor de pressão é linear (por uma reta, c × 600 / 4095). Mas sabemos que isso não é verdade, 
A explicação está em `fornecido/simulador.py`, na função `p_real`: a pressão real é 600 · sen(π/2 · c/4095). 
As duas curvas coincidem em 0 e em 4095, mas no meio a reta fica abaixo do seno. 
Para a média de 1791 contagens, a reta dá ≈ 262 kPa e o seno dá ≈ 380 kPa, igual ao valor de conferência. 
O log é gerado com `c_real` que é a inversa de `p_real' (arcsin),
e a `tabela_calibracao` indica que a correção virá por calibração, 
então poderemos usar pontos conhecidos para construir uma conversão e novos pontos sem depender da reta.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d836e4a

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 18 | 18,0 |
| Tempo do laço / tempo vetorizado | ≈ 100 | 27,3 |
| Tempo da compreensão / tempo do laço | ≈ 0,8 | 0,79 |

A maior diferença foi no vetorizado: previ ~100x e medi 27,3x (em outra execução, 20,9x). 
A conversão `c * 600 / 4095` cria arrays temporários de 1 milhão de floats (8 MB cada), 
e esse custo de memória pesa no tempo. O `uint16` guarda de 0 a 65535; 
4095 × 20 = 81900 não cabe e produz 81900 − 65536 = 16364 voltas, sem avisar. 
Para contagens (0 a 4095) usaria `uint16` (2 bytes, 18x menos memória que a lista), 
convertendo para float antes das contas (`float64`, pois kPa têm casas decimais, então precisam de um tipo de ponto flutuante).

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O único que surpreendeu foi `s.sum()` devolver `SerieTemporal`, e não um número. A soma é uma redução do NumPy,
e o resultado passa pelo mecanismo que preserva a subclasse: vira uma `SerieTemporal` de zero dimensões. Enquanto isso `s[0]`
acessa um único elemento diretamente e devolve um escalar `float64`. Sabendo disso, no `marco1.py`, usei `float(...)`
para imprimir médias e mínimos.

### R7 — Issue #4

Sintoma: a média móvel de 30 pontos sobre 600 leituras devolvia 570 valores, e não 571 (n − janela + 1). 
Testes de regressão: `test_tamanho`, `test_primeiro_valor` e `test_janela_max`. 
Causa: com a soma acumulada S, a soma da janela que começa em i é S[i+j−1] − S[i−1]; para i = 0 é preciso S[−1] = 0, 
que não existia, então `acumulada[j:] - acumulada[:-j]` começava na segunda janela e perdia a primeira. 
Correção: colocar um 0 no início da soma acumulada (`np.concatenate`) e usar `.view(type(self))` para manter o tipo. 
Os testes de aceitação só verificavam o tipo e os erros, não o tamanho nem os valores. 
Eles também não cobrem a janela igual ao tamanho da série (o código antigo devolvia vazio), caso coberto pelo meu `test_janela_max`.
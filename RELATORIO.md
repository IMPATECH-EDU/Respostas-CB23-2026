# Relatório — João Filipe Mota Ferreira (3475)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
/home/al.joao.filipe/venvs/prog2-venv/bin/python
Python 3.13.15 | NumPy 2.5.4 | fornecido 1.0

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->
`"PT101aa"`
Se utilizássesmos `re.match`, haveria falsos positivos, uma vez que ele não verifica a string em sua totalidade e strings com excessos seriam considerados, mesmo quando não deviam

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
Suponha que um sensor apresente problemas e tenha sua saída corrompida somente em contextos específicos, mas funcione adequadamente em outras situações; por exemplo, ele funcione corretamente enquanto a água estiver em um nível estável, mas apresente erros quando a bomba de água ligar. Nesse caso, se as linhas corrompidas fossem descartadas, então seria mais difícil detectar esse tipo de problema, uma vez que o fato dele não parar de funcionar definitivamente poder sugerir que ele está funcionando adequadamente.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
No `errados`, as funções lambda guardam apenas a referência à variável `k` do loop. Quando a função é executada, o loop já terminou e `k` retém o seu último valor (0.1, referente ao `"FT201"`), resultando no cálculo `4095 * 0,1 = 409,5`. A criar_conversores, por sua vez, força o early binding através da passagem de um argumento padrão, recuperando o valor de conversão no momento da criação de cada lambda.

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->
O código no `simulador.py` trabalha utilizando conversões trigonométricas `p_real` e `c_real`. Enquanto isso, a conversão que utilizei supõe um simples fator linear de conversão, explicando a discrepância.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: d8bc5f0 <!-- cole o hash curto do commit de previsões -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | $36000056 / 2000000 \approx 18$ | $18,0$ |
| Tempo do laço / tempo vetorizado | $50$ | $29,0$ |
| Tempo da compreensão / tempo do laço | $1$ | $1,1$ |

<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->
`uint16 * 20` ou, mais especificamente, `uint16(4095) * 20` dá 16364 devido ao overflow: o resultado correto é 81900, mas como o `uint16` só vai até $2^{16}-1=65535$, o resultado final obtido é $81900-2^16=16364$. Para contagens, que não passam de 4096, `uint16` é o mínimo suficiente, garantindo eficiência no uso de memória. Para kPa, `float64` garante a máxima precisão.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `ndarray` |`SerieTemporal` |
| `s[1:]` | `ndarray` |`SerieTemporal` |
| `s * 2` | `ndarray` | `SerieTemporal` |
| `s.sum()` | `ndarray` | `SerieTemporal` |
| `s[0]` | `float64` | `float64` |

<!-- Explique o resultado que mais surpreendeu você. -->
Surpreende-me o fato de que a maioria das operações sobre objetos do tipo `SerieTemporal` não tenham retorando um `ndarray`, mesmo sem que os métodos  da superclasse tenham sido sobrescrevidos. Isso parece ser um comportamento específico do numpy: em testes próprios, criar uma subclasse de `list` e somar duas instâncias ainda retorna uma `list` do Python, e não uma instância da classe filha.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
O sintoma observado foi que havia menos valores no resultado da média móvel do que o esperado, como verificado pelo `test_media_movel_tamanho_e_valores`. O motivo é que o código original ignorava o primeiro valor da média móvel: a soma acumulada só considerava a partir do indice `janela`, que é o (janela+1)-ésimo item. Os testes de aceitação não pegaram o defeito porque a única coisa que faziam era verificar se o valor retornado era SerieTemporal e testar valores inválidos para `janela`. Além disso, o novo teste também verifica se o resultado produzido condiz com o esperado.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->
Python 3.13.15 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3475

### R8 — Derivada numérica

- De $h = 1$ até $10^{-5}$: Domina o erro de truncamento $O(h)$, reduzindo o erro até o mínimo ($6{,}224 \times 10^{-10}$).
- Abaixo de $h = 10^{-5}$: Domina o erro de arredondamento $O(\epsilon/h)$ devido ao cancelamento catastrófico em $f(c+h) - f(c)$.
- Em $h = 10^{-14}$: Como $10^{-14} < \text{ulp}(1000)/2$, ocorre absorção (`1000 + 1e-14 == 1000`), zerando o numerador e a derivada estimada; o erro iguala a própria derivada exata ($0{,}2134\text{ kPa/contagem}$).

### R9 — Issue #7

- Testes: `test_absorcao`, `test_absorcao_2`, `test_medir` e `test_value_errors`.
- Causa: A soma em ponto flutuante não é associativa; como `t = s + y`, `t - (s + y)` repete o mesmo arredondamento e dá sempre `0.0`, anulando a compensação, enquanto `(t - s) - y` recupera o resíduo descartado.
- Por que passou nos testes: Os testes originais acumulavam valores de grandeza próxima ao montante (fora do regime de absorção), sem gerar erro de representação relevante.

### R10 — Precisão × exatidão

- Precisão × exatidão: Ambas têm a mesma precisão (desvio padrão $\approx 0{,}51\text{ kPa}$, ruído aleatório), mas difere a exatidão: a `spline` é exata (viés $-0{,}032\text{ kPa}$) e a `linear` é precisa, porém inexata (viés $-1{,}862\text{ kPa}$).
- Por que a média não elimina o viés: A média de ~600 leituras atenua apenas o erro aleatório ($1/\sqrt{N}$); o viés é um erro sistemático da aproximação linear sobre um transdutor não linear, deslocando todas as amostras no mesmo sentido.

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->
- 44 iterações fixas: O custo da bissecção depende apenas do tamanho do intervalo inicial e da tolerância ($k = \lceil \log_2((b - a)/\text{tol}) \rceil$), independendo da função ou de $Re$.
- Ordem 2: Indica convergência quadrática ($e_{k+1} \approx C e_k^2$), dobrando os dígitos corretos a cada passo (em $Re=10^4$, o erro salta de $5{,}0\text{e-}2 \to 2{,}3\text{e-}5 \to 5{,}0\text{e-}12 \to 8{,}9\text{e-}16$).
- Falha do Newton: Em regiões quase planas ($f'(x_k) \approx 0$) ou pontos de inflexão, Newton oscila ou projeta chutes para fora do domínio ($f \le 0$), enquanto a bissecção sempre converge havendo troca de sinal.

### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->
- Testes: `test_newton_convergencia_quadratica` e `test_newton_poucas_iteracoes`.
- Convergência linear: Fixar $f'(x_0)$ reduz o algoritmo ao método das cordas; como $f'(x_0) \neq f'(r)$, o termo de 1ª ordem de Taylor não se anula, fazendo o erro decair linearmente ($e_{k+1} \propto e_k$).
- Por que não foi detectado: Os testes de aceitação verificavam apenas o valor final da raiz, sem checar `iteracoes` ou `ordem_convergencia`, e o método ainda convergia dentro de `max_iter`.
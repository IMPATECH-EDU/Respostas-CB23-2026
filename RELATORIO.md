# Relatório — Thiago Benjamim Lopes de Azevedo (3521)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

C:\Users\thiag\Downloads\my_repos\Respostas-CB23-2026\.venv\Scripts\python.exe
=== Etapa 0: ambiente ===                                                                 
Python 3.14.7 | NumPy 2.5.3 | fornecido 1.0

### R1 — Expressões regulares

Uma string como "PT101 " (com espaço no fim) é aceita no início pelo re.match, mas rejeitada pelo re.fullmatch. Se o match fosse usado, a função valida_tag consideraria válidas tags com erros, permitindo a entrada de dados formatados incorretamente no sistema.

### R2 — Linhas inválidas

Devolver as linhas inválidas permite a verificação e o diagnóstico técnico do sistema. Numa operação real, descartá-las em silêncio esconderia problemas de comunicação da RTU ou falhas num sensor (como os carateres truncados), levando os engenheiros a acreditarem falsamente que a estação opera em perfeitas condições.

### R3 — Late binding

No ciclo da versão errada, as variáveis tag e k sofrem late binding, fazendo com que todas as lambdas apontem para o último valor do dicionário no final da iteração (0.1, de FT201), resultando num cálculo de 4095*0.1=409.5. A nova função criar_conversores resolve isto inserindo a variável no escopo local imediato de uma lambda factory.

### R4 — Escala nominal

A escala nominal assume uma resposta linear perfeita (Regra de Três Simples). Contudo, consultando o simulador (em fornecido/simulador.py), a função p_real(c) mostra que o conversor possui uma resposta senoidal (np.sin), o que justifica o grande desvio face aos 380 kPa reais.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: 47a312f

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18 |
| Tempo do laço / tempo vetorizado | 50 | 21.8 |
| Tempo da compreensão / tempo do laço | 0.75 | 0.76 |

O uint16 apenas suporta valores até 65535. Ao multiplicar 4095 por 20 (81900), ocorre overflow, resultando em 81900-65536=16364. Eu utilizaria uint16 para contagens puras do sensor e float32 ou float64 para valores contínuos como a pressão em kPa.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | numpy.float64 | SerieTemporal |
| `s[0]` | numpy.float64 | float64 |

O resultado mais impressionante é o único fora da previsão, sendo o 's.sum()', que retorna um SerieTemporal ao invés de um numpy.64 devido à classe SerieTemporal que foi criada com uma regra estrita no método de_lista para rejeitar qualquer coisa que não seja unidimensional (1D). No entanto, como o .sum() é um método nativo otimizado do NumPy, ele salta a validação e cria uma SerieTemporal 0-D, "quebrando" a regra original da classe.

### R7 — Issue #4

A média móvel devolvia 570 em vez de 571 valores. Criei o teste test_tamanho_correto_media_movel para achar o problema. A causa estava no corte cego de matrizes resultantes da soma acumulada, o que omitia a primeira janela. Inseri um valor inicial 0.0 no np.cumsum para corrigir. Os testes base falhavam em detetar isto porque não afirmavam o tamanho final da lista, falha idêntica à que cobri para o descarte de sobras em reamostrar.

## Marco 2

### Ambiente

=== Etapa 0: ambiente ===
Python 3.14.7 | NumPy 2.5.3 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3521

### R8 — Derivada numérica

O erro de truncamento deriva da aproximação por série de Taylor e diminui com h -> 0. O erro de arredondamento surge da precisão finita da máquina, para h muito pequeno, a subtração de valores próximos causa cancelamento catastrófico. O erro total é minimizado no passo ótimo de aproximadamente 10^-5 a 10^-6, abaixo do qual o erro volta a crescer.

### R9 — Issue #7

Na soma direta de séries longas ou de grandezas discrepantes, o acumulador cresce S >> x_i, descartando os bits menos significativos das novas entradas e acumulando erro de ordem O(N). 

O algoritmo de Kahan corrige essa perda armazenando os bits descartados em uma variável de compensação c. Na implementação original com defeito, a atualização usava o agrupamento c = t - (s + y). Devido à associatividade, a expressão (s + y) era calculada primeiro, resultando no próprio valor aproximado t, o que fazia com que t - (s + y) se tornasse t - t = 0.0. Com o termo de correção zerado a cada ciclo, a compensação era anulada e a função comportava-se como uma soma comum.

A correção removeu o parêntese incorreto, passando para c = (t - s) - y. Ao avaliar primeiro (t - s), obtém-se a parcela do incremento que realmente alterou t, subtraindo y desse valor, recupera-se exatamente a perda de precisão por deslocamento de mantissa.

Para validar a correção e prevenir regressões, foram adicionados dois testes específicos em testes/test_medicao.py:
test_mi_parcelas: Valida o acúmulo de um grande volume de pequenos valores 10^6 parcelas de 10^-7, onde o erro de acumulação sem a compensação de Kahan diverge significativamente do valor analítico 0.1.
test_dif_grande_uso: Valida a adição de pequenas parcelas a um valor acumulado de grande magnitude (como somar 1.0 a 10^16), evitando que a parcela menor seja absorvida devido ao limite de precisão dos ponteiros flutuantes.

Os testes de aceitação iniciais não detectaram a falha porque executavam poucas iterações e utilizavam operandos de magnitudes muito semelhantes. Nesses cenários de baixo volume, o erro numérico acumulado pela soma simples permaneceu dentro das margens de tolerância padrão do pytest.approx ou math.isclose, permitindo que o código defeituoso passasse sem emitir alertas.

### R10 — Precisão × exatidão

A spline cúbica possui maior exatidão em regimes não lineares por ajustar a curvatura física real da bomba, mas menor precisão por ser sensível a ruídos locais dos dados. A regressão linear apresenta menor exatidão se o comportamento for curvo (viés de modelagem), porém entrega maior precisão e estabilidade ao filtrar oscilações estocásticas e manter a incerteza constante.
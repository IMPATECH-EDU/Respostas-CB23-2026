# Relatório — Madson dos Santos Silva (3533)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

Python 3.13.7

=== Etapa 0: ambiente ===
Python 3.13.7 | NumPy 2.5.4 | fornecido 2.0

### R1 — Expressões regulares

Uma string como `"PT101 "` (com espaço no final) ou `"PT101X"` começa com o padrão da tag, sendo aceita pelo `re.match` no início da palavra. No entanto, ela possui lixo residual, sendo rejeitada pelo `re.fullmatch`. A consequência para `valida_tag` é que usar `fullmatch` nos protege de falsos positivos, garantindo rigorosamente que a string inteira é válida, sem caracteres ocultos no final.

### R2 — Linhas inválidas

A função `ler_log` devolve as linhas descartadas para viabilizar auditorias na qualidade dos dados. Se descartássemos as falhas em silêncio, uma pane grave (ex: formato de data do SCADA desconfigurado ou sensor retornando letras) passaria despercebida. O sistema processaria menos dados sem gerar alertas, causando análises incompletas e baseando decisões de engenharia em dados corrompidos.

### R3 — Late binding

A falha ocorre porque a `lambda` no laço do código original cria uma referência à variável iteradora `k`, e não ao seu valor. Ao fim do laço, `k` é `0.1` (referente ao último sensor, FT201), fazendo todos os conversores usarem esse fator (`4095 * 0.1 = 409.5`). O script não tem esse problema porque o `criar_conversores` usa um escopo fechado (seja por um argumento default `k=k` ou factory) que "congela" o valor isolado por tag.

### R4 — Escala nominal

A hipótese principal é que o sensor real instalado no campo sofreu degradação ou possui calibração com desvio (erro de offset ou de ganho), não acompanhando a escala puramente teórica nominal fornecida pela fábrica. No código-base, a explicação dessa diferença encontra-se no módulo da simulação (`fornecido/simulador.py`), onde ruídos e distorções na conversão analógica são inseridos intencionalmente.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: "Adiciona previsoes no relatorio"

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 18 | 18.0x |
| Tempo do laço / tempo vetorizado | 50 | 20.8x |
| Tempo da compreensão / tempo do laço | 0.7 | 0.93x |

A diferença expressiva no tempo vetorizado ocorreu porque previu-se um ganho teórico alto, porém operações no NumPy têm um custo fixo de inicialização que limita o ganho em arrays menores. O `uint16 * 20` dá `16364` devido a overflow (81900 extrapola o teto de 65535, sobrando o resto de `81900 % 65536 = 16364`). Para as variáveis, eu escolheria `uint16` para contagens e `float32` para pressões.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | SerieTemporal | SerieTemporal |
| `s[1:]` | SerieTemporal | SerieTemporal  |
| `s * 2` | SerieTemporal | SerieTemporal |
| `s.sum()` | float64 | SerieTemporal |
| `s[0]` | float64 | float64 |

O resultado que mais surpreende é `s.sum()` resultar em uma `SerieTemporal` em vez de um número simples (`float64`). Isso se explica porque operações de redução do NumPy priorizam preservar o tipo retornado das classes-filhas de `ndarray` por meio do método interno `__array_wrap__`, envelopando equivocadamente o escalar de volta para a classe da série.

### R7 — Issue #4

**Sintoma**: A média móvel retornava um ponto menos (Erro "off-by-one"), com `n=570` ao invés de `571`. **Teste**: Faltava um caso cobrindo janelas extremas (como `test_tamanho_media_movel`). **Causa**: Fatiar matrizes de `cumsum` descartava a primeiríssima janela temporal. **Correção**: Inserir um `0` artificial no início da matriz via `np.insert()` antes da soma cumulativa. Os testes de aceitação originais usavam blocos onde essa falta não era fatal, camuflando o desvio.

## Marco 2

### Ambiente

Python 3.13.7 | NumPy 2.5.4 | SciPy 1.18.1 | fornecido 4.0 | matrícula 3533

### R8 — Derivada numérica

De `h = 1` (erro `1.658e-05`) até `h = 1e-5` (erro mínimo `6.224e-10`), domina o **erro de truncamento** da diferença adiante, que é proporcional a `h` e cai cerca de 10 vezes a cada passo. Abaixo de `1e-5`, domina o **erro de arredondamento** (cancelamento catastrófico em `f(x + h) - f(x)` dividido por um `h` muito pequeno), fazendo o erro crescer até `2.134e-01`. Em `h = 1e-14`, o passo é menor que metade do ULP de `1000.0` em `float64`, então `1000.0 + 1e-14 == 1000.0`; assim, `f(x + h) - f(x)` dá exatamente `0`, a aproximação vale `0` e o erro absoluto é igual à própria derivada exata (`0.213432888873`).

### R9 — Issue #7

Testes de regressão: `test_kahan_um_milhao_de_decimos` e `test_kahan_parcelas_pequenas_apos_grande`. No código original, `t` já era o resultado arredondado de `self._soma + y`; ao calcular `t - (self._soma + y)`, a mesma soma arredondada era subtraída de si mesma, resultando sempre em `0.0` (sem compensação), enquanto `(t - self._soma) - y` primeiro recupera a parte de `y` que efetivamente entrou em `t` e depois obtém o erro perdido. Os testes de aceitação não pegaram o defeito porque somavam apenas 10 parcelas de `0.1` e validavam com `math.isclose(..., 1.0)`, tolerância larga demais para um erro acumulado tão pequeno.

### R10 — Precisão × exatidão

**Precisão** é a repetibilidade (dispersão) das leituras, medida pelo desvio padrão: para `PT102`, as curvas linear (`0.528 kPa`) e spline (`0.529 kPa`) têm praticamente a mesma precisão. **Exatidão** é a proximidade da média ao valor verdadeiro, refletida pelo viés: a spline é muito mais exata (`380.0 ± 1.5 kPa`, viés `0.018 kPa`) do que a linear (`378.2 ± 1.5 kPa`, viés `-1.811 kPa`). A média de 595 leituras válidas reduz apenas o erro aleatório (proporcional a $1/\sqrt{n}$), mas não elimina o erro sistemático de aproximação da interpolação linear, que desloca todas as leituras na mesma direção.

## Marco 3

### R11 — Bissecção × Newton

Na Etapa 2(a), a bissecção gasta sempre 44 iterações porque o número de passos depende apenas do tamanho do intervalo inicial (`[2, 15]`, largura `13`) e da tolerância (`1e-12`): $\lceil \log_2(13 / 10^{-12}) \rceil = 44$, independentemente da função ou do Reynolds. Ordem de convergência 2 (quadrática) significa que $e_{k+1} \approx C \cdot e_k^2$, ou seja, o número de dígitos corretos dobra a cada iteração — como visto em `Re = 1e4`, onde os erros caem de `5.0e-02` para `2.3e-05` e depois `5.0e-12` (ordem `2.00`). O Newton falha, mas a bissecção não, quando a derivada se anula (`f'(x) = 0`) em algum ponto iterado ou quando o chute inicial está longe da raiz e faz as iterações divergirem ou saírem do domínio, enquanto a bissecção sempre converge havendo troca de sinal em `[a, b]`.

### R12 — Issue #9

Testes de regressão: `test_newton_colebrook_poucas_iteracoes` e `test_newton_convergencia_quadratica_raiz_de_2`. Calcular a derivada apenas uma vez transforma o método de Newton no método da corda ($x_{k+1} = x_k - f(x_k)/f'(x_0)$), cuja função de iteração tem derivada $g'(x^*) = 1 - f'(x^*)/f'(x_0) \neq 0$ na raiz, deixando a convergência apenas linear em vez de quadrática. Os testes de aceitação não pegaram o defeito porque verificavam apenas se `resultado.convergiu` era `True` e se a raiz obtida estava próxima de $\sqrt{2}$, sem checar o número de iterações nem a ordem de convergência.
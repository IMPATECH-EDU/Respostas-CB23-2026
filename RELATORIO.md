# Relatório — Arthur Adriano Jacometi Barbosa (3544)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->
/home/al.arthur.barbosa/venvs/prog2-venv/bin/python

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

- A string `"PT101 extra"` (ou `"PT101\n"`) é aceita por `re.match(r"[A-Z]{1,2}[0-9]{1,3}", s)` porque `match` ancora apenas no início da string e ignora o sufixo, mas é rejeitada por `re.fullmatch`, que exige correspondência do início ao fim.
- Em `valida_tag`, usar `re.match` aceitaria tags malformadas que começam com um código válido (como `"PT1010"` ou `"PT101 "`), permitindo a entrada de identificadores inválidos no sistema.

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->
- `ler_log` devolve `invalidas` para permitir auditoria e diagnóstico de falhas de coleta ou formatação sem interromper o processamento dos registros válidos.
- Em uma estação elevatória, descartar linhas em silêncio esconderia falhas intermitentes de um sensor (como perda de comunicação ou firmware enviando campo corrompido), mascarando períodos sem monitoramento de pressão ou nível.

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->
- Na compreensão `{tag: (lambda c: c * k) ...}`, `k` não é capturado por valor a cada iteração, mas buscado no escopo envolvente apenas quando a função é chamada (*late binding*); ao fim do laço, `k` vale `0.1` (escala de `"FT201"`), fazendo `4095 * 0.1 = 409.5`.
- Em `criar_conversores` (`elevatoria/dados.py`), o parâmetro padrão `f=fator` avalia e vincula o valor numérico atual no momento em que cada `lambda` é criada, preservando a escala correta de cada tag.


### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

- A diferença ocorre porque o transmissor PT102 possui offset de zero vivo (4–20 mA, onde a contagem mínima 819 corresponde a 0 kPa, e não 0) ou curva de calibração distinta da escala linear simples `600 / 4095`.
- No código da base (`fornecido/simulador.py`), a geração das contagens de pressão aplica essa relação afim com offset/calibração real da planta ao calcular `verdade["pressao_recalque"]`.


### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: c6a157d

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ~14x | 18,00x|
| Tempo do laço / tempo vetorizado | ~10x | 21,96x |
| Tempo da compreensão / tempo do laço | ~0,90x | 0,93x |
<!-- Explique a maior diferença entre previsão e medição; por que uint16 * 20 dá 16364; que dtype você escolheria para contagens e para kPa. -->

- **Previsão × medição e overflow:** A maior diferença costuma aparecer na aceleração vetorizada (21,96× medido: 2,077 ms contra 45,599 ms do laço) porque o NumPy executa a operação em C sobre memória contígua sem *overhead* de interpretador nem *boxing* de objetos `int`/`float`; já `np.array([4095], dtype=np.uint16) * 20` resulta em `16364` porque o produto `81900` excede o máximo de 16 bits sem sinal ($65535$) e sofre *wrap-around* módulo $2^{16}$ ($81900 - 65536 = 16364$).
- **Escolha de `dtype`:** Para contagens do ADC (inteiros de 0 a 4095), `uint16` é ideal por representar exatamente o intervalo sem desperdício de memória (2 B/elemento); para pressão em kPa (grandezas físicas contínuas e frações), `float32` ou `float64` evita truncamento decimal e estouro em cálculos intermediários.
### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | `SerieTemporal` |
| `s[1:]` | `SerieTemporal` | `SerieTemporal` |
| `s * 2` | `SerieTemporal` | `SerieTemporal` |
| `s.sum()` | `float` | `float64` |
| `s[0]` | `float` | `float64` |

<!-- Explique o resultado que mais surpreendeu você. -->

O resultado que mais surpreendeu foi `s[0]` e `s.sum()` retornarem `np.float64` em vez do `float` nativo do Python, enquanto operações vetoriais (`s + s`, `s * 2`) e fatiamentos (`s[1:]`) preservam automaticamente a subclasse `SerieTemporal` graças ao mecanismo de `__array_finalize__` / *views* do NumPy.

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->

- **Sintoma e regressão:** Para uma série de $n$ pontos e janela $k$, `media_movel` devolvia $n - k$ valores em vez de $n - k + 1$ (ex.: 570 para $n=600, k=30$), descartando a primeira janela; coberto pelo teste `TestMediaMovel.test_media_movel_simples`.
- **Causa e correção:** O código original fazia `acumulada[janela:] - acumulada[:-janela]` diretamente sobre `np.cumsum(self)`, omitindo a diferença `acumulada[janela - 1] - 0` da primeira janela; a correção insere `0.0` no início da soma acumulada (`np.insert(np.cumsum(self), 0, 0.0)`), alinhando os índices.
- **Lacuna nos testes:** Os testes de aceitação verificavam apenas propriedades gerais (como tipo de retorno ou valores internos) sem checar o comprimento exato $n - k + 1$ nem casos de borda como $k = n$ (que antes devolvia série vazia), caso coberto pelo meu teste `TestMediaMovel.test_media_movel_janela_total`.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->
```text
Python 3.13.15 | NumPy 2.5.2 | SciPy 1.18.0 | fornecido 4.0 | matrícula 3544

### R8 — Derivada numérica

<!-- Com a tabela da Etapa 1(b): por que o erro diminui quando h vai de 1 até cerca de 1e-5 e
depois volta a crescer? Que tipo de erro domina em cada lado? Por que, em h = 1e-14, o erro
é exatamente a própria derivada? (Experimente 1000 + 1e-14 == 1000.) -->

De $h = 1$ até $h = 10^{-5}$, o erro cai linearmente com $h$ (de $1{,}658\times 10^{-5}$ até o mínimo de $6{,}224\times 10^{-10}$) porque domina o erro de truncamento $O(h)$ da série de Taylor na diferença adiante. Para $h < 10^{-5}$, domina o erro de arredondamento (cancelamento catastrófico em $f(x+h) - f(x)$ dividido por $h$ cada vez menor), fazendo o erro subir até $3{,}550\times 10^{-1}$ em $h = 10^{-13}$. Em $h = 10^{-14}$, $c + h = 1000 + 10^{-14}$ arredonda para o próprio $1000$ em float64 (pois o épsilon da máquina nessa escala é $\approx 1{,}14\times 10^{-13}$), fazendo $(f(c+h) - f(c))/h = 0$ e tornando o erro $|0 - f'(c)| = 0{,}2134$ igual à própria derivada.   

### R9 — Issue #7

<!-- Os nomes dos seus testes de regressão; a causa: por que, em ponto flutuante,
t - (s + y) dá sempre zero, embora seja algebricamente igual a (t - s) - y; por que os testes
de aceitação não pegaram o defeito. -->

De $h = 1$ até $h = 10^{-5}$, o erro cai linearmente com $h$ (de $1{,}658\times 10^{-5}$ até o mínimo de $6{,}224\times 10^{-10}$) porque domina o erro de truncamento $O(h)$ da série de Taylor na diferença adiante. Para $h < 10^{-5}$, domina o erro de arredondamento (cancelamento catastrófico em $f(x+h) - f(x)$ dividido por $h$ cada vez menor), fazendo o erro subir até $3{,}550\times 10^{-1}$ em $h = 10^{-13}$. Em $h = 10^{-14}$, $c + h = 1000 + 10^{-14}$ arredonda para o próprio $1000$ em float64 (pois o épsilon da máquina nessa escala é $\approx 1{,}14\times 10^{-13}$), fazendo $(f(c+h) - f(c))/h = 0$ e tornando o erro $|0 - f'(c)| = 0{,}2134$ igual à própria derivada.   

### R10 — Precisão × exatidão

<!-- Na Etapa 3(b), as curvas linear e spline dão praticamente o mesmo desvio, mas viéses bem
diferentes para PT102. Explique a diferença entre precisão e exatidão com esses números e
por que a média de quase 600 leituras não elimina o viés da curva linear. -->

Para PT102, as curvas linear e spline apresentam praticamente a mesma precisão (dispersão interna das leituras em torno da própria média), com desvios padrão amostrais de $0{,}545\text{ kPa}$ e $0{,}546\text{ kPa}$. Porém, diferem na exatidão (proximidade em relação ao valor real de referência): a spline tem viés de apenas $-0{,}027\text{ kPa}$ (média $380{,}0\text{ kPa}$), enquanto a linear tem viés sistemático de $-1{,}857\text{ kPa}$ (média $378{,}1\text{ kPa}$). Aumentar o número de leituras ($n \approx 600$) reduz apenas o erro padrão aleatório ($\sigma/\sqrt{n}$), mas não elimina um erro sistemático do modelo (aproximação linear por partes de uma curva não linear).

## Marco 3

### R11 — Bissecção × Newton

<!-- Na Etapa 2(a), a bissecção gasta sempre 44 iterações, qualquer que seja o Reynolds. Por
quê? Com os erros da Etapa 2(b), explique o que significa ordem de convergência 2. Dê uma
situação em que o Newton falha e a bissecção não. -->

Na Etapa 2(a), a bissecção parte sempre do mesmo intervalo inicial $[2, 15]$ e para quando $(b - a)/2^k < \text{tol} = 10^{-12}$, exigindo $\lceil \log_2(13 / 10^{-12}) \rceil = 44$ iterações independentemente do número de Reynolds (pois a largura depende apenas de $a$, $b$ e $\text{tol}$, não da função)[cite: 21, 29]. Na Etapa 2(b), para $\text{Re} = 10^4$, os erros de Newton caem como $2{,}9 \to 5{,}0\times 10^{-2} \to 2{,}3\times 10^{-5} \to 5{,}0\times 10^{-12}$, o que caracteriza **ordem de convergência 2** ($e_{k+1} \approx C\,e_k^2$, dobrando o número de casas decimais corretas a cada passo)[cite: 29]. O Newton falha enquanto a bissecção converge quando há derivada nula ($f'(x_k) = 0$) ou quando o chute inicial está longe da raiz e a tangente lança a próxima aproximação para fora do domínio (por exemplo, $x \le 0$ no logaritmo de Colebrook)[cite: 21, 27].


### R12 — Issue #9

<!-- Os nomes dos seus testes de regressão; por que calcular a derivada uma vez só deixa a
convergência linear; por que os testes de aceitação não pegaram o defeito. -->

Testes de regressão criados em `testes/test_operacao.py`: `test_newton_colebrook_poucas_iteracoes` e `test_newton_convergencia_quadratica_polinomio`. Calcular `derivada = self._derivada(f, x)` apenas uma vez fora do laço transforma o método de Newton no método das cordas (inclinação fixa $f'(x_0)$), cuja taxa de redução do erro é constante ($e_{k+1} \approx |1 - f'(r)/f'(x_0)|\,e_k$), degradando a convergência de quadrática ($p = 2$) para **linear** ($p = 1$)[cite: 18, 27]. Os testes de aceitação iniciais não pegaram o defeito porque verificavam apenas se o resultado final convergido (`res.raiz` e `res.convergiu`) estava dentro da tolerância, sem limitar o número máximo de iterações nem medir a ordem de convergência $p$[cite: 17].

## Marco 4

### R13 — Integração e descontinuidade

<!-- Na Etapa 1(b), integrando o custo do dia de uma vez, a ordem observada cai para cerca
de 1, no trapézio e no Simpson; integrando cada faixa separadamente, voltam as ordens 2 e 4.
Por quê? -->

As ordens teóricas 2 (trapézio) e 4 (Simpson) exigem que o integrando seja suave (classes $C^2$ e $C^4$) em todo o intervalo de integração. Ao integrar o custo do dia de uma só vez, os saltos descontínuos da tarifa às 18 h e 21 h violam a suavidade da função, degradando o erro global para $O(h)$ (ordem observada $1{,}00$ no trapézio e $0{,}65$ no Simpson)[cite: 30]. Quando se integra faixa por faixa, a tarifa é constante dentro de cada subintervalo, a função volta a ser suave e recuperam-se as ordens teóricas ($2{,}00$, com erro $6{,}3 \times 10^{-4}$, e $4{,}00$, com erro $8{,}1 \times 10^{-8}$ em $n=110$)[cite: 30].

### R14 — Issue #11

<!-- Os nomes dos seus testes de regressão; a causa do defeito; por que os testes de
aceitação não o pegaram; por que a regra de Simpson não serve para o registro do dia. -->

Testes de regressão adicionados em `testes/test_dia.py`: `test_trapezio_malha_irregular_funcao_linear` e `test_trapezio_registro_scada_com_falhas_funcao_constante`. O defeito estava em `Trapezio.integrar_tabela` (`elevatoria/integracao.py`), que assumia passo uniforme `h = x[1] - x[0]` em vez de somar `0.5 * (y[:-1] + y[1:]) * np.diff(x)`. Os testes de aceitação originais não detetaram o bug porque usavam apenas malhas uniformes (`np.linspace` e `np.arange`)[cite: 26, 28]. A regra de Simpson não serve para o registo do dia porque as 8 falhas do SCADA tornam os intervalos irregulares (15, 30 e 45 min), violando a exigência de malha igualmente espaçada[cite: 14, 21, 30].

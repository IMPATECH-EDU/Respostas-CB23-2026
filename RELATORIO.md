# Relatório — Ângelo Lourenço da Silva Cordeiro (3484)

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

### R1 — Expressões regulares

"PT1010": re.match só exige que o começo case, e casa "PT101", ignorando o "0" que sobra;
re.fullmatch exige que o padrão cubra a string toda e rejeita, porque \d{1,3} não aceita
quatro dígitos. Outros exemplos: "PT101 " (espaço no fim) e "B1x". Com match, valida_tag
aceitaria essas tags inválidas, e elas entrariam no sistema comosensoresdiferentes de PT101:
a contagem por tag e as séries ganhariam uma “tag fantasma”, sem erro nenhum.

### R2 — Linhas inválidas

Porque quem decide o que fazer com o descarte é quem chama: contar, mostrar ao opera
dor, recusar o arquivo se a fração de inválidas for grande. Os módulos não imprimemnada
(regra da casa), então o valor de retorno é a única forma de avisar. No log da 3484, duas
linhas dizem “falha de comunicação com a RTU”, e duas leituras vieram cortadas: descartando emsilêncio, o volume bombeado na hora (233,366 m3, calculado pelos pulsos) sairia
menor sem que ninguém soubesse que faltaram dados. Pior: se uma atualização mudasse
o formato do log, todas as linhas seriam descartadas e o sistema mostraria vazão zero em
vez de acusar o erro.

### R3 — Late binding

As três lambdas foram criadas no escopo da compreensão efecham sobre a mesma variável
k, que é lida na hora da chamada, não da criação. Quando errados["PT102"](4095) roda, a
compreensão já terminou e k vale o último fator, 0,1 (de FT201): 4095×0,1 = 409,5. O FT201
só sai certo por ser o último. Emcriar_conversores, cada chamada de _multiplicador(fator)
cria um escopo novo, com o seu próprio fator, e a lambda devolvida captura esse escopo
(closure): não há variável compartilhada que mude depois.

### R4 — Escala nominal

Hipótese: o transmissor não é linear, e a escala nominal é só a reta que liga (0,0)
a (4095,600 kPa), que acerta nas pontas e erra no meio. A explicação está em
fornecido/simulador.py, função p_real (linha 33): p = 600sin(0,5𝜋c/4095), uma curva
côncava, sempre acima da reta. Em c = 1787,92, 600sin(0,6858) = 380,0 kPa, contra
1787,92 × 600/4095 = 262,0 kPa: a reta subestima 31%. Por isso o Marco 2 troca a escala
nominal por curvas de calibração feitas com pontos medidos.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `4847ecf`

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | ≈ 20 | |
| Tempo do laço / tempo vetorizado | ≈ 300 | |
| Tempo da compreensão / tempo do laço | ≈ 0,5 | |

A maior diferença foi laço/vetorizado: 39 em vez de 300. A versão vetorizada faz duas
passadas sobre um milhão de números e cria dois arrays temporários de 8 MB (float64):
o tempo dela, 2 ms, é o de ler e escrever memória, não o de fazer as contas; e o laço do
Python 3.12 (80 ns por elemento) é mais rápido do que a previsão supunha. A memória
bateu: 8 + 28 = 36 bytes por elemento na lista (ponteiro mais objeto int) contra 2, razão
18. Já 4095 × 20 = 81900 não cabe em 16 bits (máximo 65535): o resultado dá a volta, 81900 − 65536 = 16364, sem aviso.

### R6 — Tipos da SerieTemporal (Etapa 4d)

| Expressão | Tipo previsto | Tipo observado |
| --- | --- | --- |
| `s + s` | `SerieTemporal` | |
| `s[1:]` | `SerieTemporal` | |
| `s * 2` | `SerieTemporal` | |
| `s.sum()` | escalar (`float64`) | |
| `s[0]` | escalar (`float64`) | |

s.sum() devolve uma SerieTemporal de dimensão zero, e não um número. As reduções de
uma subclasse (sum, mean, max) passam pelo mesmo mecanismo que embrulha o resultado
das operações no tipo dasubclasse, eoresultado deumareduçãototaléumarraydeforma
(). Já s[0], indexação de um elemento, devolve um escalar NumPy (np.float64), que não
é array. Fatias e operações elemento a elemento preservam o tipo, como previsto. Para ter
um número de verdade: float(s.sum()) ou s.sum().item().

### R7 — Issue #4

Sintoma: saíam n − w médias, uma a menos, e faltava a primeira janela. Testes:
TestMediaMovelRegressao, com test_quantidade_de_valores, test_primeira_janela_entra_no_
resultado e test_janela_do_tamanho_da_serie. Causa: com Sk = x0 + ⋯ + xk−1 e S0 = 0, a
janela que começa em i soma Si+w − Si; sem o S0 = 0, cumsum dá S1,…,Sn, e a diferença
acumulada[w:]- acumulada[:-w] só produz as janelas que começam em 1,…,n − w. Cor
reção: inserir o zero antes da soma acumulada. Aceitação: test_media_movel_tipo_e_erros
só confere o tipo devolvido e os ValueError das janelas 0 e 6; nunca olha os valores nem a
quantidade.

## Marco 2

### Ambiente

<!-- Cole a saída da Etapa 0 do `python marco2.py`. -->

### R8 — Derivada numérica

Para h grande domina o erro de truncamento da diferença adiante, h
2|f″|: cai 10 vezes a cada h
10 vezes menor (de1,66×10−5 em h = 1a1,65×10−9em10−4). Para h pequeno domina o de arredondamento: f(c + h) e f(c), perto de 225 kPa, concordam em quase todos os algarismos;
a subtração cancela os corretos, sobra o erro de arredondamento de f (da ordem de 𝜀|f| ≈
5×10−14), eeleédivididoporh: crescecomo1/h. Omínimoficaondeosdoisseequilibram,
em h ≈ 10−5. Em h = 10−14, 1000 + 1e-14 == 1000, porque o ulp de 1000 é 1,1 × 10−13 e
10−14 é menor que meioulp: f(c+h)−f(c) = 0, aderivada estimada é 0, e o erro é a própria
derivada, 0,2134.

### R9 — Issue #7

Testes: TestKahanRegressao, comtest_dez_decimos_dao_exatamente_um, test_parcelas_menores_
que_meio_ulp e test_um_milhao_de_pulsos. Causa: t acabou de ser calculado como fl(s + y);
recalcular s + y dá exatamente o mesmo númeroarredondado, e t−t = 0. Acompensação
ficasemprezeroeoacumulador viraasomaingênua. Em(t- s)- y,adiferençat−séexata
(os dois são próximos, lema de Sterbenz) e mede quanto de y entrou de fato; subtraindo
y, sobra menos a parte perdida. As duas expressões são iguais na álgebra porque a soma
real é associativa; a de ponto flutuante não é. Aceitação: o teste soma dez parcelas de
0,1 e confere com math.isclose(total, 1.0), cuja tolerância relativa padrão é 10−9; a soma
ingênua dá 0,9999999999999999 e passa.

### R10 — Precisão × exatidão

Precisão é a dispersão das leituras repetidas: o desvio padrão é 0,538 e 0,540 kPa, igual nas
duas curvas, porque vem do ruído do sensor. Exatidão é a distância da média ao valor
verdadeiro: a curva linear erra −1,84 kPa e a spline, −0,015 kPa. A média de 595 leituras
reduz o erro aleatório para 𝜎/√n ≈ 0,54/√595 ≈ 0,02 kPa, mas o viés da linear é sistemático:
entre dois pontos de calibração, a reta fica abaixo da curva côncava do sensor, e todas as
leituras erram no mesmo sentido. A média de erros iguais é o mesmo erro.

## Marco 3

### R11 — Bissecção × Newton

A bissecção divide o intervalo ao meio a cada passo e para quando a largura fica menor que
tol: são ⌈log2
(13/10−12)⌉ = ⌈43,6⌉ = 44 iterações, um número que só depende do tamanho
do intervalo e da tolerância. OReynoldsmudaafunção,masabissecçãosóusaosinaldeg.
Ordem2 quer dizer ek+1 ≈ Ce2
k: emRe = 104,oserros5,0×10−2 → 2,3×10−5 → 5,0×10−12
mostram o número de algarismos corretos dobrando a cada passo (C ≈ 0,009); a ordem estimada é 2,00. O Newtonfalha comumchutelongedaraiz: numaregiãoondeg′ équase
zero, a tangente manda o iterado para longe, e em funções como x3 − 2x + 2, a partir de
x0 = 0, ele entra no ciclo 0,1,0,1,… A bissecção, com troca de sinal no intervalo, converge
sempre.

### R12 — Issue #9

Testes: TestNewtonRegressao, com test_colebrook_em_re_1e4 (no máximo 6 iterações), test_
raiz_de_dois (no máximo 6, e não umas 30) e test_derivada_calculada_em_cada_ponto (a de
rivada é chamada uma vez por iteração, nospontosdohistórico). Porquelinear: comd0 =
g′(x0) fixo, xk+1 = xk − g(xk)/d0 é uma iteração de ponto fixo com 𝜑′(r) = 1 − g′(r)/d0 ≠ 0,
logo ek+1 ≈ (1 − g′(r)/d0)ek. Em x2 − 2 a partir de x0 = 1 a constante é 1 − 2√2/2 = 0,41:
32 iterações contra 5; em Colebrook com Re = 104, é 0,04: 10 iterações contra 5. 

## Marco 4

### R13 — Integração e descontinuidade

A tarifa salta às 18 h e às 21 h, então o integrando é descontínuo. As ordens 2 e 4 vêm das
fórmulas de erro, −(b−a)h2/12
f″ e −(b−a)h4/180 f(4), que exigem f″ e f(4) limitadas. No subintervalo
que contém um salto, a regra erra uma fração de h vezes o tamanho do salto, que depende
de onde o salto cai: um erro 𝒪(h), que domina todo o resto. Daí ordem 1 no trapézio; no
Simpson, os pesos 4 e 2 alternados fazem a constante oscilar de uma malha para outra, e a
ordem medida sai 0,65. Integrando cada faixa separadamente, com os limites exatamente
em 18 he 21h,cadaparte é suave e as ordens voltam a 2 e 4.

### R14 — Issue #11

Testes: TestTrapezioComFalhas, com test_reta_em_malha_irregular, test_apagar_leituras_de_
uma_reta e test_volume_do_dia_com_falhas. Causa: a regra usava uma única largura, x[1]
x[0] = 15 min, para todos os trapézios; nos 8 intervalos de 30 min a área era contada pela
metade, como se o dia tivesse 22 horas: o volume caía de 3894 para 3566 m3, 8,4% a me
nos. Aceitação: todosostestesusammalhasregulares(np.arange(0, 24, 1.5), np.linspace),
onde a largura única está certa. Simpson: a regra supõe pontos igualmente espaçados (a
parábola de cada par de intervalos tem pesos h
3, 4h
3 , h
3 com o mesmo h) e número par de in
tervalos; o registro tem intervalos de 15 e 30 min, eaimplementaçãorecusacomValueError.

## Declaração de uso de IA

<!-- Exigida pela política de IA do plano de ensino de CB23. O enunciado do projeto autoriza
IA para ajudar a escrever o código. Revise e complete antes de marcar o PR como pronto. -->

**Onde usei.** Usei o Gemini como ajuda no desenvolvimento, principalmente no código do Marcos 1 e 2:

- `elevatoria/dados.py` (issues #1): a IA partiu do meu rascunho de `LINHA`, `ler_log`,
  `contagem_por_tag`, `serie` e `criar_conversores`, corrigiu `valida_tag` e `serie
- `elevatoria/serie.py` (correção da #4 e `reamostrar`), `elevatoria/acumuladores.py` (#7),

**Como usei.** Eu escrevi o código e os testes a partir dos enunciados e das docstrings,
rodei os testes e os quatro scripts e conferi com ajuda da IA.

Li o código e os testes de cada issue e rodei na minha máquina
         python -m unittest discover -v (97 testes, todos passando) e os quatro marco*.py.

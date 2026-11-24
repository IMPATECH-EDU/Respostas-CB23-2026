## Marco 1
Resolve as issues #1 a #5 do enunciado.

### O que mudou
- Em Issue 1:
  - Definição de Expressão Regular para parsear o log
  - Implementação de ler_log, valida_tag, contagem_por_tag, serie
- Em Issue 2:
  - Implementação de criar_conversores
  - Identificação e correção de problema: Late binding
- Em Issue 3:
  - Implementação de medir_memoria e medir_tempos
  - Previsão e medição de o espaço e tempo gasto em armazenamento e acesso de um milhão de contagens em diferentes coleções/estruturas
- Em issue 4:
  - Correção de Bug em test_dados
  - Implementação de mais testes unitários (unittest)
- Em issue 5:
  - Implementação de SerieTemporal.reamostrar

### Como testei
- `python -m unittest discover -v`: Ran 38 tests in 0.060s OK
Executa 38 testes, e todos eles passam.

- `python marco1.py`: todos os assert passam.
Marco 1: todos os assert passaram.

Comando executado:

```powershell
python -m unittest discover -v
```

Resultado:

```text
test_contagem_por_tag (fornecido.testes_aceitacao.test_aceitacao_m1.TestContagemESerie.test_contagem_por_tag) ... ok
test_serie_ignora_registros_sem_a_chave (fornecido.testes_aceitacao.test_aceitacao_m1.TestContagemESerie.test_serie_ignora_registros_sem_a_chave) ... ok
test_cada_tag_usa_o_seu_fator (fornecido.testes_aceitacao.test_aceitacao_m1.TestConversores.test_cada_tag_usa_o_seu_fator) ... ok
test_instante (fornecido.testes_aceitacao.test_aceitacao_m1.TestLerLog.test_instante) ... ok
test_registro_imutavel (fornecido.testes_aceitacao.test_aceitacao_m1.TestLerLog.test_registro_imutavel) ... ok
test_texto_pequeno (fornecido.testes_aceitacao.test_aceitacao_m1.TestLerLog.test_texto_pequeno) ... ok
test_texto_vazio (fornecido.testes_aceitacao.test_aceitacao_m1.TestLerLog.test_texto_vazio) ... ok
test_tipos_dos_valores (fornecido.testes_aceitacao.test_aceitacao_m1.TestLerLog.test_tipos_dos_valores) ... ok
test_chaves_e_tamanhos (fornecido.testes_aceitacao.test_aceitacao_m1.TestMemoriaETempo.test_chaves_e_tamanhos) ... ok
test_conversoes_equivalentes (fornecido.testes_aceitacao.test_aceitacao_m1.TestMemoriaETempo.test_conversoes_equivalentes) ... ok
test_medir_tempos (fornecido.testes_aceitacao.test_aceitacao_m1.TestMemoriaETempo.test_medir_tempos) ... ok
test_memoria_rejeita_2d (fornecido.testes_aceitacao.test_aceitacao_m1.TestMemoriaETempo.test_memoria_rejeita_2d) ... ok
test_casa_linha_valida (fornecido.testes_aceitacao.test_aceitacao_m1.TestPadraoLinha.test_casa_linha_valida) ... ok
test_e_padrao_compilado_verbose (fornecido.testes_aceitacao.test_aceitacao_m1.TestPadraoLinha.test_e_padrao_compilado_verbose) ... ok
test_grupos_nomeados (fornecido.testes_aceitacao.test_aceitacao_m1.TestPadraoLinha.test_grupos_nomeados) ... ok
test_rejeita_linhas_corrompidas (fornecido.testes_aceitacao.test_aceitacao_m1.TestPadraoLinha.test_rejeita_linhas_corrompidas) ... ok
test_blocos (fornecido.testes_aceitacao.test_aceitacao_m1.TestReamostrar.test_blocos) ... ok
test_k_invalido (fornecido.testes_aceitacao.test_aceitacao_m1.TestReamostrar.test_k_invalido) ... ok
test_de_lista (fornecido.testes_aceitacao.test_aceitacao_m1.TestSerieTemporal.test_de_lista) ... ok
test_fatia_e_imutabilidade (fornecido.testes_aceitacao.test_aceitacao_m1.TestSerieTemporal.test_fatia_e_imutabilidade) ... ok
test_media_movel_tipo_e_erros (fornecido.testes_aceitacao.test_aceitacao_m1.TestSerieTemporal.test_media_movel_tipo_e_erros) ... ok
test_normalizar (fornecido.testes_aceitacao.test_aceitacao_m1.TestSerieTemporal.test_normalizar) ... ok
test_variacao_e_amplitude (fornecido.testes_aceitacao.test_aceitacao_m1.TestSerieTemporal.test_variacao_e_amplitude) ... ok
test_invalidas (fornecido.testes_aceitacao.test_aceitacao_m1.TestValidaTag.test_invalidas) ... ok
test_validas (fornecido.testes_aceitacao.test_aceitacao_m1.TestValidaTag.test_validas) ... ok
test_data_impossivel_preserva_linha_como_invalida (testes.test_dados.TestLerLog.test_data_impossivel_preserva_linha_como_invalida)
Uma data impossível faz a linha original aparecer entre as inválidas. ... ok
test_data_ou_hora_impossivel (testes.test_dados.TestLerLog.test_data_ou_hora_impossivel)
Datas e horas impossíveis tornam as linhas inválidas. ... ok
test_linha_com_formato_invalido (testes.test_dados.TestLerLog.test_linha_com_formato_invalido)
Uma linha que não corresponde ao padrão é descartada. ... ok
test_linha_invalida_preserva_texto_original (testes.test_dados.TestLerLog.test_linha_invalida_preserva_texto_original)
As linhas inválidas são devolvidas exatamente como recebidas. ... ok
test_linhas_vazias_sao_ignoradas (testes.test_dados.TestLerLog.test_linhas_vazias_sao_ignoradas)
Linhas vazias ou só com espaços não são registros nem linhas inválidas. ... ok
test_preserva_ordem_dos_registros (testes.test_dados.TestLerLog.test_preserva_ordem_dos_registros)
Os registros válidos mantêm a ordem das linhas de entrada. ... ok
test_texto_vazio (testes.test_dados.TestLerLog.test_texto_vazio)
Texto vazio retorna listas vazias. ... ok
test_lista_vazia (testes.test_dados.TestPorTagExemplo.test_lista_vazia)
Sem registros, por_tag devolve uma lista vazia. ... ok
test_media_movel (testes.test_dados.TestSerieTemporal.test_media_movel)
Verifica o tamanho e os valores da média móvel de três pontos. ... ok
test_media_movel_600_pontos_janela_30 (testes.test_dados.TestSerieTemporal.test_media_movel_600_pontos_janela_30)
test_media_movel com um array de 600 pontos e janela de 30. ... ok
test_media_movel_janela_do_tamanho_da_serie (testes.test_dados.TestSerieTemporal.test_media_movel_janela_do_tamanho_da_serie)
Uma janela do tamanho da série produz exatamente uma média. ... ok
test_media_movel_rejeita_janela_invalida (testes.test_dados.TestSerieTemporal.test_media_movel_rejeita_janela_invalida)
Uma janela zero ou maior que a série levanta ValueError. ... ok
test_reamostrar_calcula_medias_por_bloco (testes.test_dados.TestSerieTemporalReamostrar.test_reamostrar_calcula_medias_por_bloco)
Cada bloco completo é substituído pela sua média. ... ok

----------------------------------------------------------------------
Ran 38 tests in 0.030s

OK
```

Comando executado:

```powershell
python marco1.py
```

Resultado:

```text
(.venv) PS D:\Projetos\IMPATech\Programacao_2\Respostas-CB23-2026>                                                               
=== Etapa 0: ambiente ===                                                 
Python 3.12.10 | NumPy 2.5.3 | fornecido 1.0

=== Etapa 1: leitura do log ===
Número de registros válidos: 2404
Número de linhas inválidas: 4

=== Etapa 2: lambda e compreensões ===
Valor obtido a partir da conversão da média das contagens normais de PT102 (até 2000) com a escala nominal: 1787.94
Pressão Recalque obtida do dicionário de verdade: 380.0

=== Etapa 3: memória e tempo ===
--------------------------------------------------------------
Estrutura       Bytes/Elem      Bytes Totais    Razão vs Lista 
--------------------------------------------------------------
list            36.0            36000056        1.00           
array('H')      2.0             2000000         0.06           
uint16          2.0             2000000         0.06           
int32           4.0             4000000         0.11           
int64           8.0             8000000         0.22           
float32         4.0             4000000         0.11           
float64         8.0             8000000         0.22           



--------------------------------------------------
Versão          Tempo (ms)      Aceleração vs Laço
--------------------------------------------------
laço            161.782         1.00           
compreensão     104.622         1.55           
map+lambda      138.103         1.17           
vetorizado      6.638           24.37          



------------------------------------------
Variável        Dtype / Resultado        
------------------------------------------
misto           <U32                     
estouro[0]      16364                    

=== Etapa 4: a série de pressão ===
Média: 1791.267
Desvio Padrão: 36.422
Amplitude: 409.000


Tamanho da média móvel: 571
Mínimo com a média móvel: 1786.233
Mínimo na série original: 1780.000
Máximo com a média móvel: 1814.733
Máximo na série original: 2189.000


Tipo de 's + s': SerieTemporal
Tipo de 's[1:]': SerieTemporal
Tipo de 's * 2': SerieTemporal
Tipo de 's.sum()': SerieTemporal
Tipo de 's[0]': float64

Marco 1: todos os assert passaram.
```


### Pontos de atenção para o revisor
- A resposta R7 do RELATORIO.md ultrapassa o limite de 6 linhas para registrar o raciocínio completo sobre o defeito da issue #4 e a sua correção.

## Marco 2
Resolve as issues #6 e #7 do enunciado.

### O que mudou
- Em Issue 6:
  - Implementação de medir e altura_manometrica, em elevatoria/medicao.py
  - Validações de medir: ValueError para u_sistematica negativa, tag com menos de 2 leituras, MAD = 0 e menos de 2 leituras válidas
  - Correção em serie (Marco 1): leituras com valor 0 não são mais descartadas
- Em Issue 7:
  - Correção do AcumuladorKahan: a correção passa a ser calculada como (t - s) - y
  - Testes de regressão: test_soma_float e test_parcelas_pequenas_nao_se_perdem
- Testes de medir em testes/test_medicao.py
- Seção Marco 2 do RELATORIO.md (R8 a R10)

### Como testei
- `python -m unittest discover -v`: 58 testes, todos passando
- `python marco1.py` e `python marco2.py`: todos os assert passam
- Os testes de regressão da issue #7 falham com o código original do AcumuladorKahan

### Pontos de atenção para o revisor
- Foi orientado que os commits não serão considerados durante a avaliação, apenas a versão final.

## Marco 3
Resolve as issues #8 e #9 do enunciado.

### O que mudou
- Implementei `ponto_operacao` para encontrar a vazão em que a altura da bomba se iguala à altura exigida pela tubulação.
- Implementei `ordem_convergencia` usando os três últimos erros acima do piso definido no contrato.
- Corrigi o método de Newton para recalcular a derivada em cada aproximação, restaurando a convergência quadrática.
- Acrescentei testes de regressão para o Newton e testes adicionais para `ordem_convergencia`.
- Registrei no `RELATORIO.md` as respostas R11 e R12.

### Como testei
- `python -m unittest discover -v`: 4 testes próprios do Marco 3, além do teste de exemplo; a saída registrada no relatório geral informa 58 testes passando.
- `python marco3.py`: as etapas de interpolação, fator de atrito e ponto de operação passaram, conforme registrado no relatório.
- Os testes de regressão da issue #9 verificam o passo de Newton e sua convergência em até cinco iterações para o caso descrito.

### Pontos de atenção para o revisor
- A função `ponto_operacao` compõe a curva da bomba, o modelo da tubulação e o resolvedor fornecido, propagando erros do resolvedor conforme o contrato.
- Os testes adicionais cobrem o descarte de erros no piso e o escalonamento do piso pelo módulo da raiz.

## Marco 4
Resolve as issues #10 e #11 do enunciado.

### O que mudou
- Implementei `ajustar_polinomio` por mínimos quadrados, com coeficientes em ordem crescente e validação das entradas.
- Implementei `dia_de_operacao` para calcular volume, energia e custo por faixa tarifária.
- Corrigi `Trapezio.integrar_tabela` para usar a largura de cada intervalo da malha, incluindo registros com leituras ausentes.
- Acrescentei testes de regressão para a malha irregular e testes de validação para as funções da issue #10.
- Registrei as respostas R13 e R14 no `RELATORIO.md`.

### Como testei
- A executar: `python -m unittest discover -v` — preencher com o total após rodar os testes.
- A executar: `python marco4.py` — confirmar que todas as etapas e asserts passam.
- Os testes de regressão da issue #11 devem falhar com a implementação original do trapézio.

### Pontos de atenção para o revisor
- O ajuste usa `np.polynomial.polynomial.polyfit`, que fornece coeficientes na ordem crescente exigida pelo projeto.
- O custo é integrado separadamente em cada faixa, respeitando as mudanças de tarifa.


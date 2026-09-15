# Respostas: Pilha e Fila encadeadas

---

## 1. Organização e execução

### Arquivos

* `P06_3528_pilha_encadeada.py`
    * Questão 1: classes `Node`, `PilhaEncadeada` e `PilhaVaziaError`.
* `P06_3528_fila_encadeada.py`
    * Questão 2: classes `FilaEncadeada` e `FilaVaziaError`.
    * Importa `PilhaEncadeada` do arquivo da Questão 1.
* `test_estruturas.py`
    * Testes `unittest` das duas estruturas.

### Como executar

* Demonstração da pilha: `python P06_3528_pilha_encadeada.py`
* Demonstração da fila: `python P06_3528_fila_encadeada.py`
* Testes: `python -m unittest test_estruturas -v`

Nenhum arquivo depende de bibliotecas externas, e todos os `print` estão dentro de blocos `if __name__ == "__main__":`.

### Tratamento de erros

* Operações sobre estrutura vazia levantam `PilhaVaziaError` ou `FilaVaziaError`, ambas subclasses de `IndexError`, com mensagem descritiva.
* Nenhuma operação retorna `None` para sinalizar erro.
* Se a estrutura está vazia é decidido pelo contador, nunca pelo valor do topo.

### Decisão de projeto

* Além dos métodos exigidos, `PilhaEncadeada` oferece `__iter__`, que percorre a pilha do topo para a base sem modificá-la.
* É o que permite à fila implementar `__repr__` em O(N) sem acessar atributos internos e sem esvaziar e reconstruir as pilhas.

---

## 2. Complexidade da PilhaEncadeada

* `push(item)`: O(1)
    * Cria um nó e atualiza a referência do topo e o contador. Não percorre a lista.
* `pop()`: O(1)
    * Lê o nó do topo, move o topo para `proximo` e decrementa o contador.
* `topo()`: O(1)
    * Uma leitura do valor do nó do topo.
* `esta_vazia()`: O(1)
    * Uma comparação do contador com 0.
* `len()`: O(1)
    * Retorna o contador `_tamanho`, atualizado incrementalmente em `push` e `pop`.
* `repr()`: O(N)
    * Percorre os N nós uma vez, do topo para a base.

---

## 3. Complexidade da FilaEncadeada

* `enfileirar(item)`
    * Pior caso de uma chamada isolada: O(1).
    * Amortizada: O(1).
* `desenfileirar()`
    * Pior caso de uma chamada isolada: O(N).
    * Amortizada: O(1).
* `frente()`
    * Pior caso de uma chamada isolada: O(N).
    * Amortizada: O(1).
* `esta_vazia()`: O(1) em qualquer caso.
* `len()`: O(1) em qualquer caso, pois soma dois `len` de pilha, cada um O(1).
* `repr()`: O(N)

---

## 4. Por que a estratégia das duas pilhas está correta?

A fila guarda duas pilhas:

* `entrada`: o item mais recente fica no topo.
* `saida`: o item mais antigo fica no topo.

### Invariante

A fila, da frente para o fim, é igual a: itens de `saida` do topo para a base, seguidos de itens de `entrada` da base para o topo.

* `enfileirar` empilha em `entrada`, ou seja, acrescenta ao fim da fila. O invariante se mantém.
* A transferência só ocorre quando `saida` está vazia.
    * Nesse caso a fila é apenas `entrada`, da base para o topo.
    * Desempilhar tudo de `entrada` para `saida` inverte a ordem: o item mais antigo, que estava na base de `entrada`, fica no topo de `saida`.
    * O invariante se mantém.
* Com o invariante, o topo de `saida` (depois da eventual transferência) é sempre a frente da fila.

### Por que transferir apenas quando a saída está vazia?

Se houvesse transferência com `saida` ainda ocupada, itens mais novos seriam empilhados por cima de itens mais antigos, e a ordem FIFO seria violada.

---

## 6. Por que desenfileirar pode custar O(N) em uma chamada isolada?

### Modelo de custo

Contamos chamadas a métodos de `PilhaEncadeada` (`push`, `pop`, `topo`, `esta_vazia`, `len`). Pela Seção 2, cada uma custa O(1), e a fila não faz nenhum outro trabalho além de um número constante de comparações por chamada.

### Passo 1: situação de pior caso

Faça N chamadas a `enfileirar` a partir da fila vazia. Então `entrada` tem N elementos e `saida` está vazia.

### Passo 2: o custo

A próxima chamada a `desenfileirar` encontra `saida` vazia e transfere os N elementos.

* Para cada elemento executa um `esta_vazia` (teste do laço), um `pop` em `entrada` e um `push` em `saida`: 3 chamadas por elemento.
* Somam-se a isso algumas chamadas fixas.
* O custo é da ordem de 3N, ou seja, Θ(N).

### Conclusão

No pior caso, uma chamada isolada de `desenfileirar` (e, pelo mesmo motivo, de `frente`) custa O(N). Não é possível garantir O(1) para toda chamada individual.

---

## 7. Por que desenfileirar é O(1) amortizada?

### Passo 1: custo de cada operação

Seja k o número de elementos transferidos durante uma chamada. Contando as chamadas a métodos da pilha:

* `enfileirar`: 1 chamada (`push`).
* `desenfileirar` ou `frente` com fila vazia: no máximo 2 chamadas (`esta_vazia` das duas pilhas), seguidas da exceção.
* `desenfileirar` ou `frente` sem transferência (k = 0): no máximo 4 chamadas.
    * Até 2 no `esta_vazia` da fila.
    * 1 no `esta_vazia` da saída.
    * 1 no `pop` ou `topo`.
* `desenfileirar` ou `frente` com transferência de k ≥ 1 elementos: 3k + 5 chamadas.
    * Até 2 no `esta_vazia` da fila.
    * 1 no `esta_vazia` da saída.
    * k + 1 testes do laço.
    * k chamadas a `pop` e k chamadas a `push`.
    * 1 no `pop` ou `topo` final.
* `esta_vazia` e `len` da fila: no máximo 2 chamadas.

Logo, toda operação da fila custa no máximo 5 + 3k chamadas, onde k é o número de elementos que ela transfere (k = 0 para operações que não transferem).

### Passo 2: lema (cada elemento é transferido no máximo uma vez)

Acompanhe um elemento x ao longo de sua vida na estrutura.

* (a) x entra na estrutura somente por `enfileirar`, que o empilha em `entrada`.
* (b) O único trecho de código que retira elementos de `entrada` é o laço de transferência, que imediatamente os empilha em `saida`.
* (c) Nenhum trecho de código move elementos de `saida` para `entrada`. A única escrita em `entrada` é o `push` de `enfileirar`, que só insere elementos novos.
* (d) O único modo de x sair de `saida` é o `pop` de `desenfileirar`, que o remove da fila definitivamente.

Portanto a trajetória de x é sempre: `entrada`, depois `saida`, depois fora da fila. Cada uma dessas passagens ocorre no máximo uma vez.

* Em particular, x é transferido no máximo uma vez.
* Ao longo de toda a vida, x participa de no máximo 4 movimentações de pilha: `push` em `entrada`, `pop` de `entrada`, `push` em `saida` e `pop` de `saida`.

### Passo 3: soma sobre uma sequência

Considere qualquer sequência de m operações da fila, começando da fila vazia, das quais e são `enfileirar` (logo e ≤ m). Seja kᵢ o número de elementos transferidos na i-ésima operação. Pelo Passo 1, o custo total T satisfaz:

T ≤ Σᵢ (5 + 3kᵢ) = 5m + 3 · Σᵢ kᵢ

### Passo 4: limitar o total de transferências

Σᵢ kᵢ é o número total de transferências na sequência.

* Pelo lema do Passo 2, cada elemento contribui com no máximo 1.
* Só podem ser transferidos elementos que foram enfileirados.
* Logo Σᵢ kᵢ ≤ e ≤ m.

### Passo 5: conclusão

Substituindo: T ≤ 5m + 3m = 8m.

O custo médio por operação na sequência é T/m ≤ 8, uma constante que não depende de N nem de m. Portanto cada operação da fila, e em particular `desenfileirar`, tem custo O(1) amortizado.
# Respostas - Aula Prática 6

## Análise de Complexidade: Fila com Duas Pilhas

A operação `desenfileirar()` pode apresentar custo O(N) em uma chamada isolada, mas sua complexidade amortizada é O(1). Isso ocorre devido à estratégia utilizada pela fila, que é composta por duas pilhas: `pilha_entrada` e `pilha_saida`.

### Pior caso: O(N)

Quando a `pilha_saida` está vazia e é realizada uma operação `desenfileirar()`, os elementos que estão na `pilha_entrada` precisam ser transferidos para a `pilha_saida`.

Supondo que existam N elementos na fila, essa transferência realiza N operações de `pop()` na `pilha_entrada` e N operações de `push()` na `pilha_saida`. Portanto, uma única chamada de `desenfileirar()` pode realizar uma quantidade de operações proporcional a N, resultando em custo O(N) no pior caso.

### Complexidade amortizada: O(1)

Apesar de uma chamada isolada poder custar O(N), essa transferência não acontece a cada operação de `desenfileirar()`. Ela só ocorre quando a `pilha_saida` está vazia.

Além disso, cada elemento da fila é transferido da `pilha_entrada` para a `pilha_saida` no máximo uma vez durante sua permanência na estrutura. Depois de transferido, o elemento permanece na `pilha_saida` até chegar à frente da fila e ser removido.

Assim, considerando uma sequência de várias operações, o custo da transferência é distribuído entre os elementos envolvidos. Para cada elemento, há uma quantidade constante de operações: ele é inserido na `pilha_entrada`, pode ser transferido uma vez para a `pilha_saida` e posteriormente é removido.

Dessa forma, para N elementos, o número total de operações de transferência é proporcional a N. Portanto, embora uma operação específica possa custar O(N), o custo médio por operação em uma sequência de operações é O(1).

Consequentemente, a complexidade amortizada de `desenfileirar()` é O(1), conforme a estratégia de duas pilhas utilizada na implementação.

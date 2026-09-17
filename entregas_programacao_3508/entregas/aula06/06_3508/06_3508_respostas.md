# Aula 6 - Análise de complexidade

A fila foi implementada usando duas pilhas: uma pilha de entrada e uma pilha de saída.

Quando um elemento é enfileirado, ele é colocado diretamente na pilha de entrada, então essa operação custa `O(1)`.

No momento de desenfileirar, se a pilha de saída já tiver elementos, basta fazer um `pop`, que também custa `O(1)`. Porém, se a pilha de saída estiver vazia, todos os elementos da pilha de entrada precisam ser transferidos para ela. Nesse caso, uma chamada isolada de `desenfileirar` pode custar `O(N)`.

Mesmo assim, a complexidade amortizada é `O(1)`. Isso acontece porque cada elemento é colocado uma vez na pilha de entrada e transferido no máximo uma vez para a pilha de saída. Depois da transferência, ele permanece na pilha de saída até ser removido. Portanto, o custo da transferência é distribuído entre várias operações da fila, fazendo com que o custo médio por operação seja constante.

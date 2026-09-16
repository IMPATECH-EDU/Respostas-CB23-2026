## analise de complexidade da fila

O método desenfileirar() pode ter custo O(N) em uma chamada isolada quando a pilha de saída está vazia. Nesse caso, é necessário transferir todos os elementos da pilha de entrada para a pilha de saída antes de remover o elemento da frente.

Apesar disso, desenfileirar() possui custo O(1) amortizado. Cada elemento é inserido uma vez na pilha de entrada, transferido no máximo uma vez para a pilha de saída e removido uma vez.

Assim, considerando uma sequência de várias operações, o custo total das transferências é proporcional ao número de elementos. Por isso, o custo médio de cada operação é O(1).
Considere uma fila implementada com duas pilhas: uma pilha de entrada e uma pilha de saída. Seja \(n\) a quantidade de elementos na pilha de entrada e \(m\) a quantidade de elementos na pilha de saída.

No **melhor caso**, quando \(m > 0\), a pilha de saída já contém o elemento que está na frente da fila. Dessa forma, `desenfileirar()` realiza apenas um `pop()` na pilha de saída, resultando em complexidade \(O(1)\).

No **pior caso**, quando \(m = 0\) e \(n > 0\), é necessário transferir todos os \(n\) elementos da pilha de entrada para a pilha de saída. Cada elemento é retirado da entrada com `pop()` e inserido na saída com `push()`. Portanto, são realizadas \(n\) transferências, além de uma remoção final na pilha de saída. Assim, uma chamada isolada de `desenfileirar()` pode ter complexidade \(O(n)\).

Apesar disso, a operação possui complexidade \(O(1)\) amortizada. Isso ocorre porque cada elemento é transferido da pilha de entrada para a pilha de saída no máximo uma vez durante toda a sua permanência na fila. Depois de transferido, ele permanece na pilha de saída até ser removido, sem precisar voltar para a pilha de entrada. Dessa forma, o custo \(O(n)\) da transferência é distribuído entre várias operações de `desenfileirar()`. Em uma sequência de operações, o número total de transferências é proporcional ao número de elementos processados, fazendo com que o custo médio por operação seja \(O(1)\).

Portanto, embora `desenfileirar()` possa custar \(O(N)\) em uma chamada específica, sua complexidade amortizada é \(O(1)\).


Ao chamar o método `desenfileirar` na classe `FilaEncadeada`, o pior caso isolado possui complexidade $O(N)$. Isso ocorre quando a pilha de saída está vazia e há $N$ elementos na pilha de entrada. Para retornar o elemento da frente da fila, o algoritmo precisa esvaziar a pilha de entrada, transferindo todos os $N$ elementos para a pilha de saída utilizando operações de `pop()` e `push()`. Como a estrutura de pilha inverte naturalmente a ordem dos dados, o primeiro elemento que havia entrado na fila acaba no topo da pilha de saída, pronto para ser removido com custo constante.

Apesar desse pico de processamento, a complexidade amortizada da operação (caso médio) permanece $O(1)$. Se realizarmos $N$ chamadas consecutivas do método `desenfileirar`, apenas a primeira fará a transferência completa de $N$ itens. As $N-1$ chamadas seguintes encontrarão a pilha de saída já abastecida, custando apenas $O(1)$ cada ao aplicar um simples `pop()` direto no topo. Matematicamente, o tempo total distribuído entre as operações resulta em uma constante:
$$
\dfrac{O(N) + (N - 1) \cdot O(1)}{N} = O(1)
$$

Essa eficiência torna-se ainda mais evidente ao analisarmos o ciclo de vida de um único elemento dentro da estrutura, argumentando sobre a quantidade de vezes que ele é transferido. Aplicando o método contábil de análise, onde alocamos "pontos" de custo fixo para cada dado, percebemos que um elemento sofrerá, no máximo absoluto, apenas 4 operações fundamentais durante toda a sua permanência na fila:
1.  Um `push()` para ser inserido na pilha de entrada.
2.  Um `pop()` para ser retirado da pilha de entrada durante a transferência.
3.  Um `push()` para ser inserido na pilha de saída na mesma transferência.
4.  Um `pop()` para ser finalmente desenfileirado e removido da estrutura.

Como nenhum elemento faz o caminho inverso (da saída de volta para a entrada), ele é transferido entre as pilhas apenas uma única vez em sua vida útil. Sendo 4 operações o limite rígido de manipulações por dado, o trabalho alocado para cada elemento é estritamente constante, comprovando que o custo temporal a longo prazo independe do tamanho total da fila, mantendo a complexidade amortizada em $O(1)$.
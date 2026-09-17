#Aula 06

Desenfileirar pode custar O(N), pois, para desenfileirar, é necessário que a pilha de saída tenha elementos. 
Caso ela não tiver, então será necessário passar todos os elementos (no máximo n elementos) que estão na pilha de entrada para a pilha de saída, custando, dessa forma, O(N), após isso, será possível então realizar um pop(), que é O(1),na pilha de saída para desenfileirar, tendo custo final O(N).
Se a pilha de saída já tiver elementos, então, para desenfileirar, basta fazer um pop(), que é O(1), na pilha de saída.

Cada elemento é transferido da pilha de entrada para a pilha de saída apenas uma vez (vale ressaltar que quando um item é acrescentado na fila ele entra na pilha de entrada) e não é transferido da pilha de saída para a pilha de entrada nenhuma vez. Então, as operações de troca da pilha de entrada para a pilha de saída somarão N no total no máximo. Logo, apesar de ser possível que uma operação de desenfileirar custe O(N), ao desenfileirar todos os elementos e dividir o custo entre todas essas operações, cada operação de desenfileiramento terá custo médio O(N)/N + O(1)(operação de pop), ou seja, custo O(1) em média amortizada.
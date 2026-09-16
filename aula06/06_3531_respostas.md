Nodo
Método(__init__())
Inicializa o nó com um valor e define o ponteiro para o próximo elemento como None. Complexidade de tempo O(1)

Pilha Encadeada 

Método(__init__())
Iniciali-za a pilha encadeada vazia, complexidade O(1)

Método(push())
Insere um item no topo da pilha, apontando o ponteira para o pŕoximo item, ou para None se for o primerio, soma 1 no "tamnho", complexidade O(1).

Método(pop())
Remove o item do topo da pilha e retorna o item removido, retorna "IndexError" se a pilha estiver vazia, subtrai 1 no tamanho da pilha, como o item esta no topo não é necessário percorrer a lista, logo a complexidade O(1).

Método(topo())
Retorna o item do topo da pilha sem remove-lo, levanta "IndexError" se a pilha estiver vazia, com o intem no topo da pilha não se faz necessário percorre-lá, então a complexidade é O(1).

Método(esta_vazia())
Retorna "True" se a lista estiver vazia ou "False" se não estiver, como apenas verifica se o primeiro ponteiro aponta para "None" ou não, a complexidade é O(1).

Método(__len__())
Retorna o "tamanho" da pilha, apenas verifica o valor de um número, logo a complexidade é O(1).

Método(__repr__())
Retorna uma representação em string da pilha, do topo para a base, primeiro percorre a pilha adicionando cada elemento a uma lista e uni as strings em apenas uma usando o .join, assim a passagem pela lista é O(n) e o ponto .join O(n), logo a complexidade final é O(n)



Fila Encadeada

Método(__init__())
Inicia a fila encadeada vazia formada de duas pilhas internas, complexidade O(1)

Método(enfileira())
Usa o método "push" da classe anterior, adicionando um intem no topo da pilha 1, complexidade O(1)

Método(desenfeleirar())
Remove e retorna o item no inico da fila, utiliza o método "pop" da classe anterior aplicando na segunda pilha da seguinte forma, quando a segunda pilha esta vazia se transfere todos os intens da pilha 1 para a 2, dessa forma o primeiro item a ser inserido fica no topo da segunda pilha assim basta usar o "pop", logo no caso onde a segunda pilha não esta vazia temos O(n) pois é necessário percorrer a primiera pilha inteira, por outro lado quando a segunda pilha não esta vazia basta usar o "pop" nela assim sendo O(1),ao final de ambos retorna o intem removido O(1), logo a complexidade é O(1) amortizada.

Método(frente())
Retorna o item da frente da fila encadeada sem remove-lo, novamente quando a segunda pilha não está vazia retorna o intem de seu topo O(1), quando está é necessário percorrer a pilha 1 inteira logo O(n), assim a complexidade é O(1) amortizada.

Método(esta_vazia())
Retorna a quantidade de itens na fila, verificando o tamanho de cada pilha com o método "__len__" da classe anterior(ambas operações O(1)), quando a soma é zero retorna "True" do contrário "False", logo a complexidade é O(1).

Método(__len__())
Retorna a quantidade de itens na fila, utiliza o método "__len__" da classe anterior para verificar a quantidade de itens de cada pilha(ambas operações O(1)), retorna a soma dos tamanhos, portanto a complexidade é O(1).

Método(__repr__())
Retorna uma representação em string da fila sem alterar o estado interno, adiciona os elemntos da fila em uma lista e uni os itens e uma unica string usando .join O(n), os itens são adicionados na lista da seguinte forma adiciona os elementos da pilha 2 na lista a percorrendo(ordem n), cria uma pilha temporaria e copia os itens da pilha 1 para a temporária(ordem n) para iverter a ordem e adiciona os itens na ordem correta na lista (ordem n) assim a soma desses passos é de ordem n, logo a complexidade é O(n)

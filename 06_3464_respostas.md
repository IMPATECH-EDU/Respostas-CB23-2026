# Análise de complexidade

## Pilha

A pilha possui complexidade excelente nos seus métodos por ser uma implementação dinâmica e simples. Os métodos de inserção e remoção (além daqueles que apenas visualizam variáveis internas) operam em __O(1)__, já que é necessário apenas mudar o encadeamento do elemento que já está no _head_ da pilha.

Seus métodos dependem de verificar o valor do nó atual ou se mover para outro nó e então receber o valor (como é o caso do  __rep__, no qual é preciso acessar todos os nós, e então opera em __O(n)__).

## Fila

A fila aqui implementada opera com base em duas pilhas sobre as quais elementos são movidos para realizar seus métodos.

* __enfileirar__: Esse método sempre insere o elemento na _"pilha esquerda"_, que é usada como identificador dos itens novos. Como apenas adiciona um elemento, é __O(1)__.
* __desenfileirar__: Esse método retorna o último item na "_pilha esquerda"_ se a _"pilha direita"_ não existir, ou então o primeiro elemento da _"pilha direita"_. A ideia é que os elementos mais acima da _"pilha direita"_ sempre estão mais no início da fila. Dessa forma, desenfileirá-los opera em, __O(1) amortecido__, já que no real pior caso (a _"pilha direita"_ está vazia, é preciso _n_ etapas para remover o elemento), mas no caso médio exige apenas _1_.
* __frente__: Segue o mesmo princípio do método _desenfileirar_. (Também opera em __O(1) amortecido__)
* __esta_vazia__: Retorna um boolean que indica se a fila está ou não vazia. É __O(1)__, pois é preciso apenas retornar uma variável interna.
*  __len__: Retorna o tamanho da fila __O(1)__.
*  __repr__: Retorna uma string padrão da fila. Esse método exige percorrer todos os elementos usando os métodos internos da fila, então ocorre em __O(n)__. Vale dizer que, para evitar usar estruturas de dados como listas (ou métodos built-in como o reverse de strings, muito semelhante a vetores), esse método muda os itens de lugar momentaneamente para acessá-los com o _pop_ da pilha.

## Testes

A unidade de testes foi implementada usando uma função geradora de sequências e testes inseridos manualmente.

* __generate_sequence__: Gera uma sequência com tamanho definido como entrada, sendo os elementos escolhidos aleatoriamente com base na entrada e uma escala de números proporcional ao tamanho da sequência.
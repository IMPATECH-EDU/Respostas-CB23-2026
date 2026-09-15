# Aula 7 — Respostas

## Questão 1 — DFS iterativa

A geração do labirinto foi implementada utilizando uma versão **iterativa da busca em profundidade (DFS)**, substituindo a chamada recursiva utilizada no código `maze_builder.py` fornecido pelo professor Emílio.

Na implementação original, a própria recursão é responsável por manter o estado das salas que ainda precisam ser exploradas. Na versão iterativa, essa função é realizada principuamente por uma **pilha**.

A posição inicial `(0, 0)` é colocada na pilha e marcada como visitada. Enquanto houver posições na pilha, a posição no topo é analisada. Seus quatro possíveis vizinhos são embaralhados e, caso exista um vizinho que ainda não foi visitado, a parede entre as duas salas é removida, a nova sala é aberta e sua posição é colocada no topo da pilha.

Quando a posição atual não possui mais vizinhos não visitados, ela é retirada da pilha. Esse procedimento representa o **backtracking** da DFS.

Portanto, a pilha desempenha na implementação iterativa o papel que seria desempenhado pela pilha de chamadas da função recursiva.

A implementação mantém a mesma ideia do `maze_builder.py`: o labirinto é construído sobre uma matriz expandida, na qual as posições de coordenadas ímpares representam as salas da grade lógica e as posições entre elas representam as paredes que podem ser removidas.


## Questão 2 — Encontrar o caminho até o queijo

Para encontrar o caminho partindo da posição `(1, 1)` até o queijo, foi implementada novamente uma **busca em profundidade iterativa (DFS)**.

A busca começa na posição `(1, 1)` e utiliza uma pilha para armazenar as posições que ainda serão exploradas.

Além da pilha, são utilizadas duas estruturas auxiliares:

- `visitado`: indica quais posições já foram visitadas;
- `anterior`: guarda a posição anterior utilizada para chegar a cada posição.

Quando a busca encontra o queijo, a matriz `anterior` permite reconstruir o caminho. Para isso, começamos na posição do queijo e seguimos os predecessores até chegar à posição inicial `(1, 1)`. Como esse percurso é obtido do final para o início, a lista é invertida antes de ser retornada.

A função `exibir_labirinto_e_caminho` recebe esse caminho e marca suas posições com `.`. O queijo continua sendo representado por `*` e as paredes por `W`.


## Escolha entre busca em profundidade e busca em largura

A estratégia escolhida para encontrar o caminho foi a **busca em profundidade (DFS)**.

A principal razão para essa escolha é que o próprio labirinto utilizado na atividade é gerado por uma busca em profundidade com retrocesso. Além disso, o labirinto gerado pelo `maze_builder.py` é um **labirinto perfeito**, isto é, existe exatamente um caminho entre quaisquer duas salas.

Assim, entre a posição inicial `(1, 1)` e o queijo existe um único caminho possível. A DFS consegue encontrar esse caminho sem que seja necessário comparar diferentes caminhos para determinar qual é o menor.

A busca em largura (BFS) também poderia ser utilizada para resolver o labirinto. Em um grafo não ponderado, a BFS possui a vantagem de encontrar o caminho com menor número de passos. Porém, essa propriedade não é necessária neste caso, pois o labirinto perfeito possui apenas um caminho entre a origem e o queijo.

Por esse motivo, a DFS foi considerada uma escolha adequada para esta atividade. Ela também mantém uma relação direta com o algoritmo utilizado na geração do próprio labirinto.


## Complexidade

Se `V` representa o número de posições que podem ser exploradas no labirinto, cada posição é visitada no máximo uma vez durante a busca.

Portanto, a busca possui complexidade de tempo:

**O(V)**

A matriz `visitado`, a matriz `anterior` e a pilha podem armazenar até `V` posições. Dessa forma, a complexidade de espaço é:

**O(V)**

A reconstrução do caminho também percorre somente as posições que fazem parte do caminho encontrado e, no pior caso, pode percorrer todas as posições visitadas. Portanto, continua sendo **O(V)**.
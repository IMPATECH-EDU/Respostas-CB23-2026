# Atividade 7 — Respostas

## Questão 1

A versão original de `maze_builder.py` utiliza uma busca em profundidade (`dfs`) recursiva. Para torná-la iterativa, a pilha implícita das chamadas recursivas é substituída por uma pilha explícita armazenada em uma lista.

A posição atual é mantida no topo da pilha. Enquanto existir uma sala vizinha ainda não visitada, a parede entre as duas salas é removida, a nova sala é marcada como visitada e ela é colocada no topo da pilha. Quando a sala atual não possui vizinhos não visitados, ela é retirada da pilha, realizando o retrocesso (*backtracking*).

Essa implementação preserva a ideia da DFS original, mas não utiliza recursão. Cada uma das `m*n` salas é visitada uma vez e cada sala possui no máximo quatro vizinhos. Assim, o tempo de geração é `O(m*n)`. A pilha explícita pode, no pior caso, conter `O(m*n)` salas.

## Questão 2

Para encontrar o queijo, foi utilizada uma busca em largura (BFS), partindo da posição `(1, 1)`.

A BFS mantém uma fila de posições ainda não exploradas. Para cada posição retirada da fila, são examinados os quatro vizinhos cardeais. Apenas posições livres do labirinto ou a posição do queijo são adicionadas à busca. Um dicionário `parent` registra de qual posição cada posição foi alcançada. Quando o queijo é encontrado, esse registro permite reconstruir o caminho, voltando da posição do queijo até `(1, 1)` e invertendo a sequência obtida.

A escolha da BFS se deve ao fato de que ela encontra um caminho com o menor número de movimentos quando todas as movimentações têm o mesmo custo. No labirinto gerado pelo código, existe exatamente um caminho entre duas salas, portanto também existe um único caminho entre `(1, 1)` e o queijo. Assim, nesse caso específico, DFS e BFS encontrariam o mesmo caminho; a BFS foi escolhida por fornecer diretamente a garantia de menor número de movimentos.

A função `show_maze` exibe o labirinto original e pode receber o caminho encontrado para destacá-lo com `*`. A posição inicial é marcada com `S` e o queijo continua identificado pelo símbolo `.`.

A busca percorre cada posição da matriz no máximo uma vez, portanto sua complexidade de tempo é `O(R*C)`, onde `R` e `C` são as dimensões da matriz do labirinto. O espaço utilizado pela fila, pelos predecessores e pelo conjunto implícito de posições visitadas também é `O(R*C)`.

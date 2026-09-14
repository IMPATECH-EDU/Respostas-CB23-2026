Para implementar a solução, escolhi utilizar a Busca em Profundidade (DFS) com uma abordagem iterativa baseada em pilha. Abaixo explico os motivos dessa escolha em relação à Busca em Largura (BFS):

* A natureza do labirinto: O enunciado diz que este é um labirinto "perfeito", pelo que existe exatamente um único caminho válido entre a origem $(1,1)$ e o queijo, sem a existência de ciclos.

* Recuperação natural do caminho: Na DFS, quando alcançamos o objetivo (o queijo), a própria pilha de execução já representa o caminho exato da origem até o destino. Se tivéssemos usado BFS, a fila (queue) testaria múltiplos caminhos simultaneamente; ao encontrar o queijo, teríamos que usar uma estrutura de dados adicional (como um dicionário pai_no = no_anterior) para reconstruir o caminho de trás para frente. A DFS poupa esse trabalho e essa memória.


Em síntese, o algoritmo anda sempre em frente nas bifurcações, ou seja, se entra em um beco sem saída, ele marca o território como visitado, retira a posição da pilha e tenta a próxima ramificação. Quando acha o queijo, o conteúdo da pilha é a resposta.
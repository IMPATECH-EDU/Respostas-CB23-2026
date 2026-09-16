Podemos simplificar o problema a: estamos em um ponto inicial (nesse caso o (1,1)) e queremos partir a um determinado ponto final, que é aquele em que o queijo se encontra. 
Vamos sair desse estado inicial e percorrer os próximos pontos até chegar ao estado final (queijo) e queremos fazer isso com o menor número de passos possíveis. Temos 2 opções: busca em profundidade (em que usaríamos, tipicamente, uma pilha, como visto em sala) ou busca em largura (uma fila, como visto em sala). 
Sabemos que, se fosse utilizado uma pilha, o algoritmo iria chegar ao queijo através de algum caminho (se existir essa possibilidade). Acontece que esse caminho pode entrar por alguns "becos" que não garantam ser o menor trajeto possível. Desse modo, acaba não sendo satisfeita a ideia de encontrar o caminho mais curto até o queijo. 
Entretanto, utilizando uma fila, o algoritmo vai percorrendo "níveis" e, assim que chegar no primeiro caminho que chega ao queijo (que será o mais curto), ele vai retornar aquele caminho:
 if maze[cx][cy] == cheese: 
            return onde_estou  
Isso é exatamente o que queremos. 
Portanto, foi implementado um código que realiza a busca em largura para encontrar o queijo através do menor caminho possível até ele. 
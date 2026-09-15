* Questão 2 — justificativa da estratégia de busca
    * A busca implementada em `P07_3528_labirinto.py` para achar o caminho de `(1, 1)` até o queijo é a busca em largura (BFS), iterativa com fronteira em fila FIFO, na função `solve_maze_bfs`.
    * A busca em profundidade iterativa (`solve_maze_dfs`) também está no script, mas apenas como termo de comparação.

---

* Modelagem do labirinto como grafo
    * Vértices: todas as células da matriz `(2m+1) x (2n+1)` cujo valor é diferente de `wall`, isto é, as salas e as paredes derrubadas.
    * Arestas: pares de vértices adjacentes na vertical ou na horizontal.
    * Número de vértices: `mn + (mn - 1) = 2mn - 1`.
    * Buscar sobre a matriz expandida, e não sobre a grade lógica de salas, faz o caminho devolvido já sair contíguo, pronto para ser desenhado sem reconstruir as células intermediárias.

---

* O labirinto gerado é uma árvore, e isso muda a pergunta
    * O gerador só derruba a parede entre duas salas quando a sala vizinha ainda não foi visitada; logo há exatamente `mn - 1` paredes derrubadas e toda sala é alcançável.
    * Um grafo conexo com `mn` vértices e `mn - 1` arestas é uma árvore.
    * Numa árvore há um único caminho simples entre dois vértices: dois caminhos simples distintos entre os mesmos extremos formariam um ciclo, contradizendo a aciclicidade.
    * Consequência: qualquer busca completa que não repita vértices devolve exatamente o mesmo caminho. Não existe caminho melhor a ser achado, então a escolha entre profundidade e largura não pode ser justificada pelo resultado — tem de ser justificada pelo custo da busca, pelas garantias que ela oferece e pela robustez a mudanças de premissa.

---

* Por que a busca em largura
    * Garantia de caminho mínimo que não depende do labirinto
        * A fila FIFO faz as células serem expandidas em ordem não decrescente de distância à origem: a fronteira contém sempre vértices de no máximo dois níveis consecutivos, e por indução no nível, quando um vértice sai da fila sua distância é a mínima. O primeiro caminho encontrado até o queijo é, portanto, de comprimento mínimo.
        * Num labirinto perfeito essa garantia é gratuita, porque o caminho é único. Ela deixa de ser gratuita assim que o labirinto deixa de ser árvore: paredes extras derrubadas como atalhos, mais de um queijo, salas com várias entradas.
        * Nesses casos a busca em profundidade continua devolvendo um caminho, que pode ser arbitrariamente mais longo que o mínimo, enquanto a busca em largura continua devolvendo o mínimo sem nenhuma alteração de código.
    * Custo de exploração limitado pela distância ao objetivo
        * A BFS só expande vértices a distância menor ou igual à do queijo, ou seja, uma bola centrada na origem: o esforço é crescente na distância do objetivo e termina cedo quando o queijo está perto.
        * A DFS mergulha num ramo até o fim antes de tentar outro e pode varrer o labirinto inteiro mesmo com o queijo a poucos passos. No pior caso medido, num labirinto `25 x 25`, ela expandiu 1248 das 1249 células para alcançar um queijo que a BFS alcançou com 32 expansões.
    * Iteratividade natural
        * A fronteira é uma fila explícita (`collections.deque`, com `popleft` em tempo constante), sem recursão e portanto sem risco de `RecursionError` ou necessidade de mexer em `sys.setrecursionlimit`.
    * O argumento clássico de memória contra a BFS não se aplica aqui
        * Ele vale em grafos com fator de ramificação alto. Num labirinto perfeito o grafo é uma árvore de grau máximo 4, dominada por corredores de grau 2, e a fronteira mede-se em unidades.
        * O termo dominante de memória não é a fronteira, e sim o dicionário `parent`, que serve ao mesmo tempo de conjunto de visitados e de árvore de busca, com `Θ(mn)` entradas nas duas estratégias.

---

* Comparação empírica, em 200 labirintos `25 x 25` com 625 salas e 1249 células transitáveis
    * Caminhos devolvidos: idênticos nas 200 execuções, como previsto pela unicidade.
    * Células expandidas: 624 em média pela BFS, com máximo de 1215; 646 em média pela DFS, com máximo de 1249, o labirinto inteiro.
    * Fronteira máxima: 5,1 em média pela BFS, com máximo de 13; 13,0 em média pela DFS, com máximo de 26.
    * Leitura honesta dos números: na média as duas são equivalentes, porque o queijo é sorteado uniformemente e ambas acabam varrendo cerca de metade do labirinto. A diferença está na garantia — o esforço da BFS é função crescente da distância do objetivo, o da DFS é praticamente independente dela.

---

* Em que cenário a busca em profundidade seria preferível
    * Memória sob restrição severa: numa árvore a DFS dispensa o dicionário de visitados, bastando a pilha do caminho atual e a regra de não voltar para o pai, o que derruba a memória de `Θ(mn)` para `Θ(profundidade)`. O preço é abrir mão da minimalidade caso o labirinto não seja perfeito.
    * Objetivos tipicamente profundos: se o queijo ficasse sempre longe da origem por construção, a DFS chegaria antes na média.
    * Grafos com fator de ramificação alto, em que a fronteira da BFS se torna proibitiva.
    * Nenhuma das três condições vale no enunciado: as grades são pequenas, o queijo é sorteado uniformemente e o custo de memória é o mesmo nas duas implementações.

---

* Complexidade, com `|V| = 2mn - 1` e `|E| = |V| - 1`
    * Tempo: `O(|V| + |E|) = Θ(mn)` nas duas buscas. Cada célula entra na fronteira no máximo uma vez, garantido pelo teste `neighbor not in parent`, e cada aresta é examinada no máximo duas vezes.
    * Memória: `Θ(mn)` nas duas, dominada pelo dicionário `parent`.
    * Operações de fronteira em tempo constante: `popleft` e `append` na BFS, `pop` e `append` na DFS.
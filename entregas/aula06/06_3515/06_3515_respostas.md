# Aula 6 — Análise de complexidade

## Questão 1 — Pilha Encadeada

A classe `PilhaEncadeada` utiliza uma lista simplesmente encadeada construída manualmente.

Cada nó possui:

- `valor`
- `proximo`

A pilha mantém:

- Uma referência para o nó do topo.
- Um contador de elementos.

### Complexidades

| Operação | Complexidade |
| `push(item)` | O(1) |
| `pop()` | O(1) |
| `topo()` | O(1) |
| `esta_vazia()` | O(1) |
| `len()` | O(1) |
| `repr()` | O(N) |

A operação `push` é O(1) porque cria um novo nó e coloca sua referência no topo.

A operação `pop` é O(1) porque remove diretamente o nó do topo.

A operação `topo` é O(1) porque consulta diretamente o valor do nó do topo.

A operação `esta_vazia` é O(1) porque verifica o contador de elementos.

A operação `len` é O(1) porque o tamanho é mantido em um contador atualizado durante as inserções e remoções.

A operação `repr` é O(N) porque precisa percorrer todos os nós para construir a representação textual.


## Questão 2 — FilaEncadeada

A classe `FilaEncadeada` utiliza duas instâncias de `PilhaEncadeada`:

- Pilha de entrada.
- Pilha de saída.

A fila utiliza composição, pois possui objetos da classe `PilhaEncadeada` internamente.

A fila não acessa diretamente os atributos internos da pilha. Ela utiliza somente os métodos públicos:

- `push`
- `pop`
- `topo`
- `esta_vazia`
- `len`

### Complexidades

| Operação | Complexidade |
|---|---|
| `enfileirar(item)` | O(1) |
| `desenfileirar()` | O(1) amortizada |
| `frente()` | O(1) amortizada |
| `esta_vazia()` | O(1) |
| `len()` | O(1) |
| `repr()` | O(N) |

### Por que `enfileirar` é O(1)?

O novo item é inserido diretamente na pilha de entrada utilizando `push`.

Como `push` é O(1), `enfileirar` também é O(1).

### Por que `desenfileirar` pode ser O(N) em uma chamada?

Quando a pilha de saída está vazia, todos os elementos da pilha de entrada são transferidos para a pilha de saída.

Se houver N elementos, essa transferência exige N operações de remoção e N operações de inserção.

Portanto, uma chamada isolada de `desenfileirar` pode custar O(N).

### Por que `desenfileirar` é O(1) amortizada?

Cada elemento é transferido da pilha de entrada para a pilha de saída no máximo uma vez durante sua vida na fila.

Depois que o elemento é transferido para a pilha de saída, ele pode ser removido diretamente usando `pop`, que custa O(1).

Assim, considerando uma sequência de várias operações:

- Cada elemento é inserido uma vez na pilha de entrada.
- Cada elemento é transferido no máximo uma vez para a pilha de saída.
- Cada elemento é removido uma vez da pilha de saída.

O custo total de todas as transferências é proporcional ao número de elementos.

Se forem realizadas N operações sobre N elementos, o custo total será O(N). Dividindo esse custo pelas N operações, temos custo médio amortizado O(1) por operação.

Portanto, `desenfileirar` pode custar O(N) em uma chamada isolada, mas possui complexidade O(1) amortizada.

### Por que `frente` também é O(1) amortizada?

A operação `frente` utiliza a mesma estratégia de transferência das duas pilhas.

Se a pilha de saída estiver vazia, pode ocorrer uma transferência O(N). Caso contrário, basta consultar o topo da pilha de saída, que custa O(1).

Por isso, `frente` também é O(1) amortizada.

### Por que `repr` é O(N)?

A representação precisa consultar todos os elementos da fila para mostrar os valores da frente para o fim.

Por isso, sua complexidade é O(N).
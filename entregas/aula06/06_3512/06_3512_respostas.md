# Aula 6 — Pilha e Fila Encadeadas

## 1. TAD e estrutura de dados

Um **Tipo Abstrato de Dados (TAD)** descreve o comportamento que uma estrutura deve oferecer, sem determinar como ela será implementada internamente.

Por exemplo, uma pilha é um TAD que permite operações como inserir um elemento no topo, consultar o topo e remover o elemento do topo. A regra principal é **LIFO** (*Last In, First Out*).

A **estrutura de dados**, por outro lado, é a forma concreta utilizada para implementar esse comportamento.

Neste exercício, a `PilhaEncadeada` é uma implementação do TAD pilha utilizando uma lista simplesmente encadeada. Cada nó possui um valor e uma referência para o próximo nó.

A fila também é um TAD. Sua regra é **FIFO** (*First In, First Out*). Nesta atividade, ela é implementada por composição de duas instâncias de `PilhaEncadeada`.

---

## 2. PilhaEncadeada

A classe `PilhaEncadeada` mantém duas informações principais:

- `_topo`: referência para o nó que está no topo;
- `_tamanho`: quantidade de elementos existentes na pilha.

Cada nó da estrutura é representado pela classe `_No`, que possui:

- `valor`: elemento armazenado;
- `proximo`: referência para o próximo nó.

A inserção é feita criando um novo nó e fazendo com que ele aponte para o antigo topo.

A remoção retira o nó do topo e atualiza a referência `_topo`.

### Complexidade

| Operação | Complexidade |
|---|---|
| `push` | O(1) |
| `pop` | O(1) |
| `topo` | O(1) |
| `esta_vazia` | O(1) |
| `len` | O(1) |
| `repr` | O(N) |

O contador `_tamanho` permite obter o número de elementos em O(1), sem precisar percorrer a estrutura.

A representação (`repr`) precisa percorrer os nós para mostrar todos os elementos, portanto possui custo O(N).

---

## 3. FilaEncadeada por composição

A `FilaEncadeada` utiliza duas pilhas:

- `_entrada`: recebe os novos elementos;
- `_saida`: fornece os elementos que serão removidos.

Quando um elemento é inserido, ele é colocado na pilha de entrada.

Quando é necessário consultar ou remover o primeiro elemento da fila, verificamos se a pilha de saída está vazia. Caso esteja, todos os elementos da pilha de entrada são transferidos para a pilha de saída.

Por exemplo, depois de inserir:

```text
entrada:

topo
  3
  2
  1

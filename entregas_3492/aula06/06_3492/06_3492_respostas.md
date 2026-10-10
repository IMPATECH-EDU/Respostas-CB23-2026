# Análise de complexidade

## 1. Pilha encadeada (`PilhaEncadeada`)

Todas as operações atuam apenas sobre o nó `head`, sem percorrer a lista, por isso têm custo constante:

| Operação | Complexidade | Justificativa |
|---|---|---|
| `push` | O(1) | Cria um nó e o insere antes do `head` atual. |
| `pop` | O(1) | Remove o `head` e reatribui o ponteiro para o próximo nó. |
| `topo` | O(1) | Apenas lê `head.valor`. |
| `esta_vazia` | O(1) | Compara `tamanho` com zero. |
| `__len__` | O(1) | Retorna o atributo `tamanho`, mantido incrementalmente a cada `push`/`pop`. |

(`__repr__` é O(n), pois percorre todos os nós para montar a string — mas não é uma operação estrutural da pilha.)

## 2. Fila encadeada (`FilaEncadeada`)

A fila é implementada com duas pilhas: `_entrada` recebe os itens ao enfileirar, e `_saida` é de onde eles saem ao desenfileirar. Quando `_saida` está vazia e uma remoção é solicitada, **todo** o conteúdo de `_entrada` é transferido para `_saida` — um `pop` de `_entrada` seguido de um `push` em `_saida`, para cada elemento. Essa transferência inverte a ordem, recolocando o elemento mais antigo no topo de `_saida`, o que preserva o comportamento FIFO da fila.

| Operação | Pior caso (uma chamada) | Amortizado (sequência de operações) |
|---|---|---|
| `enfileirar` | O(1) | O(1) |
| `desenfileirar` | O(n) | **O(1)** |
| `frente` | O(n) | O(1) |
| `esta_vazia` / `__len__` | O(1) | O(1) |

`enfileirar` é sempre O(1): um único `push` em `_entrada`. Já `desenfileirar` e `frente` — que compartilham a mesma lógica de transferência — custam O(n) no pior caso, quando `_saida` está vazia e é preciso mover os n elementos de `_entrada` antes de acessar o elemento desejado. É esse pior caso que a análise a seguir justifica ser, ao longo do tempo, O(1).

## 3. Justificativa da complexidade amortizada de `desenfileirar`

### 3.1 O problema

Isoladamente, uma chamada a `desenfileirar` pode custar O(n) — por exemplo, a primeira chamada após uma sequência de `enfileirar`s. Se esse custo se repetisse a cada chamada, a fila seria tão custosa quanto uma implementação ingênua com deslocamento de posições. O que evita isso é que a transferência **nunca repete trabalho sobre o mesmo elemento**: uma vez movido para `_saida`, um elemento nunca retorna para `_entrada` nem é transferido de novo.

### 3.2 Análise por agregação (aggregate method)

Acompanhe o ciclo de vida de um elemento, do `enfileirar` que o insere até o `desenfileirar` que o remove definitivamente. Ao longo desse ciclo, ele participa de **no máximo 4 operações de pilha, todas O(1)**:

1. Um `push` em `_entrada`, no momento do `enfileirar`.
2. Um `pop` de `_entrada`, durante alguma transferência futura.
3. Um `push` em `_saida`, na mesma transferência (sempre pareado com o item 2).
4. Um `pop` de `_saida`, quando o elemento é finalmente retornado por um `desenfileirar`.

Os itens 2 e 3 ocorrem **no máximo uma vez na vida do elemento**: depois de transferido para `_saida`, ele só sai dali por um `pop` definitivo — nunca volta para `_entrada` para ser transferido de novo.

Logo, para qualquer sequência de *m* operações sobre a fila, o número de elementos que já passaram por ela é, no máximo, *m*, e o número total de operações internas de pilha é, no máximo, 4*m*:

- custo total ≤ 4m = O(m)
- custo amortizado por operação = custo total / m ≤ 4 = **O(1)**

Esse limite vale para **qualquer** sequência de chamadas, não apenas para um caso particular favorável — é justamente essa garantia (sobre qualquer sequência, e não sobre uma distribuição estatística de entradas) que caracteriza uma análise amortizada e a distingue de uma análise de caso médio.

### 3.3 Exemplo numérico

Enfileirando `A`, `B`, `C` e desenfileirando três vezes em seguida:

| Chamada | O que acontece internamente | Custo |
|---|---|---|
| `enfileirar(A)` | 1 `push` em `_entrada` | 1 |
| `enfileirar(B)` | 1 `push` em `_entrada` | 1 |
| `enfileirar(C)` | 1 `push` em `_entrada` | 1 |
| `desenfileirar()` → `A` | `_saida` vazia: transfere 3 elementos (3 `pop` + 3 `push`) + 1 `pop` final | 7 |
| `desenfileirar()` → `B` | `_saida` já tem itens: só 1 `pop` | 1 |
| `desenfileirar()` → `C` | `_saida` já tem itens: só 1 `pop` | 1 |

Custo total: 12 para 6 operações — média de 2 por operação, mesmo com uma chamada isolada custando 7. Quanto mais elementos forem enfileirados antes da primeira remoção, maior o pico daquela transferência, mas ela ocorre uma única vez por grupo de elementos: cada elemento, individualmente, continua custando O(1) em média ao longo de sua permanência na fila.

### 3.4 Confirmação pelo método da contabilidade

Como verificação alternativa: atribua um custo amortizado fixo a cada operação e confirme que o saldo de "créditos" nunca fica negativo.

- **`enfileirar` custa 3:** 1 crédito é gasto no `push` em `_entrada`; os outros 2 ficam depositados junto com o elemento, reservados para pagar seu futuro `pop` de `_entrada` e `push` em `_saida`.
- **`desenfileirar` custa 1:** paga apenas o `pop` final em `_saida`. Quando uma transferência é disparada, o custo de mover cada elemento é pago com o crédito que *aquele elemento* já trazia consigo — não com o crédito da chamada atual.

Como todo elemento carrega crédito suficiente para bancar sua própria transferência, o saldo nunca fica negativo — o que confirma 3 e 1 como cotas amortizadas válidas, ambas O(1).

## 4. Conclusão

- **Pior caso de uma chamada isolada a `desenfileirar`:** O(n), quando ela dispara a transferência completa de `_entrada` para `_saida`.
- **Custo amortizado ao longo de qualquer sequência de operações:** **O(1)**, porque cada elemento é transferido entre as duas pilhas no máximo uma vez durante toda a sua permanência na fila — o custo da transferência "cara" é diluído entre o `enfileirar` que trouxe o elemento e o `desenfileirar` que eventualmente o devolve.

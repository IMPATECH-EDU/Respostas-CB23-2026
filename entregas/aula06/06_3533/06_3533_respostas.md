# Análise de Complexidade: Fila com Duas Pilhas

## Análise da Complexidade Amortizada do `desenfileirar()`

Embora uma chamada isolada do método `desenfileirar()` possa custar **$O(N)$** no pior caso (quando a pilha de saída está vazia e a pilha de entrada contém $N$ elementos que precisam ser transferidos), a complexidade amortizada por operação é **$O(1)$**.

### Demonstração pelo Método do Contabilista (Análise Amortizada)

Para provar o custo médio por operação, analisamos o ciclo de vida de qualquer elemento inserido na estrutura:

1. **`enfileirar(item)`**: O elemento é inserido na pilha `_entrada` via `push`. 
   * Custo: **$1$ operação de push**.
2. **Transferência**: Em algum momento futuro, o elemento é removido da `_entrada` via `pop` e inserido na `_saida` via `push`.
   * Custo: **$1$ operação de pop + $1$ operação de push**.
3. **`desenfileirar()`**: O elemento é removido do topo da `_saida` via `pop`.
   * Custo: **$1$ operação de pop**.

### Conclusão

Ao longo de toda a sua permanência na fila, cada elemento passa por exatamente **4 operações primitivas de pilha** ($O(1)$ cada). 

Se realizarmos uma sequência de $N$ inserções seguidas por $N$ remoções, o número total de operações internas em pilhas será de $4N$. Ao dividir o custo total pelo número de operações $N$:

$$\text{Custo Amortizado} = \frac{O(N)}{N} = O(1)$$

Portanto, o custo $O(N)$ da transferência é distribuído ("amortizado") ao longo de múltiplas chamadas rápidas que custam $O(1)$, garantindo eficiência média constante.
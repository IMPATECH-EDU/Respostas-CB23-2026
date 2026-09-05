A análise amortizada avalia o custo médio de uma sequência de operações dividindo o custo total pelo número de operações.

Para ilustrar melhor esse problema, é útil pensar na teoria do crédito bancário: Suponha que cada elementos, antes de ser incorporado ao nosso problema, i.e., ser adicionado à pilha de entrada, possui uma determinada quantidade de crédito. Conforme operações vão sendo feitas com esse item ao longo do ćodigo, o seu crédito subtrai em uma unidade.

Seguindo essa lógica, não é difícil mostrar que cada elementos precisa ter exatamente 4 unidades de crédito, que serão gastos nas respectivas operações:
1. Enfileirado (Push na Pilha de Entrada): 
2. Transferido de entrada (Pop da Pilha de Entrada): 
3. Transferido de saída (Push na Pilha de Saída): 
4. Desenfileirado final (Pop da Pilha de Saída):

Portanto, se pensarmos na análise de complexidade do caso médio (não no caso individual), chegaremos que a complexidade para desenfileirar $N$ elementos será de $4N$. Portanto, temos que a respectiva complexidade vale:
$$
\text{Custo Amortizado por Operação} = \frac{\text{Custo Total para } N \text{ elementos}}{\text{Número de Operações}} = \frac{O(N)}{N} = O(1)
$$

É importante que façamos essa análise no caso médio, pois, se virmos o caso individual, veremos que o custo para desenfileirar um único item pode chegar a $\Omega(N)$.
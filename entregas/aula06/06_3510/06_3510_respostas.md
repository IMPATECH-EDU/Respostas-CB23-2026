`desenfileirar()` e `frente()` funcionam da seguinte forma:
- Verifica se a pilha de saída está vazia.
    - Caso esteja, o programa precisa passar todos os itens da pilha de entrada para a pilha de saída, em ordem reversa, para que o primeiro item inserido na pilha de entrada (i.e., o item do fundo da pilha), seja o primeiro item da ordem de saída (o item do topo da pilha de saída).
    - Caso não esteja, simplesmente executa a função em questão.

Dessa forma, em uma chamada isolada ou na primeira chamada de uma execução do programa, essas funções custam O(n), pois a pilha de saída ainda está vazia. Porém, em ocasiões onde as funções são chamadas várias vezes, elas custam O(1), pois o processo de transferência dos itens de uma pilha para outra não precisa ser feito novamente, até que a pilha de saída esteja vazia.

Caso um item seja enfileirado depois que algum outro tenha sido desenfileirado, ele permanecerá na pilha de entrada até que a pilha de saída esteja vazia, pois ele não é necessário para nenhuma das operações, e transferí-lo para a pilha de saída prematuramente iria interferir na ordem e inutilizar todo o processo.

Note também que os itens só são transferidos de uma pilha para outra uma vez ao longo de sua vida, visto que todas as funções fora `desenfileirar()`e `frente()` não precisam dessa transferência, e funcionam corretamente mesmo que as duas pilhas contêm elementos. 
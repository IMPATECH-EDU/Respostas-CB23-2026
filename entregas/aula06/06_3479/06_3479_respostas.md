Por que desenfileirar pode custar O(N) em uma chamada isolada e ainda assim ser O(1) amortizada (caso médio)? 
Vejamos o que faz o método desenfileirar(): 
#   def desenfileirar(self): 
    '''Método que remove e retorna o item da frente da FILA; levanta IndexError se estiver vazia
    Complexidade: O(1) amortizada (caso médio)''' 
    # basicamente, vamos repassar os elementos de uma pilha para outra e tirar o elemento do topo da segunda pilha 
    if self._entrada.esta_vazia() is True and self._saida.esta_vazia() is True: 
      raise IndexError('a fila está vazia') 
    if self._saida.esta_vazia() is True: 
      while self._entrada.esta_vazia() is not True:
        self._saida.push(self._entrada.pop()) 
    return self._saida.pop()  
No pior caso, podemos imaginar uma pilha da seguinte forma: [n, n-1. n-2, ..., 1]. Desejamos retirar o item da frente da fila correspondente, ou seja, desejamos retirar o número 1. Para isso, vamos jogar todos esses valores na segunda pilha, que é a nossa self._saida. Então, o while vai rodar n vezes. Nesse caso, temos uma complexidade O(N). 
Mas, para que esse caso aconteça, temos que o self._saida deve estar vazio desde o princípio. Então, depois que o self._saida está cheio, tudo se segue com complexidade O(1), já que estaremos apenas executando um pop, que é de complexidade O(1) também. 
Logo, temos que, feito caso O(N), tudo será O(1) em seguida. Portanto, estamos em um caso O(1) amortizado.  
Para melhor visualizarmos, podemos pensar no ciclo de vida do elemento: 
(I) ele entra na self._entrada com um push (equivalente ao enfileirar), sai com um pop (equivalente a desenfileirar), entra em self._saida com um push e sai de volta com outro pop. São feitas, então, 4 operações, em que as duas primeiras são "compensadas" após as 2 últimas. 
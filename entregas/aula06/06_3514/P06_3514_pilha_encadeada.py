import time
class No:
 def __init__(self, dado):
      self.dado = dado
      self.proximo = None

class ListaEncadeada:
 """
 'Método' utilizado para definir parâmetros inicias, nele se define incialamente a cabeca, que atua como ponteiro principal, que depois
 adicionamos instâncias da classe auxiliar NO, possui O(n)=1, pois apenas atribui valores
 """
 def __init__(self):
    self.cabeca = None
    self._len = 0

 """
 Método utilizado para verificação se a lista está vazia ou não, consiste em tomar a cabeca, se houver algum elemento
 deve retornar None pois no caso cabeca seria um NO, possui O(n)=1, visto que realiza apenas uma comparação
 """

 def esta_vazia(self):
    return self.cabeca is None

 """
 'Método' para contagem de elementos na lista, é atualizado a cada método de adição/remoção chamado, em vista disso, possui
 O(n)=1, visto que o valor sempre está armazenado corretamente
 """

 def __len__(self):
     return self._len
 
 """
 'Método' de representação chamado com a função print, vale mencionar que devido a restrição de não usar listas tive que optar por realizar
 o método dessa forma, o que acaba retornando um "", pois não consegui implementar o print como return de maneira eficiente
 com a utilização de listas bastaria criar uma auxiliar para depois retorná-la com todos os dados, possui O(n)=n, visto que sempre é necessário
 percorrer todos os elementos 
 """
 def __repr__(self):
    atual = self.cabeca
    while atual:
        if atual.proximo:
         print(atual.dado, end=" -> ")
        else:
           print(atual.dado)
        atual = atual.proximo
    return ""
 """
 Possui O(n) = 1, pois se trata de um método que liga um novo dado ao elemento mais a esquerda da lista encadeada, sendo necessário apenas
 ligar o dado no anterior e torná-lo a cabeça, além disso aumenta o len
 """
 def inserir_no_inicio(self, dado):
    novo_no = No(dado)
    novo_no.proximo = self.cabeca
    self.cabeca = novo_no
    self._len += 1
 """
 Possui lógica parecida, mas esse adiciona no lado mais a direita. sendo necessário percorrer todos os elementos, tendo O(n)=n, também aumenta o len
 """
 def inserir_no_fim(self, dado):
    novo_no = No(dado)
    if self.esta_vazia():
        self.cabeca = novo_no
        return
    atual = self.cabeca
    while atual.proximo:
        atual = atual.proximo
    atual.proximo = novo_no
    self._len += 1

 """
 Percorre todos os elementos até encontra o argumento dado, se encontrar, remove o elemento, junta seus adjacentes e diminui o len. Caso não encontre
 retorna None, possui O(n)=n pois no pior caso percorre toda a lista 
 """
 def remover(self, dado):
    if self.esta_vazia():
        return
    if self.cabeca.dado == dado:
      self.cabeca = self.cabeca.proximo
      self._len -= 1
      return 
    atual = self.cabeca
    while atual.proximo and atual.proximo.dado != dado:
       atual = atual.proximo
    if atual.proximo:
      atual.proximo = atual.proximo.proximo
      self._len -= 1     


class Pilha(ListaEncadeada):
   """
   Observação: Optei por não fazer o len visto que herda da classe ListaEncadeada e já foi devidamente explicado na lista encadeada, que resumindo
   altera a cada operação de adição/remoção, o mesmo se aplica ao esta_vazia()
   """
   """
   'Método' de representação, funciona de maneira análoga ao da lista encadeada, sendo essa a classe que herda algumas características
   """
   def __repr__(self):
      if self.cabeca is None:
         return "Pilha vazia"
      print("Início", end=" -> ")
      atual = self.cabeca
      while atual is not None:
         print(atual.dado, end=" -> ")
         atual = atual.proximo
      return "Fim"
   """
   Método que equivale ao inserir no incio da classe lista encadeada, embora preferi reescrever para reforçar seu papel. Tem O(n) = 1 visto que
   segue o princípio FIFO (First In First Out) e só necessário seguir a lógica do inserir no início
   """
   def push(self, data):
      ndata = No(data)
      ndata.proximo = self.cabeca
      self.cabeca = ndata
      self._len += 1
   """
   Método de remoção, remove da pilha apenas o elemento do topo, possuindo então O(n) = 1, retorna o elemento apagado e diminui o len.
   Em caso de pilha vazia retorna um erro
   """
   def pop(self):
      if self.cabeca is None:
         raise IndexError("Pilha sem elementos")
      valor = self.cabeca.dado
      self.cabeca = self.cabeca.proximo
      self._len -=1
      return valor
   '''
   Método que retorna o elemento do topo, possuindo então O(n)=1, levanta um erro em caso de pilha vazia
   '''
   def topo(self):
      if self.cabeca is None:
         raise IndexError("Pilha sem elementos")
      return self.cabeca.dado
#Unittest a seguir
print("\n---------------------------\n\n\nUnittest das pilhas\n---------------------------\n\n")
Pilha1 = Pilha()
for i in range(10):
   Pilha1.push(i)
   Pilha1.push(i+1)
   Pilha1.pop()
print(Pilha1)
print(f"Tamanho da pilha: {len(Pilha1)}")
print(f"Removendo o {Pilha1.topo()}, pois segue o lifo, onde Pilha1.pop() = {Pilha1.pop()}")
print(Pilha1)
print(f"Elemento no topo: {Pilha1.topo()}")
print(f"Novo tamanho da pilha: {len(Pilha1)}")
for k in range(len(Pilha1)):
   Pilha1.pop()
print(f"Esvaziamos a saída, Pilha = {Pilha1}")
for t in range(10):
   Pilha1.push(t+1)
Pilha1.push(None)
Pilha1.push("Teste")
print(Pilha1)
for e in range(12):
   Pilha1.pop()
print(f"Esvaziamos a Pilha novamente, Nova Pilha = {Pilha1}")
print(f"Testes de output na pilha para os métodos topo e pop, respectivamente")
#print(Pilha1.pop())
#print(Pilha1.topo()) Coloquei em comentário para mostrar os resultados da fila, é reecomendável editar essa parte caso queira testar
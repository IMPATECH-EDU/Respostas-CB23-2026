import P06_3514_pilha_encadeada as p
class Fila():
   """
   "Método" de iniciação, define como base 2 pilhas, uma de entrada e outra de saida, em suma, o que iremos fazer é montar a de entrada
   e depois mandá-los para a de saída, pois assim é possível inverter a ordem do LIFO para o FIFO (First In First Out)
   além disso é adicionado o len que segue a mesma lógica da pilha e também um valor cabeça
   """
   def __init__(self):
    self.entrada = p.Pilha()
    self.saida = p.Pilha()
    self._len = 0
    self.cabeca = None
   """
   Método que retorna o tamanho da fila, é atualizado a cada adição/remoção na mesma, por isso tem O(n) = 1
   """
   def __len__(self):
      return self._len
   ''' O código abaixo é a maneira que encontrei de representação, o uso de listas se dá por convenção e armazenar o retorno, não sendo necessário no
   decorrer da implementação'''
   def __repr__(self):
      if self.entrada.esta_vazia() and self.saida.esta_vazia():
         return "Fila vazia"
      elem = []
      atual = self.saida.cabeca
      while atual:
         elem.append(str(atual.dado))
         atual = atual.proximo
      elementos = []
      atual = self.entrada.cabeca
      while atual:
         elementos.append(str(atual.dado))
         atual = atual.proximo
      elem.extend(reversed(elementos))
      return "Frente -> " + " -> ".join(elem) + " -> Fim"
      

   """
   Adicionamos um elemento na Pilha de entrada, mas o efeito em si é adicionar um termo na fila no último lugar, tem O(n)=1 pois é efetuado
   apenas com um push e atualização do len, que possuem tempos constantes
   """
   def enfileirar(self, data):
    self.entrada.push(data)
    self._len += 1
   """
   Método de remoção, consiste em passar todos os elementos da pilha de entrada para a de saída, onde a cada chamada adiciona os termos na pilha de saída
   portanto, no caso médio possui O(n) = 1 pois assumimos a pilha de entrada praticamente vazia, embora no pior caso tenha que fazer n operações de push
   além disso diminui o len em 1
   """
   def desenfileirar(self):
         if self.entrada.esta_vazia() and self.saida.esta_vazia():
            raise IndexError("Fila vazia")
         if self.saida.esta_vazia():
            while not self.entrada.esta_vazia():
               atual = self.entrada.pop()
               self.saida.push(atual)
         self._len -= 1
         return self.saida.pop()
         
   """
   Segue a mesma lógica das pilhas do desenfileirar, embora esse não tire o elemento da fila, esse método retorna o elemento da frente e levanta erro 
   em caso de Fila sem elementos        
   """      
   def frente(self):
      if self.entrada.esta_vazia() and self.saida.esta_vazia():
         raise IndexError("Fila sem elementos")
      if self.saida.esta_vazia():
         while not self.entrada.esta_vazia():
            self.saida.push(self.entrada.pop())
      return self.saida.topo()
print("\n---------------------------\n\n\nUnittest das Filas\n---------------------------\n\n")
Fila1 = Fila()
for i in range(10):
   Fila1.enfileirar(i)
   Fila1.enfileirar(i+1)
   Fila1.desenfileirar()
print(Fila1)
print(f"Tamanho da Fila: {len(Fila1)}")
print(f"Removendo o {Fila1.frente()}, pois segue o fifo, onde Fila1.desenfileirar() = {Fila1.desenfileirar()}")
print(Fila1)
print(f"Elemento no topo: {Fila1.frente()}")
print(f"Novo tamanho da Fila: {len(Fila1)}")
for k in range(len(Fila1)):
   Fila1.desenfileirar()
print(f"Esvaziamos a saída, Nova Fila = {Fila1}")
for t in range(10):
   Fila1.enfileirar(t+1)
print(Fila1)
for e in range(10):
   Fila1.desenfileirar()
print(f"Esvaziamos a Fila novamente, Nova Fila = {Fila1}")
print(f"Testes de output na Fila para os métodos frente e desenfileirar, respectivamente")
print(Fila1.desenfileirar())
print(Fila1.frente())
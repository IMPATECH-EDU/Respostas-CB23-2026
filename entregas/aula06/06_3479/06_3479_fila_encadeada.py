import importlib

_pilha_mod = importlib.import_module("06_3479_pilha_encadeada")
PilhaEncadeada = _pilha_mod.PilhaEncadeada# importa a pilha encadeada do arquivo em que ela está
class FilaEncadeada:
  '''Cria a fila encadeada, onde usaremos 2 pilhas, formando a composição'''
  def __init__(self): 
    '''Cria os atributos que serão usados, no caso, 2 pilhas'''
    self._entrada = PilhaEncadeada() 
    self._saida = PilhaEncadeada() 
  def enfileirar(self,item): 
    '''Método que adiciona um elemento no fim da fila, o correspondente a adicionar no topo de uma pilha
    Complexidade: O(1) para todas as operações''' 
    self._entrada.push(item)
  def desenfileirar(self): 
    '''Método que remove e retorna o item da frente da FILA; levanta IndexError se estiver vazia
    Complexidade: O(1) amortizada (caso médio)''' 
    # basicamente, vamos repassar os elementos de uma pilha para outra e tirar o elemento do topo da segunda pilha 
    if self._entrada.esta_vazia() is True and self._saida.esta_vazia() is True: 
      raise IndexError('a fila está vazia') 
    if self._saida.esta_vazia() is True: 
      while self._entrada.esta_vazia() is not True:
        self._saida.push(self._entrada.pop()) 
    return self._saida.pop()  
  def frente(self): 
    '''Método que retorna o item da frente sem removê-lo; levanta IndexError se a fila estiver vazia
    Complexidade: O(1) amortizada (caso médio)'''
    if self._entrada.esta_vazia() is True and self._saida.esta_vazia() is True:
      raise IndexError('a fila está vazia')
    if self._saida.esta_vazia() is True:
      while self._entrada.esta_vazia() is not True:
        self._saida.push(self._entrada.pop()) 
    return self._saida.topo() 
  def esta_vazia(self):
        '''retorna True quando não há elementos armazenados na fila
        Complexidade: O(1) para todas as operações'''
        if self._entrada.esta_vazia() is True and self._saida.esta_vazia() is True:
          return True
        else:
          return False 
  def __len__(self):
    '''Retorna o tamanho total da fila
    Complexidade: O(1) para todas as operações'''
    return len(self._entrada) + len(self._saida)
  def __repr__(self):
    '''Representação textual da fila (ou seja, da segunda pilha de cima para baixo)
    Complexidade: O(N) para todas as operações'''
    elementos = []
    copia_saida = PilhaEncadeada()
    copia_entrada = PilhaEncadeada()
    while self._saida.esta_vazia() is not True:
      val = self._saida.pop()
      elementos.append(repr(val))
      copia_saida.push(val)
    while copia_saida.esta_vazia() is not True:
      self._saida.push(copia_saida.pop())

    while self._entrada.esta_vazia() is not True:
      copia_entrada.push(self._entrada.pop())
    while copia_entrada.esta_vazia() is not True:
      val = copia_entrada.pop()
      elementos.append(repr(val))
      self._entrada.push(val)

    return f"FilaEncadeada([{', '.join(elementos)}])"

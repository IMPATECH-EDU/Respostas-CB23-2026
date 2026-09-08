class PilhaEncadeada:
  ''' Cria a pilha encadeada '''
  class _No:
    ''' Classe auxiliar que cria o nó '''
    def __init__(self,valor,proximo):
      '''Definindo os atributos "valor" e "próximo" para saber qual o valor que o nó guarda e para quem ele aponta'''
      self.valor = valor
      self.proximo = proximo # me diz o valor que está acima do atual
    # vai nos auxiliar no momento de verificar o "len" da pilha, esse é o nosso contador
  def __init__(self):
    '''Definindo os atributos "top" e "comprimento" para saber quem está no topo da pilha e qual o seu comprimento
    Complexidade: O(1) para todas as operações'''
    self.top = None # a pilha está vazia, esse foi o primeiro elemento a existir
    self.comprimento = 0
  def push(self,item): 
    '''Método para inserir o elemento "item" no topo da pilha
    Complexidade: O(1) para todas as operações'''
    self.top = self._No(item,self.top)
    self.comprimento +=1
  def pop(self):
    '''Método que remove e retorna o item do topo, além de levantar IndexError se a pilha estiver vazia
    Complexidade: O(1) para todas as operações'''
    if self.comprimento == 0:
      raise IndexError("a pilha está vazia")
    valor = self.top.valor
    self.top = self.top.proximo
    self.comprimento -=1
    return valor
  def topo(self):
    '''Método que retorna o item do topo sem removê-lo; levanta IndexError se a pilha estiver vazia
    Complexidade: O(1) para todas as operações'''
    if self.comprimento == 0:
      raise IndexError("a pilha está vazia")
    return self.top.valor
  def esta_vazia(self):
    '''Método que retorna True quando não há elementos armazenados
    Complexidade: O(1) para todas as operações'''
    if self.comprimento == 0:
      return True
    return False
  def __len__(self):
    '''Método que retorna a quantidade de elementos; exige contador mantido incrementalmente
    Complexidade: O(1) para todas as operações'''
    return self.comprimento
  def __repr__(self):
    '''Método que apresenta uma representação textual legível, do topo para a base
    Complexidade: O(N)'''
    nohs = []
    pilha_i = self.top
    while pilha_i is not None:
      nohs.append(repr(pilha_i.valor))  # Usa repr para mostrar strings com aspas
      pilha_i = pilha_i.proximo
    return f"PilhaEncadeada([{', '.join(nohs)}])"
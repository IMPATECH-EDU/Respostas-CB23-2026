class Node:
    """Representa um nó que possui um elemento e um ponteiro
    Args:
        valor = objeto que usamos para ser o inicio do nó
        proximo = objeto que apontamos como o próximo de um nó
    Atributos:
        head: Aponta para o valor do parâmetro.
        next: Aponta para o próximo valor do nó."""
    def __init__(self,valor,proximo=None):
        """Instancia um objeto da classe nó
        Recebe com parâmetro uma string ou int
        .head = ao parâmetro recebido
        .next = aponta para o proximo elemento"""
        self.head = valor
        self.next = proximo
class PilhaEncadeada:
    """É um tipo de armazenamento de objetos que empilha cada objeto de forma encadeada.

    Args:
        Valor = objeto que é inserido no início da lista.
    Atributos:
        Início = objeto da classe Node que foi instanciado com o args Valor.
    """
    def __init__(self,valor = None):
        No = Node(valor)
        self.inicio = No
        if valor is None:
            self.len = 0
        else:
            self.len = 1
    def push(self,item):
        """Insere um elemento no começo da PilhaEncadeada.
        Args:
            item: objeto que queremos adicionar no começo da pilha encadeada.
        Returns:
            None.
        Complexidade O(1)"""
        No_novo = Node(item)
        No_novo.next = self.inicio
        self.inicio = No_novo
        self.len += 1
    def pop(self):
        """Remove e retorna o elemento que está no topo da PilhaEncadeada
        Returns:
            Retorna o elemento que está no topo da PIlhaEncadeada
        Raises:
            IndexError:Se a lista for vazia.
        Complexidade: O(1)"""
        if self.len == 0:
            raise IndexError("A pilha está vazia!")
        self.len -= 1
        primeiro_no = self.inicio
        self.inicio = primeiro_no.next
        return primeiro_no.head
    def topo(self):
        """Retorna o elemento do topo da PilhaEncadeada.
        Returns:
            Retorna o elemento que está no topo da lista.
        Raises:
            IndexError: Se a lista estiver vazia.
        Complexidade O(1)"""
        if self.len == 0:
            raise IndexError("A lista está vazia!")
        return self.inicio.head
    def esta_vazia(self):
        """Verifica se a PilhaEncadeada está vazia ou não.
        Returns:
            Se a PilhaEncadeada estiver vazia, retorna True
            caso contrário, retorna False.
        Complexidade: O(1)"""
        if self.len == 0:
            return True
        return False
    def __len__(self):
        """Calcula quantos elementos a PilhaEncadeada possui.
        Returns:
            Retorna um inteiro que representa a quantidade de elementos na PilhaEncadeada.
        Complexidade: O(1)"""
        return self.len
    def __repr__(self):
        """Cria uma representação da PilhaEncadeada.
        Returns:
            Retorna uma string que representa os elementos da nossa lista
            do topo para a base
        Complexidade: O(n)"""
        if self.len == 0:
            return "None"
        p = self.inicio
        saida = " | " + str(p.head) + " | "
        for i in range(1,len(self)):
            p = p.next
            saida += str(p.head) + " | "
        return saida
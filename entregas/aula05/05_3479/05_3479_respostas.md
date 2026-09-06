# Questão 1
# Classes-Base: Pessoa, Restaurante, Iguaria, Funcionário
# Subclasses: Funcionário, Pizzaria, Pizza, Bolo, Garçom, Chefe de cozinha, Gerente
# Justificativa: vejamos que a classe Pessoa indica o nome e a idade, que são os 
# atributos esperados para um funcionário. Nesse caso, Pessoa é a classe-base da classe
# Funcionário, que herda as str 'nome' e 'idade'. 
# Vejamos também que a classe Garçom, Chefe de cozinha e Gerente são objetos correlacionados
# à classe Funcionário, sendo, então, subclasses suas. Elas herdam os atributos salario e
# carga_horaria. 
# Restaurante é a classe-base da classe Pizzaria, que herda os atributos 'nome' e 'endereço', já
# que Restaurante é uma classe mais genérica e Pizzaria, mais específica. 
# Iguaria é a classe-base das subclasses Pizza e Bolo, as quais herdam os atributos 'nome' e 'preco'. 
# Mais uma vez, isso ocorre porque Iguaria é uma classe mais genérica e as classes Pizza e Bolo são 
# específicas do que essa classe deseja indicar: comidas. 

# Questão 2
# Podemos pensar na classe Iguaria como um "cardápio" de comidas do restaurante. Então
# a classe Restaurante é definida e, dentro dela, criamos a classe Iguaria. Nesse caso, 
# seria interessante ter atributos para definir esse cardápio, a princípio. Seria algo
# semelhante ao seguinte:
# class Restaurante:
#   def __init__(self, nome, endereco):
#        self.nome = nome
#        self.endereco = endereco
#        self.iguarias = []
#    def pratos(self, iguaria): 
#        self.iguarias.append(iguaria)
#    def cardapio(self):
#        return self.iguarias
#    
#    class Iguaria:
#        def __init__(self, nome, preco):   
#            self.nome = nome
#            self.preco = preco 
# Isso seria legal para conseguirmos estruturar um pedido, como esse:
# restaurante = Restaurante("Pizzaria Impateca", "Av. Pereira Reis")
# pedido = restaurante.Iguaria("Pizza de frango", 32.0)

# Questão 3
# Argumento 1: é um pedido, que é, basicamente, a iguaria. Se é pizza, temos como resposta True 
# ou False; se é bolo, temos a str que armazena as informações. Então, podemos considerar o pedido
# como uma lista da classe Iguaria, que é uma classe-base como definido mais acima. 
# Argumento 2: recebe o pedido escrito pelo garçom. Então, podemos manter a lista da classe Iguaria;
# Argumento 3: recebe o nome do funcionário que deve demitir. Então, esse argumento deve
# uma instância da classe Funcionário, que é classe-base da subclasse Gerente. 
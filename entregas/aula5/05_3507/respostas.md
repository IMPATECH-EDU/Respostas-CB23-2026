# Aula 5 - Diagrama UML

# Questão 1:
    
    As classes Garçom, Gerente, Chefe de Cozinha herdam os atributos da classe funcionarios já que todas essas classes são tipos especificos de funcionários sendo assim características gerais de funcionário com carga horária e salário são herdadas. Já a classe funcionário herda de Pessoa pois todo funcionario é uma Pessoa assim atributos como nome e idade são herdados por Funcionários. De forma analoga a classe Pizzaria herda de Restaurante pois toda classe é um Restaurante e portanto deve possuir os atributos de um restaurante mais os especificos de uma Pizzaria

# Questão 2:
    
    A relação entre as classes Restaurante e Iguaria é feita por meio de uma classe intermediaria, Cardapio que possui uma lista de outra classe Itens_Cardapio cada instancia do tipo Item_Cardapio se relaciona apeas com uma instancia de Iguaria sendo uma relação de agregação, ou seja, a Iguaria não tem uma dependencia forte com o Item cardapio. além disso a classe Pedido foi necesária para modelar o funcionamento dos métodos de Garçom e chefe de cozinha 

# Questão 3:

    O argumento 1 é do tipo Cardapio pois para que o Garçom crie o pedido a única informação necessária é saber os itens do cardapio para sugerir a um cliente tal método deve retornar um pedido que é uma classe que possui um dicionário em que as chaves são os nomes dos item pedidos e o valor é a quantidade de cada item que foi pedido. Continuando o tipo do Argumento 2 deve ser justamente Pedido pois o Chefe de Cozinha deve receber um Pedido para saber quais guarnições devem ser feitas. Já o argumento 3 deve ser do tipo Funcionário pois somente pode-se demitir alguém que seja funcionário do restaurante.

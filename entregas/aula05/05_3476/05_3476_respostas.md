Questão 1
        Classe: Pessoa
            Subclasses: Funcionário, Chefe de cozinha, Gerente
        Classe: Iguaria
            Subclasses: Bolo, Pizza
        Classe: Restaurante
            Subclasse: Pizzaria
Questão 2

Seria necessário implementar um atributo "Cardapio" dentro da classe "Restaurante" que seria uma Lista de instâncias da classe com todas as iguarias disponíveis no restaurante. 

Questão 3

argumento1 = Iguaria, porque um possível cliente do restaurante realizaria um pedido ao garçom que estaria na atributo "cardápio" composta por atributos da classe "Iguaria"
argumento2 = Iguaria, porque o chefe de cozinha iria preparar o pedido feito ao garçom, que é um atributo de "Iguaria"
argumento3 = Funcionário, porque o gerente iria demitir um funcionário, e para isso iria consultar os atributos de "Funcionário"
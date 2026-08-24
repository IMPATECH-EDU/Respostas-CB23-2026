**1)**



Restaurante

|- Pizzaria



Pizzaria herda: nome, endereço, telefone



Pessoa

|- Funcionário

&#x20; |- Garçom

&#x20; |- Gerente

&#x20; |- Chefe de cozinha



Funcionário herda: nome e idade



Garçom, Gerente, Chefe de cozinha herdam: nome, idade, salário, carga horária



Iguaria (comida)

|-Bolo

|-Pizza



Bolo, Pizza herdam: nome, preço



**2)**



Seria modelada na forma de um atributo cardápio em Restaurante, que constrói um conjunto com os objetos Iguarias que são servidos. Esse atributo seria herdado por Pizzaria. Por exemplo, no cardápio de Pizzaria, estaria {Pizza}.




**3)**



argumento1 -> Pedido

Recebe um Pedido, uma classe que possui atributos de mesa: int e lista de iguarias: list(iguaria)



argumento2 -> Pedido

Recebe uma instância de Pedido, com número de mesa para organização de ordem de cocção e lista de iguarias para preparo



argumento3 -> Funcionário

Recebe uma instancia de funcionário para efetuar a demissão


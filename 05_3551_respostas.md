# Aula prática 24/08

1 - A primeira classe base seria a “Pessoa”, que geraria a subclasse “Funcionário” e essa mesma herdaria os atributos nome e idade. Da subclasse “Funcionário” sairiam as subclasses “Garçom”, “Chefe de cozinha” e “Gerente”, e eles herdariam os atributos “salário” e “carga horária”.  Já a segunda classe base seria “Restaurante” que geram “Bolo” e “Iguaria” e uma terceira classe possível seria “Pizzaria” que gera “Pizza”.


Em forma de diagrama seria:

Pessoa:

---> Funcionário:
    ---> Garçom
    ---> Chefe de Cozinha
    ---> Gerente

Pizzaria:
---> Pizza

Restaurante:
---> Bolo
---> Iguaria





2 - A classe “Iguaria” seria uma classe filha da classe “Restaurante”, poderia ser criado um atributo chamado “nome_restaurante” e “endereço_do_restaurante para o nome e endereço do restaurante no qual a iguaria é servida, a fim de facilitar essa relação.



3 - Para o argumento1, que está relacionado ao garçom, seria apropriado atribuir a ele um dicionário com o “nome do pedido” como chave que aponta para a quantidade de pedidos desse tipo, a fim de facilitar a entrega dos pedidos. Para o argumento2, que pertence ao chefe de cozinha, atribuiria uma lista com o nome de cada prato na ordem na qual foram pedidos, assim vamos evitar que cada cliente espere um tempo desproporcional. E para o argumento3 atribuiria um conjunto com os funcionários, pois a ordem que os funcionários devem ser demitidos não importa para efeitos práticos.
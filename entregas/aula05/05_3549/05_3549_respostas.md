# Questão 1:

- Pessoa
    - Funcionário
        - Garçom
        - Chefe de Cozinha
        - Gerente

- Iguaria (comida)
    - Pizza
    - Bolo

- Restaurante
    - Pizzaria

Todas as classes filhas herdam os atributos e métodos de suas respectivas classes pais ou até "avós". Isso porquê todos os atributos e métodos das classes pais são relevantes para os filhos.

# Questão 2:
A classe "Iguaria" é completamente dependente da classe restaurante, pois sem restaurante não existe comida, porém não tem uma relação de herança já que não há necessidade ou sequer utilidade de uma iguaria herdar atributos como "endereco". Essa relação deve ser implementada tendo em conta que cada restaurante pode ter várias comidas e cada tipo de comida pode estar no menu de vários restaurantes. Sendo assim, seria útil criar uma classe "menu" ou "cardápio" para relacionar essas duas classes mães de maneira mais intuitiva e fácil de aplicar. Além disso, podemos adicionar o atributo "ingredientes" às iguarias, deixaria mais pesado, mas poderia facilitar alguns processos.

# Questão 3:
- Argumento 1:
    Deve ser uma lista ordenada de dois elementos: O nome do cliente (para isso precisariamos criar uma classe "cliente" que herdaría de "pessoa" e teria como atributo adicional "mesa"), e uma lista com todas as iguarias que foram pedidas pelo cliente. Isso pois um pedido pode mudar, seja trocando ou pedindo mais coisas, e é importante saber quem fez o pedido.
- Argumento 2:
    Poderia se criar uma classe de "Pedidos" que serviria como o argumento 2. Mas evitando criar mais classes, deve ser uma lista com todos as iguarias de um pedido. Para deixar ainda melhor, pode ser a mesma lista que foi dada como argumento 1, já que assim que o pedido for concluído, já estará disponível a informação de qual cliente deve receber (juntamente com a mesa onde este está).
- Argumento 3:
    Deve ser um dos filhos da classe "funcionário", ou a própria. Porquê o gerente, se for demitir alguém, deve demitir um dos seus funcionários. No geral depende de como for implementado para facilitar a execução do código.

Nota: Só consegui visualizar o png com fundo escuro, então alterei a fonte para claro para facilitar a leitura, espero que esteja legível :)
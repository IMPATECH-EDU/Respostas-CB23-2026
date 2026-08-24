## Questão 1:
Hierarquia de Pessoas/Funcionários:
* Classe Base:
  * Pessoa (atributos: nome, idade).
    * Subclasse:
      * Funcionário: Herda "nome" e "idade" de Pessoa; adiciona "salario" e "carga_horaria".
        * Subclasses:
          * Garçom: Herda todos os atributos de Pessoa e de Funcionário; adiciona o método "anotar_pedido()".
          * Chefe de cozinha: Herda todos os atributos de Pessoa e de Funcionário; adiciona o método "preparar()".
          * Gerente: Herda todos os atributos de Pessoa e Funcionário; adiciona o método "demitir()".

Hierarquia de Alimentos:
* Classe Base:
  * Iguaria (comida) (atributos: nome, preco).
    * Subclasses:
      * Pizza: Herda "nome" e "preco" de Iguaria; adiciona o atributo "borda_rechada".
      * Bolo: Herda "nome" e "preco" de Iguaria; adiciona o atributo "formato".

Hierarquia de Estabelecimentos:
* Classe Base:
  * Restaurante (atributos: nome, endereco, telefone).
    * Subclasse:
      * Pizzaria: Herda "nome", "endereco" e "telefone" de Restaurante, adiciona o atributo "rodizio".

---

## Questão 2:

O modelo entre Restaurante e Iguaria pode ser feito criando uma nova classe chamada "Cardapio". Assim, a classe Restaurante terá um novo atributo do tipo Cardapio, e ele guardará uma lista com os objetos da classe Iguaria (comida). O Cardapio deve gerenciar a lista com métodos próprios para adicionar e remover pratos.

---

## Questão 3:

Para o "argumento1" (método anotar_pedido()):
* uma lista de objetos da classe Iguaria (comida), pois o garçom é responsável por registrar os pedidos dos clientes, os quais geralmente contêm um ou mais itens do cardápio, permitindo assim que objetos de qualquer subclasse, como Pizza ou Bolo, sejam armazenados e processados.

Para o "argumento2" (método cozinha.preparar()):
* um objeto da classe Iguaria (comida), visto que a função principal do chefe é cozinhar um alimento específico do menu e, ao utilizar a classe Iguaria (comida), garantindo que o método consiga receber qualquer prato existente no sistema, como um Bolo ou uma Pizza.

Para o "argumento3" (método Gerente.demitir()):
* um objeto da classe Funcionário, já que a atribuição do gerente é a gestão administrativa do pessoal da casa e, ao declarar o objeto da classe base Funcionário, o método fica genérico o suficiente para realizar a demissão de qualquer colaborador da equipe, seja ele um Garçom ou um Chefe de cozinha.
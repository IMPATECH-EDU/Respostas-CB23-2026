# 3514: Atividade 5
## **Questão 1:**
## Classes base:
* **Iguaria (comida)**
* **Pessoa**
* **Restaurante** 

 A explicação decorre do fato de ambas estabelecerem bases para todas as outras classes. Visto que todas presentes na imagem ou se tratam de comidas, pessoas ou restaurantes.

## Subclasses:
### **Funcionário (Subclasse de Pessoa):**

Herda de pessoa o nome e idade, mas adicona os atributos salario e carga_horaria.

### **Garçom (Subclasse de Funcionário)**
Herda de funcionário e pessoa, ou seja, herda nome, idade, salario e carga_horaria, mas adiciona o método anotar_pedido(), cujo argumento podemos supor que é uma lista de iguarias

### **Chefe de cozinha (subclasse de Funcionário)**
Herda de funcionário e pessoa, ou seja, herda nome, idade, salario e carga_horaria, mas adiciona o método preparar(), cujo argumento podemos supor que é uma iguaria

### **Gerente (subclasse de Funcionário)**
Herda de funcionário e pessoa, ou seja, herda nome, idade, salario e carga_horaria, mas adiciona o método demitir(), que podemos supor que tem como valor de entrada um objeto da classe funcionário (Ex: Garçom)

### **Pizzaria (Subclasse de Restaurante):**
Herda de Restaurante o nome, endereço e telefone, mas adicona o atributo rodizio que é do tipo bool, além disso ele herda por que uma pizzaria é um restaurante

### **Pizza (Subclasse de Iguaria):**
Herda de Iguaria o nome e preço, mas adicona o atributo borda_recheada que é do tipo bool, pois se trata de uma comida

### **Bolo (Subclasse de Iguaria):**
Herda de Iguaria o nome e preço, mas adicona o atributo formato, pois se trata de uma comida
#
# Questão 2: (Relação entre Restaurante e iguaria)

    Poderiamos implementar uma associação de elementos, de forma que cada restaurante "Apontasse" para uma lista de iguarias, que seria seu menu, dessa forma a remoção de um restaurante não afetaria os objetos de iguaria, no caso supondo Giraffas = Restaurante(), poderiamos adicionar um novo atributo menu = list() (para acessarmos elementos da classe iguaria), onde a principio Giraffas.menu = [], a menos que criássemos um método add_iguaria(Iguaria), que adicionasse comidas no menu e um remove_iguaria(Iguaria) que removesse, além disso, poderia também tornar menu como uma classe, embora não necessário, seria de bom uso e de boa organização a implementação do mesmo, nesse cenário, bastaria adiconar como atributo em restaurante um objeto da classe menu e realizar alguns pequenos ajustes
#
# Questão 3: 
    Como já mencionado na atividade 1, poderíamos supor que tanto o método preparar() e anotar_pedido() consistiriam de objetos da classe Iguaria, embora dependendo da implementação estariam em listas ou não, no caso adotado, optei por preparar receber um único alimento por vez, pois poderia retornar uma lista contendo tempo, qualidade do prato etc.. E o método anotar_pedido() optei por ser uma lista de iguarias, pois cada cliente teria uma lista com seus desejos. Adicionalmente, o método demitir() tem como argumento um objeto da classe funcionário (Ou lista de funcionários, mas novamente, se trata de uma questão de como deseja ser implementado), optei por ser um único funcionário por vez.
    
    Resumindo os argumentos:
    Método anotar_pedido() -> list[Iguaria]
    Método demitir() -> Funcionário
    Método preparar() -> Iguaria
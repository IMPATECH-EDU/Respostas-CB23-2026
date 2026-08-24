# Exercício 1

# 1) Pessoa 

**Classe base: Pessoa.**

**Atributos próprios:**
Nome,
Idade.

**A classe Pessoa** é uma classe mãe.

# 1.1 Funcionário

**Subclasse de: Pessoa.**

**Atributos herdados:**
Nome,
Idade.

**Atributos próprios:**
Salário,
Carga Horária.

**A classe Funcionário** herda os atributos Nome e Idade da classe Pessoa e possui também seus próprios atributos para funcionários.

# 1.1.1 Chefe de Cozinha

**Subclasse de: Funcionário.**

**Atributos herdados:**
Nome,
Idade,
Salário,
Carga Horária.

**Função própria:**
Preparar.

**O Chefe de Cozinha** herda as características de Funcionário e de Pessoa, além de possuir função específica de preparar.

# 1.1.2 Garçom

**Subclasse de: Funcionário.**

**Atributos herdados**
Nome,
Idade,
Salário,
Salário,
Carga Horária.

**Função Própria**
Anotar Pedidos.

**O Garçom** herda as características de Funcionário e de Pessoa, além de possui função específica de anotar pedidos.

# 1.1.3 Gerente

**Subclasse de: Funcionário.**

**Atributos herdados**
Nome,
Idade,
Salário,
Salário,
Carga Horária.

**Função Própria**
Demitir.

**O Garçom** herda as características de Funcionário e de Pessoa, além de possui função específica de demitir.

# 2) Restaurante

**Classe base: Restaurante.**

**Atributos próprios**
Nome,
Endereço,
Telefone.

**A classe Restaurante** é uma classe mãe.


# 2.1 Pizzaria

**Subclasse de: Restaurante.**

**Atributos herdados**
Nome,
Endereço,
Telefone.

**Atributos próprios:**
Rodízio

A Pizzaria herda as informações de Restaurante e possui características próprias sobre servir ou não rodízio.

# 3) Iguaria

**Classe base: Iguaria.**

**Atributos próprios**
Nome,
Preço.

**A classe Iguaria** é uma classe mãe.

# 3.1 Pizza

**Subclasse de: Iguaria.**

**Atributos herdados**
Nome,
Preço.

**Atributos próprios**
Borda Recheada .

A Pizza herda as características de Iguaria e possui característica específica de possuir ou não borda recheada.

# 3.2 Bolo

**Subclasse de: Iguaria.**

**Atributos herdados**
Nome,
Preço.

**Atributos próprios**
Formato.

O Bolo herda as características de Iguaria e possui característica específica de formato.

# Exercício 2

A relação entre Restaurante e Iguaria pode ser feita através da criação de um MENU, onde um restaurante oferece diversas iguarias que esão presentes no MENU.

# Implementação

**A Classe Restaurante pode receber um novo atributo:**

+ Cardapio: Lista com as Iguarias (Iguaria1 , Iguaria2 , ... , IguariaN)

**Também é possível adicionar metódos como:**

+ Adicionar_Iguaria: Recebe uma Iguaria e adiciona no cardápio.
+ Remover_Iguaria: Remove uma Iguaria do cardápio.
+ Listar_Cardapio: Lista todas Iguarias do cardápio.

# Justificativa

Como a **Classe Iguaria** já possui os atributos **Nome** e **Preço**, o gerenciamento do cardápio seria facilitado, permitindo incluir novas comidas, remover itens e consultar todas as opções possíveis. Além de deixar a **Classe Restaurante** com mais funcionalidades.

# Exercício 3

## 1. Atribuição de Tipos aos Argumentos

### **Argumento 1 — Método `anotar_pedido()` na classe `Garçom`**

* **Tipo Recomendado:** Instância da classe **`Pedido`**.

* **Implementação:** Seria necessário adicionar uma classe `Pedido` a qual recebe:
Numero_mesa: int;
Lista_pedidos: list(iguaria1 , iguaria2 , ... , iguarian);
Obs: str.

* **Justificativa:** O garçom atende os clientes e registra o número da mesa, uma lista com os pedidos (`iguarias`) e as observações do pedido.

### **Argumento 2 — Método `preparar()` na classe `Chefe de cozinha`**

* **Tipo Recomendado:** Instância da classe **`Pedido`**

* **Implementação:** Seria necessário adicionar uma classe `Pedido` a qual recebe:
Numero_mesa: int;
Lista_pedidos: list(iguaria1 , iguaria2 , ... , iguarian);
Obs: str.

* **Justificativa:** A responsabilidade principal do chefe de cozinha é a preparação das refeições. Logo o método preparar recebe uma classe pedido, com a lista dos pedidos a serem preparados (`iguarias`) e com as observações de cada pedido.

### **Argumento 3 — Método `demitir()` na classe `Gerente`**

* **Tipo Recomendado:** Instância de lista com **`Funcionários`**.

* **Justificativa:** O gerente atua na gestão de pessoas e processos administrativos. A ação de demitir aplica-se estritamente a um ou mais funcionários, logo ele recebe uma lista com os funcionários a serem demitidos.

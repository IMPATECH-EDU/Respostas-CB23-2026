# Atividade

## 1. Classes-base e herança

Acredito que podemos abstrair as características gerais das classes para definir quais são as classes-base e quais herdam delas.

Desse modo, as classes-base seriam:

- **Pessoa**
- **Restaurante**
- **Iguaria (comida)**

### Hierarquia de `Pessoa`

De `Pessoa`, teríamos a subclasse `Funcionário`, da qual teríamos:

- `Garçom`
- `Chefe de cozinha`
- `Gerente`

`Funcionário` herda de `Pessoa`. `Garçom`, `Chefe de cozinha` e `Gerente` herdam de `Funcionário`.

### Hierarquia de `Restaurante`

De `Restaurante`, apenas `Pizzaria` é subclasse, e herda dele.

### Hierarquia de `Iguaria (comida)`

Já para `Iguaria (comida)`, temos:

- `Bolo`
- `Pizza`

Ambas herdam de `Iguaria (comida)`.

---

## 2. Relação entre `Restaurante` e `Iguaria`

A relação seria de que cada elemento da classe `Restaurante` se relacionaria com instâncias de `Iguarias (comida)`, definindo preço e nome das comidas que o restaurante serve.

Um elemento de `Restaurante` poderia ter como um dos seus atributos uma **lista de iguarias que serve**, sendo que esse atributo seria opcional e, caso nada fosse passado no `__init__`, teria-se uma lista vazia como atributo padrão.

Obviamente, seria necessário um método para adicionar novas opções do tipo `Iguaria (comida)` à lista possuída pelo restaurante.

Além disso, poderia contar com um método que descreve as iguarias que serve e os respectivos preços.

Não acho que seria necessário implementar uma nova classe. Basta possibilitar que uma instância de `Restaurante` tenha uma lista associada de elementos de `Iguaria (comida)` e métodos para alterar tais elementos, adicionando, mudando preço ou retirando.

---

## 3. Tipos dos argumentos dos métodos

### 3.1. Método `.anotar_pedido()`

O tipo apropriado do argumento 1, do método `.anotar_pedido()`, seria **lista de elementos do tipo `string`**, pois o garçom deve anotar a lista dos itens pedidos pelo cliente e, por meio do método, devolver uma lista de elementos de `Iguaria (comida)` para ser passada ao chefe de cozinha e usada para montar a nota fiscal.

Ademais, durante a conversão de `string` para `Iguaria`, seria verificado se o elemento realmente existe dentre as opções da loja, originando um aviso em caso negativo.

### 3.2. Método `.preparar()`

O tipo apropriado do argumento 2, do método `.preparar()`, seria uma **lista de elementos de `Iguaria (comida)`**, pois o método há de ser aplicado a cada objeto que foi anotado pelo garçom e passado ao chefe de cozinha.

### 3.3. Método `.demitir()`

O tipo apropriado para o argumento 3, do método `.demitir()`, é **`Funcionário`**, pois, para ser demitido, precisa ser `Funcionário`, e os atributos de `Funcionário` são indispensáveis para a parte da jurisdição trabalhista no processo de demissão.

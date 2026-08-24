# 2. Questões

## 1. Relações de herança entre as classes

**Pessoa** seria uma classe base, adicionando os atributos `nome` (`str`) e `idade` (`int`).

**Funcionário** herdaria de **Pessoa** os atributos `nome` e `idade`, adicionando os atributos `salario` (`float`) e `carga_horaria` (`int`).

**Garçom** herdaria de **Funcionário** os atributos `nome`, `idade`, `salario` e `carga_horaria`, criando o método `anotar_pedido(argumento1)`.

**Gerente** herdaria de **Funcionário** esses mesmos atributos, além de criar o método `demitir(argumento3)`.

**Chefe de Cozinha** também herdaria de **Funcionário** os atributos `nome`, `idade`, `salario` e `carga_horaria`, além de criar o método `preparar(argumento2)`.

**Restaurante** seria uma classe base, possuindo os atributos `nome` (`str`), `endereco` (`str`) e `telefone` (`str`).

**Pizzaria** herdaria de **Restaurante** os atributos `nome`, `endereco` e `telefone`, além de ter o atributo `rodizio` (`bool`).

**Iguaria** seria uma classe base, possuindo os atributos `nome` (`str`) e `preco` (`float`).

**Pizza** herdaria de **Iguaria** esses atributos, além de ter o atributo `borda_recheada` (`bool`).

**Bolo** herdaria de **Iguaria** os atributos `nome` e `preco`, além de ter o atributo `formato` (`str`).

### Hierarquia de herança

```text
Pessoa
└── Cliente
└── Funcionário
    ├── Garçom
    ├── Gerente
    └── Chefe de Cozinha

Restaurante
└── Pizzaria

Iguaria
├── Pizza
└── Bolo
```

## 2. Relação entre `Restaurante` e `Iguaria`

Eu criaria uma nova classe `Cliente` que herdaria da classe mãe `Pessoa` e possuiria além disso os atributos num_mesa:(int) e pedido: (lista c/ Iguaria), desse modo poderia correlacionar a classe Restaurante, recebendo como parâmetro do metódo anotar_pedido() da classe Garçom, que herda de Restaurante, um objeto da classe Iguaria e enviando para a classe Chefe de Cozinha poder preparar o pedido.

## 3. Escolha de `Argumentos`

Argumento 1: Objeto da classe `Cliente`, que possui os atributos nome:(str), num_mesa:(int) e pedido: (lista c /Iguaria)

Argumento 2: Objeto da classe `Iguaria`, acessando o atributo name. Pois para o Chef de Cozinha preparar uma comida é necessário lhe informar o nome da iguaria

Argumento 3: Objeto da classe `Funcionário`, acessando o atributo name. Pois para o Gerente demitir o funcionário é necessário informar a identificação.

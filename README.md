# Respostas-CB23-2026 — Projeto Elevatória

Repositório de entregas das práticas de Programação 2 (IMPATECH, 2026). A branch `main`
contém a base de código do Projeto Elevatória: o software de supervisão de uma estação
elevatória de água, escrito por uma equipe da qual você agora faz parte. Cada aluno trabalha
na sua própria branch e entrega o trabalho em um Pull Request contra a `main`.

**Marco atual:** [Marco 1 — Dados](ENUNCIADO_MARCO1.md).

## Como trabalhar

Você não tem permissão para escrever neste repositório. Trabalhe em um **fork** (a sua cópia)
e envie o Pull Request do fork para cá.

```bash
# 1. No GitHub, clique em "Fork" nesta página para criar a sua cópia.
# 2. Clone o SEU fork, ligue-o a este repositório e crie a sua branch:
git clone https://github.com/<seu_usuario>/Respostas-CB23-2026.git
cd Respostas-CB23-2026
git remote add upstream https://github.com/IMPATECH-EDU/Respostas-CB23-2026.git
git switch -c projeto_<sua_matricula>       # nunca faça commit na main
# ... trabalho, testes, commits ...
git push -u origin projeto_<sua_matricula>  # envia para o seu fork
```

Abra **um único Pull Request** com base `IMPATECH-EDU/Respostas-CB23-2026`, branch `main`, e
head `<seu_usuario>/Respostas-CB23-2026`, branch `projeto_<sua_matricula>`. Use o título
`projeto_<sua_matricula>` e a conta do GitHub associada ao seu e-mail @impatech.edu.br. Abra-o
como rascunho (*Draft*) logo no primeiro marco; os pushes seguintes para a mesma branch do seu
fork atualizam o PR sozinhos. O PR **não será integrado** à `main`: ele é a sua entrega e o
lugar da revisão. Não apague o fork nem a branch até o fim da disciplina.

**Marco novo publicado?** Traga-o para a sua branch e envie para o seu fork:

```bash
git switch projeto_<sua_matricula>
git pull --no-rebase --no-edit upstream main
git push
```

## A base de código

| Pasta ou arquivo | De quem é | Regra |
| --- | --- | --- |
| `fornecido/` | Outra equipe (a disciplina) | **Não altere.** Qualquer mudança aparece no diff do seu PR. Se achar um problema, avise o professor. |
| `elevatoria/` | A equipe da aplicação (você) | Implemente e corrija o que as issues pedem, sem mudar nomes nem assinaturas públicas. |
| `testes/` | Você | Os seus testes automatizados. |
| `marco*.py`, `RELATORIO.md` | Você | Os scripts de demonstração e o seu relatório. |
| `ENUNCIADO_*.md`, `README.md` | A disciplina | Não altere. |

## Regras da casa

**Antes de cada commit**, a partir da raiz do repositório e com o ambiente ativado:

```bash
python -m unittest discover -v
```

**Código**

- Toda função, classe e método público tem docstring com o contrato: o que recebe, o que
  devolve e quando levanta exceção. Toda assinatura tem anotações de tipo.
- Os módulos de `elevatoria/` não imprimem nada: quem imprime são os scripts `marco*.py`.
- Entrada inválida levanta `ValueError` com uma mensagem que diga o que estava errado. Nunca
  devolva `None` em silêncio.
- Em `SerieTemporal`, só operações do NumPy: sem laços sobre os elementos, e nenhum método
  modifica `self`.

**Testes**

- Toda correção de defeito vem com um teste de regressão, escrito antes da correção, que
  falha com o código defeituoso e passa com a correção.
- Cada teste tem uma docstring de uma linha dizendo qual caso ele cobre.
- Compare números de ponto flutuante com `assertAlmostEqual` ou `np.allclose`, nunca com `==`.

**Commits e Pull Request**

- Commits pequenos, uma ideia por commit.
- Nunca inclua ambientes virtuais nem `__pycache__` (o `.gitignore` já cuida disso).
- A descrição do PR diz o que mudou, como foi testado e o que o revisor deve olhar com
  atenção (modelo no enunciado de cada marco).
- Todo o código enviado deve ter sido executado, testado e lido por você, inclusive o gerado
  com ajuda de IA. O que está na `main` fica fora da comparação do antiplágio; a comparação
  recai sobre o que o seu PR muda.

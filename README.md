# Data Structures Lab

Repositório de estudo de estruturas de dados: implementações do zero, testes e anotações sobre complexidade de cada operação.

O objetivo não é reinventar bibliotecas prontas, e sim entender **como** cada estrutura funciona por dentro, **por que** ela é mais rápida ou mais lenta para certas operações e **quando** escolher uma em vez de outra.

## Trilha de estudo

| # | Tema | Pasta | Status |
|---|------|-------|--------|
| 1 | Listas (array dinâmico e lista encadeada) | [01-listas](01-listas/) | ⬜ |
| 2 | Pilhas e filas | [02-pilhas-e-filas](02-pilhas-e-filas/) | ⬜ |
| 3 | Tabelas hash | [03-tabelas-hash](03-tabelas-hash/) | ⬜ |
| 4 | Árvores (BST, balanceadas) | [04-arvores](04-arvores/) | ⬜ |
| 5 | Heaps e filas de prioridade | [05-heaps](05-heaps/) | ⬜ |
| 6 | Grafos (BFS, DFS, caminhos mínimos) | [06-grafos](06-grafos/) | ⬜ |

## Como cada tema é organizado

Dentro de cada pasta:

- `README.md`: a ideia da estrutura, as operações principais e a complexidade (Big O) de cada uma, com o raciocínio por trás.
- Código de implementação.
- Testes cobrindo casos normais, casos de borda e operações vazias.

## Convenções

- Cada implementação deve ter ao menos um teste de comportamento e um de borda.
- Complexidade se justifica com uma frase, não só com a notação.
- Código comentado apenas onde a lógica não é óbvia.

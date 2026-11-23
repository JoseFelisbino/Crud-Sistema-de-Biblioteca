# Roteiro de testes manuais pelo menu

Roteiro para testar o sistema pelo terminal (e para usar na apresentação).
Siga os passos **na ordem**, porque os IDs dependem dos passos anteriores.
Marque a coluna **OK** com ✅ quando o resultado for igual ao esperado.

**Antes de começar:** apague o arquivo `biblioteca.json` (se existir) para começar com a biblioteca vazia.

Observação: nas opções 3, 5 e 7 o programa pergunta vários dados em sequência.
Na coluna "O que digitar", os valores separados por `→` são digitados um depois do outro, apertando Enter.
`(Enter)` significa apertar Enter sem digitar nada.

## Parte 1 – Início e entradas inválidas no menu

| Passo | O que digitar no menu | Resultado esperado | OK |
|---|---|---|---|
| 1 | No terminal: `py app.py` | Mostra "Nenhum arquivo encontrado. Biblioteca vazia." e o menu | |
| 2 | `abc` | "Digite uma opção numérica válida." e o menu aparece de novo | |
| 3 | `99` | "Opção inválida! Tente novamente." | |
| 4 | `2` | "Listando usuários..." e nenhum usuário listado | |
| 5 | `4` | "Listando Livros..." e nenhum livro listado | |
| 6 | `7` | "Não há livros cadastrados." | |
| 7 | `8` | "Não há empréstimos ativos para devolver." | |

## Parte 2 – Usuários (opções 1 e 2)

| Passo | O que digitar no menu | Resultado esperado | OK |
|---|---|---|---|
| 8 | `1` → `Ana` → `2024001` | "Usuário cadastrado com sucesso!" | |
| 9 | `1` → `Bruno` → `2024002` | "Usuário cadastrado com sucesso!" | |
| 10 | `2` | Lista "ID: 1, Nome: Ana, Matrícula: 2024001" e "ID: 2, Nome: Bruno, Matrícula: 2024002" | |
| 11 | `1` → `(Enter)` → `(Enter)` | **Esperado:** mensagem de erro (nome/matrícula vazios). **Hoje:** o usuário vazio é cadastrado (problema conhecido do UsuarioService). Se cadastrar, apague o `biblioteca.json` e recomece | |

## Parte 3 – Livros (opções 3, 4, 5 e 6)

| Passo | O que digitar no menu | Resultado esperado | OK |
|---|---|---|---|
| 12 | `3` → `(Enter)` → `Machado de Assis` → `1899` → `true` | "O campo título não pode ficar vazio." | |
| 13 | `3` → `Dom Casmurro` → `Machado de Assis` → `abc` → `true` | "O ano deve ser um número inteiro." | |
| 14 | `3` → `Dom Casmurro` → `Machado de Assis` → (ano que vem, ex.: `2030`) → `true` | "O ano deve estar entre 1 e (ano atual)." | |
| 15 | `3` → `Dom Casmurro` → `Machado de Assis` → `1899` → `talvez` | "Disponibilidade inválida. Digite true ou false." | |
| 16 | `3` → `Dom Casmurro` → `Machado de Assis` → `1899` → `true` | "Livro cadastrado com sucesso!" | |
| 17 | `3` → `O Cortiço` → `Aluísio Azevedo` → `1890` → `(Enter)` | "Livro cadastrado com sucesso!" (Enter = disponível) | |
| 18 | `3` → `Iracema` → `José de Alencar` → `1865` → `true` | "Livro cadastrado com sucesso!" | |
| 19 | `4` | Lista os 3 livros (IDs 1, 2 e 3), todos com "Status: Disponível" | |
| 20 | `5` → `abc` | "ID inválido. Digite um número inteiro." | |
| 21 | `5` → `99` → `(Enter)` 4 vezes | "Livro não encontrado." | |
| 22 | `5` → `1` → `(Enter)` → `(Enter)` → `abc` → `(Enter)` | "O ano deve ser um número inteiro." (o livro não muda) | |
| 23 | `5` → `1` → `(Enter)` → `(Enter)` → `1900` → `(Enter)` | "Livro editado com sucesso!" | |
| 24 | `4` | Livro 1 com "Ano: 1900"; título, autor e status continuam iguais | |
| 25 | `6` → `abc` | "ID inválido. Digite um número inteiro." | |
| 26 | `6` → `99` | "Livro não encontrado." | |
| 27 | `6` → `3` | "Livro deletado com sucesso!" | |
| 28 | `4` | Aparecem só os livros 1 e 2 | |

## Parte 4 – Empréstimos (opção 7)

| Passo | O que digitar no menu | Resultado esperado | OK |
|---|---|---|---|
| 29 | `7` → `abc` | Lista os livros e mostra "ID inválido. Digite um número inteiro." | |
| 30 | `7` → `99` | "Livro não encontrado." | |
| 31 | `7` → `1` → `99` | Lista os usuários e mostra "Usuário não encontrado." | |
| 32 | `7` → `1` → `1` | "Empréstimo realizado com sucesso!" e os dados do empréstimo ID 1 com a data de hoje e "Ainda não devolvido" | |
| 33 | `4` | Livro 1 com "Status: Indisponível" | |
| 34 | `7` → `1` → `2` | **"Livro indisponível! Não é possível realizar o empréstimo."** (empréstimo bloqueado) | |
| 35 | `5` → `1` → `(Enter)` → `(Enter)` → `(Enter)` → `true` | "Este livro está emprestado. Registre a devolução para alterar a disponibilidade." | |
| 36 | `6` → `1` | "Não é possível remover este livro, pois ele possui histórico de empréstimos." | |
| 37 | `7` → `2` → `1` | "Empréstimo realizado com sucesso!" (empréstimo ID 2) | |

## Parte 5 – Consultas por usuário (opção 9)

| Passo | O que digitar no menu | Resultado esperado | OK |
|---|---|---|---|
| 38 | `9` → `abc` | "ID inválido." | |
| 39 | `9` → `99` | "Usuário não encontrado." | |
| 40 | `9` → `1` → `5` | "Consulta inválida." | |
| 41 | `9` → `1` → `1` | Lista os empréstimos 1 (Dom Casmurro) e 2 (O Cortiço), ambos "Ainda não devolvido" | |
| 42 | `9` → `2` → `1` | "Nenhum empréstimo encontrado para esse usuário." | |

## Parte 6 – Devolução (opção 8)

| Passo | O que digitar no menu | Resultado esperado | OK |
|---|---|---|---|
| 43 | `8` → `abc` | Lista os empréstimos ativos e mostra "ID inválido." | |
| 44 | `8` → `99` | "Empréstimo não encontrado." | |
| 45 | `8` → `1` | "Livro devolvido com sucesso!" | |
| 46 | `8` → `1` | A lista mostra só o empréstimo 2 e aparece "Este empréstimo já foi devolvido." | |
| 47 | `4` | Livro 1 voltou para "Status: Disponível" | |
| 48 | `9` → `1` → `1` | Mostra só o empréstimo 2 (livros emprestados agora) | |
| 49 | `9` → `1` → `2` | Histórico: empréstimo 1 com a data de devolução de hoje e empréstimo 2 "Ainda não devolvido" | |
| 50 | `7` → `1` → `2` | "Empréstimo realizado com sucesso!" (livro devolvido pode ser emprestado de novo, empréstimo ID 3) | |

## Parte 7 – Gravação em disco

| Passo | O que digitar no menu | Resultado esperado | OK |
|---|---|---|---|
| 51 | `10` | "Saindo..." e "Programa finalizado." | |
| 52 | Abrir o arquivo `biblioteca.json` | Contém as listas "livros", "usuarios" e "emprestimos" com os dados cadastrados | |
| 53 | No terminal: `py app.py` | "Dados anteriores carregados do disco." | |
| 54 | `2` | Ana (ID 1) e Bruno (ID 2) continuam lá | |
| 55 | `4` | Livros 1 e 2 com o mesmo título, autor, ano e status de antes (os dois "Indisponível") | |
| 56 | `9` → `1` → `2` | Histórico da Ana igual ao do passo 49 | |
| 57 | `3` → `Iracema` → `José de Alencar` → `1865` → `true`, depois `4` | Novo livro cadastrado com ID 3 (o ID continua a partir do maior ID salvo) | |
| 58 | `1` → `Carla` → `2024003`, depois `2` | Nova usuária com ID 3 | |
| 59 | `10`, abrir o `biblioteca.json` num editor, apagar tudo e escrever `abc`, salvar, rodar `py app.py` | Mensagem "Erro ao ler o arquivo biblioteca.json..." e o programa fecha | |
| 60 | Apagar o `biblioteca.json` e rodar `py app.py` | "Nenhum arquivo encontrado. Biblioteca vazia." (começa do zero) | |

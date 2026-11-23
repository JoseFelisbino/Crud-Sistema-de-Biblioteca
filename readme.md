📚 Sistema de Biblioteca

Projeto simples em Python para gerenciamento de livros e empréstimos,
utilizando apenas dados em memória.
🧱 Entidades principais
📖 Livro

    Título
    Autor
    Ano
    Disponível

👤 Usuário

    Nome
    Matrícula

📑 Empréstimo

    Livro
    Usuário
    Data do empréstimo
    Data de devolução

✅ Funcionalidades obrigatórias

    📚 Listar livros cadastrados
    ➕ Cadastrar novo livro
    ✏️ Editar informações de um livro
    ❌ Remover livro
    👥 Cadastrar usuários
    👤 Listar usuários cadastrados
    📄 Listar livros emprestados por um usuário
    📦 Realizar empréstimo de livro
    🔄 Devolver livro
    🚫 Bloquear empréstimo se o livro não estiver disponível

✨ Funcionalidades adicionais (opcional)

    📅 Exibir histórico de empréstimos por usuário
    ⏳ Controlar prazo de devolução dos livros
    📋 Gravar em disco

🛠️ Tecnologias utilizadas

    🐍 Python 3 --- linguagem principal
    📦 Bibliotecas nativas apenas (sem dependências externas)

🎓 Avaliação

    🟢 Funcionalidades obrigatórias: nota base
    🟡 Funcionalidades adicionais: ponto bônus
    🛑 Requisitos obrigatórios não atendidos: ponto negativo
    ⚠️ Qualidade e clareza do código também serão avaliadas

💡 Dica

    👨‍💻 Use listas para armazenar dados em memória
    🏗️ Utilize classes para representar entidades (Livro, Usuário,
    Empréstimo)
    🔄 Use loops e condicionais para implementar o menu de opções

---

## ▶️ Como executar

É preciso ter o **Python 3** instalado. Não há nenhuma biblioteca externa para instalar.

Na pasta do projeto, rode:

```
py app.py
```

(ou `python app.py`, dependendo de como o Python foi instalado)

## 🧪 Como rodar os testes

Os testes automáticos usam o `unittest`, que já vem com o Python. Na pasta do projeto, rode:

```
py -m unittest discover tests -v
```

Os testes não mexem no arquivo `biblioteca.json` (usam um arquivo temporário).

Também existe um roteiro de testes manuais pelo menu em [tests/ROTEIRO_TESTES.md](tests/ROTEIRO_TESTES.md).

## 📁 Estrutura de pastas

```
app.py          -> menu principal no terminal
entity/         -> classes das entidades: Livro, Usuario e Emprestimo
service/        -> regras do sistema (cadastrar, listar, editar, emprestar, salvar...)
tests/          -> testes automáticos e roteiro de testes manuais
biblioteca.json -> arquivo com os dados salvos (criado automaticamente)
```

- `service/LivroService.py`: cadastrar, listar, buscar, editar e deletar livros, com validação dos dados.
- `service/UsuarioService.py`: cadastrar e listar usuários.
- `service/EmprestimoService.py`: realizar empréstimo, devolver livro e listar empréstimos.
- `service/PersistenciaService.py`: salvar e carregar os dados no arquivo `biblioteca.json`.

## 📋 Opções do menu

| Opção | O que faz |
|---|---|
| 1 - Cadastrar usuário | Pede nome e matrícula e cadastra o usuário |
| 2 - Listar usuários | Mostra todos os usuários com ID, nome e matrícula |
| 3 - Cadastrar Livro | Pede título, autor, ano e disponibilidade (true/false) e cadastra o livro. Recusa título/autor vazios e ano inválido |
| 4 - Listar Livros | Mostra todos os livros com ID, título, autor, ano e status (Disponível/Indisponível) |
| 5 - Editar Livro | Pede o ID e os novos dados. Apertar Enter mantém o valor atual. Não deixa mudar a disponibilidade de um livro emprestado |
| 6 - Deletar Livro | Remove o livro pelo ID. Não deixa remover um livro que já teve empréstimos |
| 7 - Realizar empréstimo | Escolhe o livro e o usuário pelo ID. Bloqueia o empréstimo se o livro estiver indisponível |
| 8 - Devolver livro | Mostra os empréstimos ativos e registra a devolução, deixando o livro disponível de novo |
| 9 - Listar empréstimos por usuários | Escolhe o usuário e mostra os livros emprestados agora (1) ou o histórico completo (2) |
| 10 - Sair | Encerra o programa |

## ✅ Funcionalidades implementadas

**Obrigatórias**

- [x] Listar livros cadastrados (opção 4)
- [x] Cadastrar novo livro (opção 3)
- [x] Editar informações de um livro (opção 5)
- [x] Remover livro (opção 6)
- [x] Cadastrar usuários (opção 1)
- [x] Listar usuários cadastrados (opção 2)
- [x] Listar livros emprestados por um usuário (opção 9 → 1)
- [x] Realizar empréstimo de livro (opção 7)
- [x] Devolver livro (opção 8)
- [x] Bloquear empréstimo se o livro não estiver disponível (opção 7)

**Adicionais (bônus)**

- [x] Exibir histórico de empréstimos por usuário (opção 9 → 2)
- [x] Gravar em disco (arquivo `biblioteca.json`)
- [ ] Controlar prazo de devolução dos livros (ainda não implementado)

**Extras**

- Validação dos dados do livro (título e autor vazios, ano com letras ou no futuro)
- Tratamento de entradas erradas no menu (letra no lugar de número, opção ou ID inexistente)
- Testes automáticos com `unittest`

## 💾 Dados salvos em disco

Os dados (livros, usuários e empréstimos) são salvos automaticamente no arquivo `biblioteca.json`
sempre que algo é cadastrado, editado, removido, emprestado ou devolvido.
Quando o programa é aberto de novo, os dados são carregados desse arquivo.

Para começar do zero, basta apagar o arquivo `biblioteca.json`.

## 👥 Divisão da equipe

| Integrante | Responsabilidade |
|---|---|
| Integrante 1 | Estrutura inicial do projeto e menu principal (`app.py`) |
| Integrante 2 | Usuários: classe `Usuario` e `UsuarioService` (cadastrar e listar) |
| Integrante 3 | Livros: classe `Livro` e `LivroService` (cadastrar, listar, editar, remover e validações) |
| Integrante 4 | Empréstimos: classe `Emprestimo`, realizar empréstimo e gravação em disco (`PersistenciaService`) |
| Integrante 5 | Devolução de livros e consultas de empréstimos/histórico por usuário |
| Integrante 6 | Qualidade e entrega: testes, conferência dos requisitos, revisão do código e README |

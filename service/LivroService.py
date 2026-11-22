from datetime import date

from entity.Livro import Livro


class LivroService:
    def __init__(self):
        self.lista = []

    # ---------- Validações ----------

    def _validar_texto(self, valor, campo):
        if valor is None or str(valor).strip() == "":
            raise ValueError(f"O campo {campo} não pode ficar vazio.")
        return str(valor).strip()

    def _validar_ano(self, ano):
        try:
            ano = int(str(ano).strip())
        except (ValueError, TypeError):
            raise ValueError("O ano deve ser um número inteiro.") from None

        ano_atual = date.today().year
        if ano < 1 or ano > ano_atual:
            raise ValueError(f"O ano deve estar entre 1 e {ano_atual}.")
        return ano

    def _converter_disponivel(self, disponivel):
        if isinstance(disponivel, bool):
            return disponivel
        if disponivel is None:
            return True

        texto = str(disponivel).strip().lower()
        if texto in ("", "true", "sim", "s"):
            return True
        if texto in ("false", "nao", "não", "n"):
            return False
        raise ValueError("Disponibilidade inválida. Digite true ou false.")

    # ---------- Cadastro e listagem ----------

    def cadastrar(self, titulo, autor, ano, disponivel=True):
        # Valida tudo antes de criar o livro, para não gastar um ID à toa
        titulo = self._validar_texto(titulo, "título")
        autor = self._validar_texto(autor, "autor")
        ano = self._validar_ano(ano)
        disponivel = self._converter_disponivel(disponivel)

        novo_livro = Livro(titulo, autor, ano, disponivel)
        self.lista.append(novo_livro)
        return novo_livro

    def listar(self):
        return self.lista

    def buscar_por_id(self, id_livro):
        for livro in self.lista:
            if livro.idLivro == id_livro:
                return livro
        return None

    # ---------- Edição ----------

    def editar(self, id_livro, titulo=None, autor=None, ano=None,
               disponivel=None, emprestimos=None):
        livro = self.buscar_por_id(id_livro)
        if livro is None:
            return None

        # Campos com None mantêm o valor atual.
        # Valida tudo antes de alterar, para o livro não ficar editado pela metade.
        if titulo is None:
            novo_titulo = livro.titulo
        else:
            novo_titulo = self._validar_texto(titulo, "título")

        if autor is None:
            novo_autor = livro.autor
        else:
            novo_autor = self._validar_texto(autor, "autor")

        if ano is None:
            novo_ano = livro.ano
        else:
            novo_ano = self._validar_ano(ano)

        if disponivel is None:
            novo_disponivel = livro.disponivel
        else:
            novo_disponivel = self._converter_disponivel(disponivel)

        if (novo_disponivel != livro.disponivel
                and self._possui_emprestimo_ativo(id_livro, emprestimos)):
            raise ValueError(
                "Este livro está emprestado. "
                "Registre a devolução para alterar a disponibilidade."
            )

        livro.titulo = novo_titulo
        livro.autor = novo_autor
        livro.ano = novo_ano
        livro.disponivel = novo_disponivel
        return livro

    def _possui_emprestimo_ativo(self, id_livro, emprestimos):
        if not emprestimos:
            return False
        for emprestimo in emprestimos:
            if (emprestimo.livro.idLivro == id_livro
                    and emprestimo.data_devolucao is None):
                return True
        return False

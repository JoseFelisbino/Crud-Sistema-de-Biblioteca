from datetime import date

from entity.Emprestimo import Emprestimo


class EmprestimoService:
    def __init__(self):
        self.lista = []

    def realizar_emprestimo(self, livro, usuario):
        if not livro.disponivel:
            return None, "Livro indisponível! Não é possível realizar o empréstimo."

        novo_emprestimo = Emprestimo(livro, usuario)
        livro.disponivel = False
        self.lista.append(novo_emprestimo)

        return novo_emprestimo, "Empréstimo realizado com sucesso!"

    def listar(self):
        return self.lista

    def listar_ativos(self):
        return [
            emprestimo for emprestimo in self.listar()
            if emprestimo.data_devolucao is None
        ]

    def devolver_livro(self, id_emprestimo):
        emprestimo = next(
            (e for e in self.listar() if e.idEmprestimo == id_emprestimo),
            None
        )

        if emprestimo is None:
            return False, "Empréstimo não encontrado."

        if emprestimo.data_devolucao is not None:
            return False, "Este empréstimo já foi devolvido."

        emprestimo.data_devolucao = date.today()
        emprestimo.livro.disponivel = True

        return True, "Livro devolvido com sucesso!"

    def listar_por_usuario(self, id_usuario):
        return [
            emprestimo for emprestimo in self.listar()
            if emprestimo.usuario.idUsuario == id_usuario
        ]

    def listar_ativos_por_usuario(self, id_usuario):
        return [
            emprestimo for emprestimo in self.listar_por_usuario(id_usuario)
            if emprestimo.data_devolucao is None
        ]
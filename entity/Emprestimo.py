from datetime import date


class Emprestimo:
    _contador_id = 1

    def __init__(self, livro, usuario):
        self.idEmprestimo = Emprestimo._contador_id
        Emprestimo._contador_id += 1

        self.livro = livro
        self.usuario = usuario
        self.data_emprestimo = date.today()
        self.data_devolucao = None

    def __str__(self):
        if self.data_devolucao is None:
            devolucao = "Ainda não devolvido"
        else:
            devolucao = self.data_devolucao.strftime("%d/%m/%Y")

        return (
            f"ID: {self.idEmprestimo}, Livro: {self.livro.titulo}, "
            f"Usuário: {self.usuario.nome}, "
            f"Data do empréstimo: {self.data_emprestimo.strftime('%d/%m/%Y')}, "
            f"Data de devolução: {devolucao}"
        )

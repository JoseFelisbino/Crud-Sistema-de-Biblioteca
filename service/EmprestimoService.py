from datetime import date

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
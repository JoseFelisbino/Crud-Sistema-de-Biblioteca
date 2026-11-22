class Livro:
    _contador_id = 1

    def __init__(self, titulo, autor, ano, disponivel=True):
        self.idLivro = Livro._contador_id
        Livro._contador_id += 1

        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = disponivel

    def __str__(self):
        status = "Disponível" if self.disponivel else "Indisponível"
        return (
            f"ID: {self.idLivro}, Título: {self.titulo}, "
            f"Autor: {self.autor}, Ano: {self.ano}, Status: {status}"
        )

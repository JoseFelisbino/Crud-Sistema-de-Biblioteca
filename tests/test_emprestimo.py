import unittest
from datetime import date

from entity.Livro import Livro
from entity.Usuario import Usuario
from entity.Emprestimo import Emprestimo
from service.LivroService import LivroService
from service.UsuarioService import UsuarioService
from service.EmprestimoService import EmprestimoService


class TestEmprestimo(unittest.TestCase):

    def setUp(self):
        Livro._contador_id = 1
        Usuario._contador_id = 1
        Emprestimo._contador_id = 1

        self.serviceLivro = LivroService()
        self.serviceUsuario = UsuarioService()
        self.serviceEmprestimo = EmprestimoService()

        self.livro = self.serviceLivro.cadastrar("Dom Casmurro", "Machado de Assis", "1899")
        self.usuario = self.serviceUsuario.cadastrar("Ana", "2024001")

    def test_empresta_livro_disponivel(self):
        emprestimo, mensagem = self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)

        self.assertIsNotNone(emprestimo)
        self.assertEqual(mensagem, "Empréstimo realizado com sucesso!")
        self.assertFalse(self.livro.disponivel)
        self.assertEqual(emprestimo.data_emprestimo, date.today())
        self.assertIsNone(emprestimo.data_devolucao)

    def test_nao_empresta_livro_indisponivel(self):
        self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)
        outro_usuario = self.serviceUsuario.cadastrar("Bruno", "2024002")

        emprestimo, mensagem = self.serviceEmprestimo.realizar_emprestimo(self.livro, outro_usuario)

        self.assertIsNone(emprestimo)
        self.assertIn("indisponível", mensagem)
        self.assertEqual(len(self.serviceEmprestimo.listar()), 1)

    def test_nao_empresta_livro_cadastrado_como_indisponivel(self):
        livro = self.serviceLivro.cadastrar("O Cortiço", "Aluísio Azevedo", "1890", "false")

        emprestimo, mensagem = self.serviceEmprestimo.realizar_emprestimo(livro, self.usuario)

        self.assertIsNone(emprestimo)

    def test_devolucao_libera_livro_e_registra_data(self):
        emprestimo, mensagem = self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)

        sucesso, mensagem = self.serviceEmprestimo.devolver_livro(emprestimo.idEmprestimo)

        self.assertTrue(sucesso)
        self.assertTrue(self.livro.disponivel)
        self.assertEqual(emprestimo.data_devolucao, date.today())

    def test_devolver_duas_vezes_da_erro(self):
        emprestimo, mensagem = self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)
        self.serviceEmprestimo.devolver_livro(emprestimo.idEmprestimo)

        sucesso, mensagem = self.serviceEmprestimo.devolver_livro(emprestimo.idEmprestimo)

        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "Este empréstimo já foi devolvido.")

    def test_devolver_emprestimo_inexistente_da_erro(self):
        sucesso, mensagem = self.serviceEmprestimo.devolver_livro(99)

        self.assertFalse(sucesso)
        self.assertEqual(mensagem, "Empréstimo não encontrado.")

    def test_livro_devolvido_pode_ser_emprestado_de_novo(self):
        emprestimo, mensagem = self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)
        self.serviceEmprestimo.devolver_livro(emprestimo.idEmprestimo)

        novo_emprestimo, mensagem = self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)

        self.assertIsNotNone(novo_emprestimo)
        self.assertEqual(novo_emprestimo.idEmprestimo, 2)

    def test_lista_apenas_emprestimos_ativos(self):
        livro2 = self.serviceLivro.cadastrar("O Cortiço", "Aluísio Azevedo", "1890")
        emprestimo1, mensagem = self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)
        emprestimo2, mensagem = self.serviceEmprestimo.realizar_emprestimo(livro2, self.usuario)
        self.serviceEmprestimo.devolver_livro(emprestimo1.idEmprestimo)

        ativos = self.serviceEmprestimo.listar_ativos()

        self.assertEqual(len(ativos), 1)
        self.assertEqual(ativos[0].idEmprestimo, emprestimo2.idEmprestimo)

    def test_historico_e_ativos_por_usuario(self):
        livro2 = self.serviceLivro.cadastrar("O Cortiço", "Aluísio Azevedo", "1890")
        outro_usuario = self.serviceUsuario.cadastrar("Bruno", "2024002")

        emprestimo1, mensagem = self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)
        self.serviceEmprestimo.devolver_livro(emprestimo1.idEmprestimo)
        self.serviceEmprestimo.realizar_emprestimo(livro2, self.usuario)
        self.serviceEmprestimo.realizar_emprestimo(self.livro, outro_usuario)

        historico_ana = self.serviceEmprestimo.listar_por_usuario(self.usuario.idUsuario)
        ativos_ana = self.serviceEmprestimo.listar_ativos_por_usuario(self.usuario.idUsuario)
        historico_bruno = self.serviceEmprestimo.listar_por_usuario(outro_usuario.idUsuario)

        self.assertEqual(len(historico_ana), 2)
        self.assertEqual(len(ativos_ana), 1)
        self.assertEqual(ativos_ana[0].livro.titulo, "O Cortiço")
        self.assertEqual(len(historico_bruno), 1)

    def test_nao_muda_disponibilidade_de_livro_emprestado(self):
        self.serviceEmprestimo.realizar_emprestimo(self.livro, self.usuario)

        with self.assertRaises(ValueError):
            self.serviceLivro.editar(1, disponivel="true", emprestimos=self.serviceEmprestimo.listar())


if __name__ == "__main__":
    unittest.main()

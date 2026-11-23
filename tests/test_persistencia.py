import os
import tempfile
import unittest
from datetime import date

from entity.Livro import Livro
from entity.Usuario import Usuario
from entity.Emprestimo import Emprestimo
from service.LivroService import LivroService
from service.UsuarioService import UsuarioService
from service.EmprestimoService import EmprestimoService
from service.PersistenciaService import PersistenciaService


class TestPersistencia(unittest.TestCase):

    def setUp(self):
        Livro._contador_id = 1
        Usuario._contador_id = 1
        Emprestimo._contador_id = 1

        # Usa um arquivo na pasta temporária para não mexer no biblioteca.json de verdade
        self.caminho = os.path.join(tempfile.gettempdir(), "teste_biblioteca.json")
        if os.path.exists(self.caminho):
            os.remove(self.caminho)

        self.persistencia = PersistenciaService(self.caminho)

    def tearDown(self):
        if os.path.exists(self.caminho):
            os.remove(self.caminho)

    def zerar_contadores(self):
        Livro._contador_id = 1
        Usuario._contador_id = 1
        Emprestimo._contador_id = 1

    def test_carregar_sem_arquivo_retorna_false(self):
        resultado = self.persistencia.carregar(LivroService(), UsuarioService(), EmprestimoService())

        self.assertFalse(resultado)

    def test_salva_e_carrega_os_mesmos_dados(self):
        serviceLivro = LivroService()
        serviceUsuario = UsuarioService()
        serviceEmprestimo = EmprestimoService()

        serviceLivro.cadastrar("Dom Casmurro", "Machado de Assis", "1899")
        livro2 = serviceLivro.cadastrar("O Cortiço", "Aluísio Azevedo", "1890")
        serviceLivro.cadastrar("Iracema", "José de Alencar", "1865")
        serviceLivro.deletar(1)
        usuario = serviceUsuario.cadastrar("Ana", "2024001")
        emprestimo, mensagem = serviceEmprestimo.realizar_emprestimo(livro2, usuario)
        serviceEmprestimo.devolver_livro(emprestimo.idEmprestimo)
        serviceEmprestimo.realizar_emprestimo(livro2, usuario)

        self.persistencia.salvar(serviceLivro, serviceUsuario, serviceEmprestimo)

        # Começa do zero, como se o programa tivesse sido fechado e aberto de novo
        self.zerar_contadores()
        novoServiceLivro = LivroService()
        novoServiceUsuario = UsuarioService()
        novoServiceEmprestimo = EmprestimoService()

        resultado = self.persistencia.carregar(novoServiceLivro, novoServiceUsuario, novoServiceEmprestimo)

        self.assertTrue(resultado)

        livros = novoServiceLivro.listar()
        self.assertEqual(len(livros), 2)
        self.assertEqual(livros[0].idLivro, 2)
        self.assertEqual(livros[0].titulo, "O Cortiço")
        self.assertFalse(livros[0].disponivel)
        self.assertEqual(livros[1].idLivro, 3)
        self.assertEqual(livros[1].ano, 1865)

        usuarios = novoServiceUsuario.listar()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].idUsuario, 1)
        self.assertEqual(usuarios[0].matricula, "2024001")

        emprestimos = novoServiceEmprestimo.listar()
        self.assertEqual(len(emprestimos), 2)
        self.assertEqual(emprestimos[0].idEmprestimo, 1)
        self.assertEqual(emprestimos[0].data_emprestimo, date.today())
        self.assertEqual(emprestimos[0].data_devolucao, date.today())
        self.assertEqual(emprestimos[1].idEmprestimo, 2)
        self.assertIsNone(emprestimos[1].data_devolucao)
        self.assertEqual(emprestimos[1].livro.titulo, "O Cortiço")
        self.assertEqual(emprestimos[1].usuario.nome, "Ana")

    def test_novos_ids_continuam_depois_de_carregar(self):
        serviceLivro = LivroService()
        serviceUsuario = UsuarioService()
        serviceEmprestimo = EmprestimoService()
        serviceLivro.cadastrar("Dom Casmurro", "Machado de Assis", "1899")
        serviceLivro.cadastrar("O Cortiço", "Aluísio Azevedo", "1890")
        serviceUsuario.cadastrar("Ana", "2024001")
        self.persistencia.salvar(serviceLivro, serviceUsuario, serviceEmprestimo)

        self.zerar_contadores()
        novoServiceLivro = LivroService()
        novoServiceUsuario = UsuarioService()
        self.persistencia.carregar(novoServiceLivro, novoServiceUsuario, EmprestimoService())

        livro_novo = novoServiceLivro.cadastrar("Iracema", "José de Alencar", "1865")
        usuario_novo = novoServiceUsuario.cadastrar("Bruno", "2024002")

        self.assertEqual(livro_novo.idLivro, 3)
        self.assertEqual(usuario_novo.idUsuario, 2)

    def test_arquivo_corrompido_da_erro(self):
        with open(self.caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write("isso nao e um json")

        with self.assertRaises(RuntimeError):
            self.persistencia.carregar(LivroService(), UsuarioService(), EmprestimoService())


if __name__ == "__main__":
    unittest.main()

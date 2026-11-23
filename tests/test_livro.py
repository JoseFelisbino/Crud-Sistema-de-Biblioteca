import unittest
from datetime import date

from entity.Livro import Livro
from service.LivroService import LivroService


class TestLivro(unittest.TestCase):

    def setUp(self):
        Livro._contador_id = 1
        self.service = LivroService()

    def test_cadastra_livro_valido(self):
        livro = self.service.cadastrar("Dom Casmurro", "Machado de Assis", "1899")

        self.assertEqual(livro.idLivro, 1)
        self.assertEqual(livro.titulo, "Dom Casmurro")
        self.assertEqual(livro.autor, "Machado de Assis")
        self.assertEqual(livro.ano, 1899)
        self.assertTrue(livro.disponivel)
        self.assertEqual(len(self.service.listar()), 1)

    def test_titulo_vazio_da_erro(self):
        with self.assertRaises(ValueError):
            self.service.cadastrar("   ", "Machado de Assis", "1899")

        self.assertEqual(len(self.service.listar()), 0)

    def test_ano_com_letras_da_erro(self):
        with self.assertRaises(ValueError):
            self.service.cadastrar("Dom Casmurro", "Machado de Assis", "abc")

    def test_ano_no_futuro_da_erro(self):
        ano_futuro = date.today().year + 1

        with self.assertRaises(ValueError):
            self.service.cadastrar("Livro do Futuro", "Autor", str(ano_futuro))

    def test_editar_mantem_campos_em_branco(self):
        self.service.cadastrar("Dom Casmurro", "Machado de Assis", "1899")

        livro = self.service.editar(1, titulo="Memórias Póstumas")

        self.assertEqual(livro.titulo, "Memórias Póstumas")
        self.assertEqual(livro.autor, "Machado de Assis")
        self.assertEqual(livro.ano, 1899)
        self.assertTrue(livro.disponivel)

    def test_editar_livro_inexistente_retorna_none(self):
        resultado = self.service.editar(99, titulo="Qualquer")

        self.assertIsNone(resultado)

    def test_deletar_livro_existente(self):
        self.service.cadastrar("Dom Casmurro", "Machado de Assis", "1899")

        resultado = self.service.deletar(1)

        self.assertTrue(resultado)
        self.assertEqual(len(self.service.listar()), 0)

    def test_deletar_livro_inexistente(self):
        resultado = self.service.deletar(99)

        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()

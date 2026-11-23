import unittest

from entity.Usuario import Usuario
from service.UsuarioService import UsuarioService


class TestUsuario(unittest.TestCase):

    def setUp(self):
        Usuario._contador_id = 1
        self.service = UsuarioService()

    def test_cadastra_usuario(self):
        usuario = self.service.cadastrar("Ana", "2024001")

        self.assertEqual(usuario.idUsuario, 1)
        self.assertEqual(usuario.nome, "Ana")
        self.assertEqual(usuario.matricula, "2024001")

    def test_lista_usuarios_cadastrados(self):
        self.service.cadastrar("Ana", "2024001")
        self.service.cadastrar("Bruno", "2024002")

        usuarios = self.service.listar()

        self.assertEqual(len(usuarios), 2)
        self.assertEqual(usuarios[0].nome, "Ana")
        self.assertEqual(usuarios[1].nome, "Bruno")
        self.assertEqual(usuarios[1].idUsuario, 2)

    def test_lista_vazia_quando_nao_ha_usuarios(self):
        self.assertEqual(self.service.listar(), [])


if __name__ == "__main__":
    unittest.main()

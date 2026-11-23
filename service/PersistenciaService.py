import json
import os
from datetime import date

from entity.Livro import Livro
from entity.Usuario import Usuario
from entity.Emprestimo import Emprestimo


class PersistenciaService:
    def __init__(self, arquivo="biblioteca.json"):
        self.arquivo = arquivo

    def salvar(self, serviceLivro, serviceUsuario, serviceEmprestimo):
        livros = []
        for livro in serviceLivro.listar():
            livros.append({
                "id": livro.idLivro,
                "titulo": livro.titulo,
                "autor": livro.autor,
                "ano": livro.ano,
                "disponivel": livro.disponivel
            })

        usuarios = []
        for usuario in serviceUsuario.listar():
            usuarios.append({
                "id": usuario.idUsuario,
                "nome": usuario.nome,
                "matricula": usuario.matricula
            })

        emprestimos = []
        for emprestimo in serviceEmprestimo.listar():
            if emprestimo.data_devolucao is None:
                data_devolucao = None
            else:
                data_devolucao = emprestimo.data_devolucao.isoformat()

            emprestimos.append({
                "id": emprestimo.idEmprestimo,
                "id_livro": emprestimo.livro.idLivro,
                "id_usuario": emprestimo.usuario.idUsuario,
                "data_emprestimo": emprestimo.data_emprestimo.isoformat(),
                "data_devolucao": data_devolucao
            })

        dados = {
            "livros": livros,
            "usuarios": usuarios,
            "emprestimos": emprestimos
        }

        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def carregar(self, serviceLivro, serviceUsuario, serviceEmprestimo):
        if not os.path.exists(self.arquivo):
            return False

        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados["livros"]:
                livro = Livro(item["titulo"], item["autor"], item["ano"], item["disponivel"])
                livro.idLivro = item["id"]
                serviceLivro.lista.append(livro)

            for item in dados["usuarios"]:
                usuario = Usuario(item["nome"], item["matricula"])
                usuario.idUsuario = item["id"]
                serviceUsuario.lista.append(usuario)

            for item in dados["emprestimos"]:
                livro = serviceLivro.buscar_por_id(item["id_livro"])
                usuario = None
                for u in serviceUsuario.listar():
                    if u.idUsuario == item["id_usuario"]:
                        usuario = u

                emprestimo = Emprestimo(livro, usuario)
                emprestimo.idEmprestimo = item["id"]
                emprestimo.data_emprestimo = date.fromisoformat(item["data_emprestimo"])
                if item["data_devolucao"] is not None:
                    emprestimo.data_devolucao = date.fromisoformat(item["data_devolucao"])
                serviceEmprestimo.lista.append(emprestimo)

        except (json.JSONDecodeError, KeyError, ValueError):
            raise RuntimeError(
                f"Erro ao ler o arquivo {self.arquivo}. "
                "Verifique o arquivo ou apague ele para começar do zero."
            )

        # Os contadores de ID continuam a partir do maior ID salvo
        Livro._contador_id = self._proximo_id([l.idLivro for l in serviceLivro.listar()])
        Usuario._contador_id = self._proximo_id([u.idUsuario for u in serviceUsuario.listar()])
        Emprestimo._contador_id = self._proximo_id(
            [e.idEmprestimo for e in serviceEmprestimo.listar()]
        )

        return True

    def _proximo_id(self, ids):
        if not ids:
            return 1
        return max(ids) + 1

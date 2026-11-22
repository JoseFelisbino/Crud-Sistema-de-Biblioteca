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

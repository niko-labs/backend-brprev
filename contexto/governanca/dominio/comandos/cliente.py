from datetime import datetime

from pydantic import EmailStr

from contexto.governanca.dominio.objeto_de_valor.cliente import Genero
from libs.ddd.comando import Comando


class CriarCliente(Comando):
    cpf: str
    nome: str
    email: EmailStr
    genero: Genero
    renda_mensal: float
    data_de_nascimento: datetime

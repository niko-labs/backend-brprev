from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, field_validator
from validate_docbr import CPF

from contexto.governanca.dominio.objeto_de_valor.cliente import Genero
from libs.fastapi.camelcase import Modelo


class EntradaCriarCliente(Modelo):
    cpf: str
    nome: str
    email: EmailStr
    genero: Genero
    renda_mensal: float
    data_de_nascimento: datetime

    @field_validator("cpf")
    def check_cpf(cls, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise ValueError("CPF inválido")
        return value


class SaidaCliente(Modelo):
    id: UUID
    cpf: str
    nome: str
    email: str
    genero: Genero
    renda_mensal: float
    data_de_nascimento: datetime

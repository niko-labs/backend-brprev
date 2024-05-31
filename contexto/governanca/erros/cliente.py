from dataclasses import dataclass

from libs.fastapi.exception import ExceptionBase


@dataclass
class ErroAoCriarCliente(ExceptionBase):
    detail = "Erro durante a criação do cliente."
    status_code = 500


@dataclass
class ErroClienteNaoEncontrado(ExceptionBase):
    detail = "Cliente não encontrado."
    status_code = 404

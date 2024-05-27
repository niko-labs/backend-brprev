from uuid import UUID

from contexto.governanca.dominio.entidades.cliente import Cliente
from contexto.governanca.erros.cliente import ErroClienteNaoEncontrado
from contexto.governanca.repositorios.repos.cliente import RepoCliente
from libs.ddd.uow import UoW


def vizualizador_buscar_cliente_por_id(id_cliente: UUID, uow: UoW) -> Cliente:
    with uow:
        repo = RepoCliente(uow.session)

        cliente = repo.buscar_por_id(id_cliente)
        if not cliente:
            raise ErroClienteNaoEncontrado()

    return cliente

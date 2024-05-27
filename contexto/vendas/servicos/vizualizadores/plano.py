from typing import Optional
from uuid import UUID

from contexto.vendas.dominio.entidades.plano import Plano
from contexto.vendas.erros.plano import (
    ErroPlanoNaoEncontrado,
)
from contexto.vendas.repositorios.repos.cliente import RepoPlano
from libs.ddd.uow import UoW


def vizualizador_buscar_plano_por_id(id: UUID, uow: UoW) -> Plano:
    with uow:
        repo = RepoPlano(uow.session)

        plano: Optional[Plano] = repo.buscar_plano_por_id(id)
        if not plano:
            raise ErroPlanoNaoEncontrado()

    return plano

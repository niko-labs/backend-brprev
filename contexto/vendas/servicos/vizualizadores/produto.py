from typing import Optional
from uuid import UUID

from contexto.vendas.dominio.entidades.produto import Produto
from contexto.vendas.erros.produto import ErroProdutoNaoEncontrado
from contexto.vendas.repositorios.repos.produto import RepoProduto
from libs.ddd.uow import UoW


def vizualizador_buscar_produto_por_id(id: UUID, uow: UoW) -> Produto:
    with uow:
        repo = RepoProduto(uow.session)

        produto: Optional[Produto] = repo.buscar_produto_por_id(id)
        if not produto:
            raise ErroProdutoNaoEncontrado()

    return produto

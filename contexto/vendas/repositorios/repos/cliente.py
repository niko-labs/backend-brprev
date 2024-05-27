from typing import Optional
from uuid import UUID

from sqlalchemy.orm.session import Session

from contexto.governanca.dominio.entidades.cliente import Cliente
from contexto.vendas.dominio.entidades.plano import Plano
from contexto.vendas.dominio.entidades.produto import Produto
from libs.ddd.repositorio import Repositorio


class RepoPlano(Repositorio):
    sql_session: Session

    def criar(self, instancia: Plano) -> Plano:
        self.sql_session.add(instancia)
        return instancia

    def buscar_cliente_por_id(self, id: UUID) -> Optional[Cliente]:
        return self.sql_session.query(Cliente).filter(Cliente.id == id).first()

    def buscar_produto_por_id(self, id: UUID) -> Optional[Produto]:
        return self.sql_session.query(Produto).filter(Produto.id == id).first()

    def buscar_plano_por_id(self, id: UUID) -> Optional[Plano]:
        return self.sql_session.query(Plano).filter(Plano.id == id).first()

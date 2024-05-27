from typing import Optional
from uuid import UUID

from sqlalchemy.orm.session import Session

from contexto.governanca.dominio.entidades.cliente import Cliente
from libs.ddd.repositorio import Repositorio


class RepoCliente(Repositorio):
    sql_session: Session

    def criar(self, instancia: Cliente) -> Cliente:
        self.sql_session.add(instancia)
        return instancia

    def buscar_por_id(self, id_cliente: UUID) -> Optional[Cliente]:
        return self.sql_session.query(Cliente).filter(Cliente.id == id_cliente).first()

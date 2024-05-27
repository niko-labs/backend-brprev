from sqlalchemy.orm.session import Session

from contexto.vendas.dominio.entidades.produto import Produto
from libs.ddd.repositorio import Repositorio


class RepoProduto(Repositorio):
    sql_session: Session

    def criar(self, instancia: Produto) -> Produto:
        self.sql_session.add(instancia)
        return instancia

    def buscar_produto_por_id(self, id: str) -> Produto:
        return self.sql_session.query(Produto).filter(Produto.id == id).first()

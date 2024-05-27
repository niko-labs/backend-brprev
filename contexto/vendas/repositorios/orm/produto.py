import sqlalchemy as sa
from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import UUID

from contexto.vendas.dominio.entidades.produto import Produto
from libs.orm.sqlalchemy import metadata, orm_registry

tabela_produto = Table(
    "produtos",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("nome", sa.String, nullable=False),
    Column("susep", sa.String, nullable=False),
    Column("expiracao_da_venda", sa.Date, nullable=False),
    Column(
        "valor_minimo_aporte_inicial", sa.Numeric(precision=10, scale=2), nullable=False
    ),
    Column(
        "valor_minimo_aporte_extra", sa.Numeric(precision=10, scale=2), nullable=False
    ),
    Column("idade_de_entrada", sa.Integer, nullable=False),
    Column("idade_de_saida", sa.Integer, nullable=False),
    Column("carencia_inicial_de_resgate", sa.Integer, nullable=False),
    Column("carencia_entre_resgates", sa.Integer, nullable=False),
    #
    # CONFIGURACAO DE CHAVES E INDICES E CONSTRAINTS
    sa.Index("ix_planos_susep", "susep", unique=True),
    sa.Index("ix_planos_expiracao_da_venda", "expiracao_da_venda", unique=True),
    sa.CheckConstraint(
        "valor_minimo_aporte_inicial >= 0", name="ck_planos_valor_minimo_aporte_inicial"
    ),
    sa.CheckConstraint(
        "valor_minimo_aporte_extra >= 0", name="ck_planos_valor_minimo_aporte_extra"
    ),
    sa.CheckConstraint("idade_de_entrada > 0", name="ck_planos_idade_de_entrada"),
    sa.CheckConstraint("idade_de_saida > 0", name="ck_planos_idade_de_saida"),
    sa.CheckConstraint(
        "carencia_inicial_de_resgate >= 0", name="ck_planos_carencia_inicial_de_resgate"
    ),
    sa.CheckConstraint(
        "carencia_entre_resgates >= 0", name="ck_planos_carencia_entre_resgates"
    ),
)


orm_registry.map_imperatively(Produto, tabela_produto)

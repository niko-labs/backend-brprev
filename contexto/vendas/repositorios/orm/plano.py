import sqlalchemy as sa
from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import UUID

from contexto.vendas.dominio.entidades.plano import Plano
from libs.orm.sqlalchemy import metadata, orm_registry

tabela_plano = Table(
    "plano",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("id_produto", UUID, nullable=False),
    Column("id_cliente", UUID, nullable=False),
    Column("aporte", sa.Numeric(precision=10, scale=2), nullable=False),
    Column("data_da_contratacao", sa.Date, nullable=False),
    Column("idade_de_aposentadoria", sa.Integer, nullable=False),
    Column("ultimo_resgate", sa.Date, nullable=True),
    Column("plano_finalizado", sa.Boolean, nullable=False),
    #
    # CONFIGURACAO DE CHAVES E INDICES E CONSTRAINTS
    sa.ForeignKeyConstraint(["id_produto"], ["produtos.id"]),
    sa.ForeignKeyConstraint(["id_cliente"], ["clientes.id"]),
    sa.Index("ix_produtos_id_produto", "id_produto", unique=True),
    sa.Index("ix_produtos_id_cliente", "id_cliente", unique=True),
    sa.Index("ix_produtos_data_da_contratacao", "data_da_contratacao", unique=True),
    sa.Index(
        "ix_produtos_idade_de_aposentadoria", "idade_de_aposentadoria", unique=True
    ),
    sa.CheckConstraint("aporte >= 0", name="ck_produtos_aporte"),
    sa.CheckConstraint("idade_de_aposentadoria > 0", name="ck_idade_de_aposentadoria"),
)


orm_registry.map_imperatively(Plano, tabela_plano)

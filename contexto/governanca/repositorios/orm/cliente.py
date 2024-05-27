import sqlalchemy as sa
from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from contexto.governanca.dominio.entidades.cliente import Cliente
from contexto.governanca.dominio.objeto_de_valor.cliente import Genero
from contexto.vendas.dominio.entidades.plano import Plano
from contexto.vendas.repositorios.orm.plano import tabela_plano
from libs.orm.sqlalchemy import metadata, orm_registry

tabela_clientes = Table(
    "clientes",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("cpf", sa.String(11), nullable=False, unique=True),
    Column("nome", sa.String(96), nullable=False),
    Column("email", sa.String(256), nullable=False, unique=True),
    Column("genero", sa.Enum(Genero), nullable=False),
    Column("renda_mensal", sa.Numeric(10, 2), nullable=False),
    Column("data_de_nascimento", sa.Date, nullable=False),
    #
    # CONFIGURACAO DE CHAVES E INDICES E CONSTRAINTS
    sa.Index("ix_clientes_cpf", "cpf", unique=True),
    sa.Index("ix_clientes_email", "email", unique=True),
    sa.Index("ix_clientes_email_genero", "email", "genero", unique=True),
)


orm_registry.map_imperatively(
    Cliente,
    tabela_clientes,
    properties={
        "planos_contratados": relationship(
            Plano, foreign_keys=[tabela_plano.c.id_cliente]
        ),
    },
)

from datetime import datetime
from uuid import UUID

from contexto.governanca.dominio.objeto_de_valor.cliente import ClienteID
from contexto.vendas.dominio.objeto_de_valor.produto import ProdutoID
from libs.ddd.comando import Comando


class CriarPlano(Comando):
    id_cliente: UUID
    id_produto: UUID

    aporte: float

    data_da_contratacao: datetime
    idade_de_aposentadoria: int


class RealizaAporteExtraNoPlano(Comando):
    id_plano: UUID
    id_cliente: UUID
    valor_aporte: float


class RealizarResgateDoPlano(Comando):
    id_plano: UUID
    valor_resgate: float

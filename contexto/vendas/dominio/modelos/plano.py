from datetime import datetime
from uuid import UUID

from libs.fastapi.camelcase import Modelo


class EntradaCriarPlano(Modelo):
    id_cliente: UUID
    id_produto: UUID

    aporte: float

    data_da_contratacao: datetime
    idade_de_aposentadoria: int


class EntradaRealizarAporteExtra(Modelo):
    id_cliente: UUID
    id_plano: UUID
    valor_aporte: float


class EntradaRealizarResgate(Modelo):
    id_plano: UUID
    valor_resgate: float

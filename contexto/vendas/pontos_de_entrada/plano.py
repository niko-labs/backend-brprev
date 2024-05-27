from uuid import UUID

from fastapi.routing import APIRouter

from contexto.vendas.dominio.comandos.plano import (
    CriarPlano,
    RealizaAporteExtraNoPlano,
    RealizarResgateDoPlano,
)
from contexto.vendas.dominio.modelos.plano import (
    EntradaCriarPlano,
    EntradaRealizarAporteExtra,
    EntradaRealizarResgate,
)
from libs.ddd.barramento import Barramento
from libs.ddd.uow import UoW
from libs.pydantic.apenas_id import RetornoApenasId

rota = APIRouter(tags=["Plano"])


@rota.post("/plano", status_code=201)
def criar_plano(entrada: EntradaCriarPlano) -> RetornoApenasId[UUID]:
    uow = UoW()
    barramento = Barramento()

    comando = CriarPlano(
        aporte=entrada.aporte,
        id_produto=entrada.id_produto,
        id_cliente=entrada.id_cliente,
        data_da_contratacao=entrada.data_da_contratacao,
        idade_de_aposentadoria=entrada.idade_de_aposentadoria,
    )
    retorno_comando = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


@rota.post("/plano/aporte-extra", status_code=200)
def realizar_aporte_extra(entrada: EntradaRealizarAporteExtra) -> RetornoApenasId[UUID]:
    uow = UoW()
    barramento = Barramento()

    comando = RealizaAporteExtraNoPlano(
        id_plano=entrada.id_plano,
        id_cliente=entrada.id_cliente,
        valor_aporte=entrada.valor_aporte,
    )
    retorno_comando = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


@rota.post("/plano/resgate", status_code=200)
def realizar_resgate(entrada: EntradaRealizarResgate) -> RetornoApenasId[UUID]:
    uow = UoW()
    barramento = Barramento()

    comando = RealizarResgateDoPlano(
        id_plano=entrada.id_plano,
        valor_resgate=entrada.valor_resgate,
    )
    retorno_comando = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)

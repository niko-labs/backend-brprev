from uuid import UUID

from fastapi.routing import APIRouter

from contexto.governanca.dominio.comandos.cliente import CriarCliente
from contexto.governanca.dominio.entidades.cliente import Cliente
from contexto.governanca.dominio.modelos.cliente import (
    EntradaCriarCliente,
    SaidaCliente,
)
from contexto.governanca.servicos.vizualizadores.cliente import (
    vizualizador_buscar_cliente_por_id,
)
from libs.ddd.barramento import Barramento
from libs.ddd.uow import UoW
from libs.pydantic.apenas_id import RetornoApenasId, RetornoDado

rota = APIRouter(tags=["Cliente"])


@rota.post("/cliente", status_code=201)
def criar_cliente(entrada: EntradaCriarCliente) -> RetornoApenasId[UUID]:
    uow = UoW()
    barramento = Barramento()

    comando = CriarCliente(
        cpf=entrada.cpf,
        nome=entrada.nome,
        email=entrada.email,
        genero=entrada.genero,
        renda_mensal=entrada.renda_mensal,
        data_de_nascimento=entrada.data_de_nascimento,
    )
    retorno_comando: Cliente = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


@rota.get("/cliente/{id_cliente}")
def buscar_cliente_por_id(id_cliente: UUID) -> RetornoDado[SaidaCliente]:
    uow = UoW()

    cliente: Cliente = vizualizador_buscar_cliente_por_id(id_cliente, uow)

    return RetornoDado(
        dado=SaidaCliente(
            id=cliente.id,
            cpf=cliente.cpf,
            nome=cliente.nome,
            data_de_nascimento=cliente.data_de_nascimento,
            email=cliente.email,
            genero=cliente.genero,
            renda_mensal=cliente.renda_mensal,
        )
    )

from uuid import UUID

from fastapi.routing import APIRouter

from contexto.vendas.dominio.comandos.produto import CriarProduto
from contexto.vendas.dominio.entidades.produto import Produto
from contexto.vendas.dominio.modelos.produto import EntradaCriarProduto, SaidaProduto
from contexto.vendas.servicos.vizualizadores.produto import (
    vizualizador_buscar_produto_por_id,
)
from libs.ddd.barramento import Barramento
from libs.ddd.uow import UoW
from libs.pydantic.apenas_id import RetornoApenasId, RetornoDado

rota = APIRouter(tags=["Produto"])


@rota.post("/produto", status_code=201)
def criar_produto(entrada: EntradaCriarProduto) -> RetornoApenasId[UUID]:
    uow = UoW()
    barramento = Barramento()

    comando = CriarProduto(
        nome=entrada.nome,
        susep=entrada.susep,
        idade_de_saida=entrada.idade_de_saida,
        idade_de_entrada=entrada.idade_de_entrada,
        expiracao_da_venda=entrada.expiracao_da_venda,
        carencia_entre_resgates=entrada.carencia_entre_resgates,
        valor_minimo_aporte_extra=entrada.valor_minimo_aporte_extra,
        valor_minimo_aporte_inicial=entrada.valor_minimo_aporte_inicial,
        carencia_inicial_de_resgate=entrada.carencia_inicial_de_resgate,
    )
    retorno_comando = barramento.enviar_comando(comando, uow)

    return RetornoApenasId(id=retorno_comando.id)


@rota.get("/produto/{id_produto}")
def buscar_produto_por_id(id_produto: UUID) -> RetornoDado[SaidaProduto]:
    uow = UoW()

    produto: Produto = vizualizador_buscar_produto_por_id(id_produto, uow)

    return RetornoDado(
        dado=SaidaProduto(
            id=produto.id,
            nome=produto.nome,
            carencia_entre_resgates=produto.carencia_entre_resgates,
            carencia_inicial_de_resgate=produto.carencia_inicial_de_resgate,
            expiracao_da_venda=produto.expiracao_da_venda,
            idade_de_entrada=produto.idade_de_entrada,
            idade_de_saida=produto.idade_de_saida,
            susep=produto.susep,
            valor_minimo_aporte_extra=produto.valor_minimo_aporte_extra,
            valor_minimo_aporte_inicial=produto.valor_minimo_aporte_inicial,
        )
    )

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from libs.orm.caregar_orm import carregar_orm

app = FastAPI(
    title="API",
    description="API com FastAPI, SQLAlchemy e Pydantic, PostgreSQL, Docker, DDD, TDD, UoW, CQRS, EventBus, Swagger",
    version="1.0.0",
)


@app.middleware("http")
async def tempo_de_resposta(request, call_next):
    import time

    inicio = time.time()
    response = await call_next(request)
    duracao = time.time() - inicio
    response.headers["X-Response-Time"] = str(duracao)
    return response


# Rota de health check
@app.get("/health-check", tags=["HELPERS"], include_in_schema=False)
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


# Redirect para a documentação
@app.get("/", tags=["HELPERS"], include_in_schema=False)
async def redirect_para_docs() -> dict[str, str]:
    return RedirectResponse(url="/docs")


def registrar_comandos_e_eventos() -> None:
    from contexto.governanca.dominio.comandos.cliente import CriarCliente
    from contexto.governanca.servicos.executores.cliente import criar_cliente
    from contexto.vendas.dominio.comandos.plano import (
        CriarPlano,
        RealizaAporteExtraNoPlano,
        RealizarResgateDoPlano,
    )
    from contexto.vendas.dominio.comandos.produto import CriarProduto
    from contexto.vendas.servicos.executores.plano import (
        criar_plano,
        realizar_aporte_extra_plano,
        realizar_resgate_do_plano,
    )
    from contexto.vendas.servicos.executores.produto import criar_produto
    from libs.ddd.barramento import Barramento

    barramento = Barramento()
    barramento.registrar_comando(CriarCliente, criar_cliente)
    barramento.registrar_comando(CriarProduto, criar_produto)
    barramento.registrar_comando(CriarPlano, criar_plano)
    barramento.registrar_comando(RealizaAporteExtraNoPlano, realizar_aporte_extra_plano)
    barramento.registrar_comando(RealizarResgateDoPlano, realizar_resgate_do_plano)


def registrar_rotas() -> None:
    from contexto.governanca.pontos_de_entrada.cliente import rota as rota_cliente
    from contexto.vendas.pontos_de_entrada.plano import rota as rota_plano
    from contexto.vendas.pontos_de_entrada.produto import rota as rota_produto

    app.include_router(rota_cliente)
    app.include_router(rota_produto)
    app.include_router(rota_plano)


registrar_comandos_e_eventos()
registrar_rotas()
carregar_orm()

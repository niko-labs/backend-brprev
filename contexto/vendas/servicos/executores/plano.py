from typing import Optional
from uuid import UUID

from contexto.governanca.dominio.entidades.cliente import Cliente
from contexto.governanca.erros.cliente import ErroClienteNaoEncontrado
from contexto.vendas.dominio.comandos.plano import (
    CriarPlano,
    RealizaAporteExtraNoPlano,
    RealizarResgateDoPlano,
)
from contexto.vendas.dominio.entidades.plano import Plano
from contexto.vendas.dominio.entidades.produto import Produto
from contexto.vendas.erros.plano import (
    ErroAoCriarPlano,
    ErroAoResgatarPlano,
    ErroPlanoJaFoiFinalizado,
    ErroPlanoNaoEncontrado,
    ErroPlanoSendoResgatadoAntesDoPeridoDeCarencia,
    ErroPlanoSendoResgatadoAntesDoPeridoDeCarenciaEntreResgates,
)
from contexto.vendas.erros.produto import (
    ErroProdutoComIdadeDeEntradaMaiorQueAIdadeDoCliente,
    ErroProdutoComIdadeDeSaidaMaiorQueAIdadeDoCliente,
    ErroProdutoExpirado,
    ErroProdutoNaoEncontrado,
    ErroProdutoNaoTeveValorDoAporteMinimoAtingido,
)
from contexto.vendas.repositorios.repos.cliente import RepoPlano
from libs.ddd.uow import UoW


def criar_plano(comando: CriarPlano, uow: UoW):
    with uow:
        repo = RepoPlano(uow.session)
        produto: Optional[Produto] = repo.buscar_produto_por_id(comando.id_produto)

        # Validações: Produto
        if not produto:
            raise ErroProdutoNaoEncontrado()
        if produto.produto_esta_expirado():
            raise ErroProdutoExpirado()
        if not produto.pode_realizar_aporte(comando.aporte):
            raise ErroProdutoNaoTeveValorDoAporteMinimoAtingido()

        # Validações: Cliente
        cliente: Optional[Cliente] = repo.buscar_cliente_por_id(comando.id_cliente)
        if not cliente:
            raise ErroClienteNaoEncontrado

        if not produto.idade_do_cliente_de_entrada_eh_valida(cliente.idade):
            raise ErroProdutoComIdadeDeEntradaMaiorQueAIdadeDoCliente

        if not produto.idade_do_cliente_de_saida_eh_valida(cliente.idade):
            raise ErroProdutoComIdadeDeSaidaMaiorQueAIdadeDoCliente

        # Criação do plano
        plano = Plano.criar(
            aporte=comando.aporte,
            id_cliente=comando.id_cliente,
            id_produto=comando.id_produto,
            data_da_contratacao=comando.data_da_contratacao,
            idade_de_aposentadoria=comando.idade_de_aposentadoria,
        )

        try:
            repo.criar(plano)
            uow.commit()
        except Exception as e:
            uow.rollback()
            raise ErroAoCriarPlano from e

    return plano


def realizar_aporte_extra_plano(comando: RealizaAporteExtraNoPlano, uow: UoW):
    with uow:
        repo = RepoPlano(uow.session)
        cliente: Optional[Cliente] = repo.buscar_cliente_por_id(comando.id_cliente)

        if not cliente:
            raise ErroClienteNaoEncontrado()

        plano = filtrar_plano_do_cliente(comando.id_plano, cliente)
        if not plano:
            raise ErroPlanoNaoEncontrado()

        if plano.plano_finalizado:
            raise ErroPlanoJaFoiFinalizado()

        produto: Optional[Produto] = repo.buscar_produto_por_id(plano.id_produto)
        if not produto:
            raise ErroProdutoNaoEncontrado()

        if not produto.pode_realizar_aporte_extra(comando.valor_aporte):
            raise ErroProdutoNaoTeveValorDoAporteMinimoAtingido()

        plano.realizar_aporte_extra(comando.valor_aporte)

        uow.adicionar(plano)
        uow.commit()

    return plano


def realizar_resgate_do_plano(comando: RealizarResgateDoPlano, uow: UoW):
    with uow:
        repo = RepoPlano(uow.session)

        plano: Optional[Plano] = repo.buscar_plano_por_id(comando.id_plano)
        if not plano:
            raise ErroPlanoNaoEncontrado()

        if plano.plano_finalizado:
            raise ErroPlanoJaFoiFinalizado()

        produto: Optional[Produto] = repo.buscar_produto_por_id(plano.id_produto)
        if not produto:
            raise ErroProdutoNaoEncontrado()

        if not produto.carencia_inicial_de_resgate < plano.dias_desde_contratacao:
            raise ErroPlanoSendoResgatadoAntesDoPeridoDeCarencia()

        if (
            plano.dias_desde_ultimo_resgate is not None
            and not produto.carencia_entre_resgates <= plano.dias_desde_ultimo_resgate
        ):
            raise ErroPlanoSendoResgatadoAntesDoPeridoDeCarenciaEntreResgates()

        plano.realizar_resgate(comando.valor_resgate)

        try:
            uow.adicionar(plano)
            uow.commit()
        except Exception:
            uow.rollback()
            raise ErroAoResgatarPlano

    return plano


# AUXILIAR
def filtrar_plano_do_cliente(id_plano: UUID, cliente: Cliente) -> Optional[Plano]:
    return next(filter(lambda p: p.id == id_plano, cliente.planos_contratados), None)

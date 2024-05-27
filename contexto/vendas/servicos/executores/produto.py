from contexto.vendas.dominio.comandos.produto import CriarProduto
from contexto.vendas.dominio.entidades.produto import Produto
from contexto.vendas.erros.produto import ErroAoCriarProduto
from contexto.vendas.repositorios.repos.produto import RepoProduto
from libs.ddd.uow import UoW


def criar_produto(comando: CriarProduto, uow: UoW):
    produto = Produto.criar(
        nome=comando.nome,
        susep=comando.susep,
        idade_de_saida=comando.idade_de_saida,
        idade_de_entrada=comando.idade_de_entrada,
        expiracao_da_venda=comando.expiracao_da_venda,
        carencia_entre_resgates=comando.carencia_entre_resgates,
        valor_minimo_aporte_extra=comando.valor_minimo_aporte_extra,
        valor_minimo_aporte_inicial=comando.valor_minimo_aporte_inicial,
        carencia_inicial_de_resgate=comando.carencia_inicial_de_resgate,
    )
    with uow:
        repo = RepoProduto(uow.session)

        try:
            produto = repo.criar(produto)
            uow.commit()
        except Exception as e:
            uow.rollback()
            raise ErroAoCriarProduto()

    return produto

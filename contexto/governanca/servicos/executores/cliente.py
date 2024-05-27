from contexto.governanca.dominio.comandos.cliente import CriarCliente
from contexto.governanca.dominio.entidades.cliente import Cliente
from contexto.governanca.erros.cliente import ErroAoCriarCliente
from contexto.governanca.repositorios.repos.cliente import RepoCliente
from libs.ddd.uow import UoW


def criar_cliente(comando: CriarCliente, uow: UoW):
    cliente = Cliente.criar(
        cpf=comando.cpf,
        nome=comando.nome,
        email=comando.email,
        genero=comando.genero,
        renda_mensal=comando.renda_mensal,
        data_de_nascimento=comando.data_de_nascimento,
    )
    with uow:
        repo = RepoCliente(uow.session)

        try:
            cliente = repo.criar(cliente)
            uow.commit()
        except Exception as e:
            uow.rollback()
            msg = f"Erro durante a criação do cliente: {str(e)}"
            raise ErroAoCriarCliente(detail=msg, status_code=500)

    return cliente

import uuid
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from freezegun import freeze_time
from validate_docbr import CPF

from contexto.governanca.dominio.modelos.cliente import EntradaCriarCliente
from contexto.governanca.dominio.objeto_de_valor.cliente import Genero
from contexto.vendas.dominio.entidades.produto import Produto
from contexto.vendas.dominio.modelos.plano import (
    EntradaCriarPlano,
    EntradaRealizarAporteExtra,
    EntradaRealizarResgate,
)
from contexto.vendas.dominio.modelos.produto import EntradaCriarProduto
from contexto.vendas.erros.produto import (
    ErroProdutoComIdadeDeEntradaMaiorQueAIdadeDoCliente,
    ErroProdutoComIdadeDeSaidaMaiorQueAIdadeDoCliente,
    ErroProdutoExpirado,
    ErroProdutoNaoEncontrado,
    ErroProdutoNaoTeveValorDoAporteMinimoAtingido,
)
from libs.ddd.uow import UoW


def test_criar_plano_pela_api(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado_cliente = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=2899.50,
        data_de_nascimento="2001-12-04T12:00:00.000Z",
    ).model_dump(mode="json")
    resp_cliente = client.post("/cliente", json=dado_cliente)
    assert resp_cliente.status_code == 201

    dado_produto = EntradaCriarProduto(
        nome="Brasilprev Longo Prazo",
        susep="15414900840201817",
        idade_de_saida=60,
        idade_de_entrada=18,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=365),
    ).model_dump(mode="json")
    resp_produto = client.post("/produto", json=dado_produto)
    assert resp_produto.status_code == 201

    dado_plano = EntradaCriarPlano(
        aporte=1000.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=resp_produto.json()["id"],
        id_cliente=resp_cliente.json()["id"],
    ).model_dump(mode="json")

    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 201


def test_criar_plano_pela_api_com_id_produto_invalido(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado_cliente = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=2899.50,
        data_de_nascimento="2001-12-04T12:00:00.000Z",
    ).model_dump(mode="json")
    resp_cliente = client.post("/cliente", json=dado_cliente)
    assert resp_cliente.status_code == 201

    dado_plano = EntradaCriarPlano(
        aporte=1000.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=uuid.uuid4(),
        id_cliente=resp_cliente.json()["id"],
    ).model_dump(mode="json")

    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 404
    assert resp_plano.json()["detail"] == ErroProdutoNaoEncontrado.detail


def test_criar_plano_pela_api_com_id_cliente_invalido(client: TestClient):
    dado_produto = EntradaCriarProduto(
        nome="Brasilprev Longo Prazo",
        susep="15414900840201817",
        idade_de_saida=60,
        idade_de_entrada=18,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=365),
    ).model_dump(mode="json")
    resp_produto = client.post("/produto", json=dado_produto)
    assert resp_produto.status_code == 201

    dado_plano = EntradaCriarPlano(
        aporte=1000.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=resp_produto.json()["id"],
        id_cliente=uuid.uuid4(),
    ).model_dump(mode="json")

    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 404


def test_criar_plano_pela_api_com_cliente_com_idade_menor_que_a_idade_de_entrada(
    client: TestClient
):
    cpf = CPF()
    cpf.generate()
    dado_cliente = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=2899.50,
        data_de_nascimento="2001-12-04T12:00:00.000Z",
    ).model_dump(mode="json")
    resp_cliente = client.post("/cliente", json=dado_cliente)
    assert resp_cliente.status_code == 201

    dado_produto = EntradaCriarProduto(
        nome="Brasilprev Longo Prazo",
        susep="15414900840201817",
        idade_de_saida=60,
        idade_de_entrada=45,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=365),
    ).model_dump(mode="json")
    resp_produto = client.post("/produto", json=dado_produto)
    assert resp_produto.status_code == 201

    dado_plano = EntradaCriarPlano(
        aporte=1000.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=resp_produto.json()["id"],
        id_cliente=resp_cliente.json()["id"],
    ).model_dump(mode="json")

    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 400
    assert (
        resp_plano.json()["detail"]
        == ErroProdutoComIdadeDeEntradaMaiorQueAIdadeDoCliente.detail
    )


def test_criar_plano_pela_api_com_cliente_com_idade_maior_que_a_idade_de_saida(
    client: TestClient
):
    cpf = CPF()
    cpf.generate()
    dado_cliente = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=2899.50,
        data_de_nascimento="2001-12-04T12:00:00.000Z",
    ).model_dump(mode="json")
    resp_cliente = client.post("/cliente", json=dado_cliente)
    assert resp_cliente.status_code == 201

    dado_produto = EntradaCriarProduto(
        nome="Brasilprev Longo Prazo",
        susep="15414900840201817",
        idade_de_saida=18,
        idade_de_entrada=10,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=365),
    ).model_dump(mode="json")
    resp_produto = client.post("/produto", json=dado_produto)
    assert resp_produto.status_code == 201

    dado_plano = EntradaCriarPlano(
        aporte=1000.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=resp_produto.json()["id"],
        id_cliente=resp_cliente.json()["id"],
    ).model_dump(mode="json")
    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 400
    assert (
        resp_plano.json()["detail"]
        == ErroProdutoComIdadeDeSaidaMaiorQueAIdadeDoCliente.detail
    )


def test_criar_plano_pela_api_com_aporte_inicial_menor_que_o_permitido(
    client: TestClient
):
    cpf = CPF()
    cpf.generate()
    dado_cliente = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=2899.50,
        data_de_nascimento="2001-12-04T12:00:00.000Z",
    ).model_dump(mode="json")
    resp_cliente = client.post("/cliente", json=dado_cliente)
    assert resp_cliente.status_code == 201

    dado_produto = EntradaCriarProduto(
        nome="Brasilprev Longo Prazo",
        susep="15414900840201817",
        idade_de_saida=60,
        idade_de_entrada=18,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=365),
    ).model_dump(mode="json")

    resp_produto = client.post("/produto", json=dado_produto)
    assert resp_produto.status_code == 201

    dado_plano = EntradaCriarPlano(
        aporte=999.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=resp_produto.json()["id"],
        id_cliente=resp_cliente.json()["id"],
    ).model_dump(mode="json")

    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 400
    assert (
        resp_plano.json()["detail"]
        == ErroProdutoNaoTeveValorDoAporteMinimoAtingido.detail
    )


# produto expirado
def test_criar_plano_pela_api_com_produto_expirado(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado_cliente = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=2899.50,
        data_de_nascimento="2001-12-04T12:00:00.000Z",
    ).model_dump(mode="json")
    resp_cliente = client.post("/cliente", json=dado_cliente)
    assert resp_cliente.status_code == 201

    dado_produto = EntradaCriarProduto(
        nome="Brasilprev Longo Prazo",
        susep="15414900840201817",
        idade_de_saida=60,
        idade_de_entrada=18,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=1),
    ).model_dump(mode="json")
    resp_produto = client.post("/produto", json=dado_produto)
    assert resp_produto.status_code == 201

    uow = UoW()
    with uow:
        uow.session.query(Produto).filter(
            Produto.id == resp_produto.json()["id"]
        ).update({"expiracao_da_venda": datetime.now() - timedelta(days=1)})

    dado_plano = EntradaCriarPlano(
        aporte=1000.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=resp_produto.json()["id"],
        id_cliente=resp_cliente.json()["id"],
    ).model_dump(mode="json")

    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 400
    assert resp_plano.json()["detail"] == ErroProdutoExpirado.detail


def test_criar_plano_e_realiza_aporte_extra(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado_cliente = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=2899.50,
        data_de_nascimento="2001-12-04T12:00:00.000Z",
    ).model_dump(mode="json")
    resp_cliente = client.post("/cliente", json=dado_cliente)
    assert resp_cliente.status_code == 201

    dado_produto = EntradaCriarProduto(
        nome="Brasilprev Longo Prazo",
        susep="15414900840201817",
        idade_de_saida=60,
        idade_de_entrada=18,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=365),
    ).model_dump(mode="json")
    resp_produto = client.post("/produto", json=dado_produto)
    assert resp_produto.status_code == 201

    dado_plano = EntradaCriarPlano(
        aporte=1000.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=resp_produto.json()["id"],
        id_cliente=resp_cliente.json()["id"],
    ).model_dump(mode="json")

    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 201

    dado_aporte_extra = EntradaRealizarAporteExtra(
        id_cliente=resp_cliente.json()["id"],
        id_plano=resp_plano.json()["id"],
        valor_aporte=1000.00,
    ).model_dump(mode="json")

    resp_aporte = client.post("/plano/aporte-extra", json=dado_aporte_extra)
    assert resp_aporte.status_code == 200


def test_cria_plano_e_realiza_resgate(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado_cliente = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=2899.50,
        data_de_nascimento="2001-12-04T12:00:00.000Z",
    ).model_dump(mode="json")
    resp_cliente = client.post("/cliente", json=dado_cliente)
    assert resp_cliente.status_code == 201

    dado_produto = EntradaCriarProduto(
        nome="Brasilprev Longo Prazo",
        susep="15414900840201817",
        idade_de_saida=60,
        idade_de_entrada=18,
        carencia_inicial_de_resgate=60,
        carencia_entre_resgates=30,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=365),
    ).model_dump(mode="json")
    resp_produto = client.post("/produto", json=dado_produto)
    assert resp_produto.status_code == 201

    dado_plano = EntradaCriarPlano(
        aporte=1000.00,
        idade_de_aposentadoria=65,
        data_da_contratacao=datetime.now(),
        id_produto=resp_produto.json()["id"],
        id_cliente=resp_cliente.json()["id"],
    ).model_dump(mode="json")

    resp_plano = client.post("/plano", json=dado_plano)
    assert resp_plano.status_code == 201

    with freeze_time(datetime.now() + timedelta(days=61)):
        dado_resgate = EntradaRealizarResgate(
            id_plano=resp_plano.json()["id"],
            valor_resgate=100.00,
        ).model_dump(mode="json")

        resp_resgate = client.post("/plano/resgate", json=dado_resgate)
        assert resp_resgate.status_code == 200

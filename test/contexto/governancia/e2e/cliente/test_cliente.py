from fastapi.testclient import TestClient
from validate_docbr import CPF

from contexto.governanca.dominio.modelos.cliente import EntradaCriarCliente
from contexto.governanca.dominio.objeto_de_valor.cliente import Genero


def test_criar_cliente_pela_api(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Asuka Langley Soryu",
        email="asuka@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=10000.00,
        data_de_nascimento="2001-12-04",
    )
    resp = client.post("/cliente", json=dado.model_dump(mode="json"))

    assert resp.status_code == 201


def test_nao_pode_criar_cliente_com_cpf_invalido(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Shinji Ikari",
        email="shinji@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=10000.00,
        data_de_nascimento="2001-12-04",
    )
    dado.cpf = "12345678901"
    resp = client.post("/cliente", json=dado.model_dump(mode="json"))

    assert resp.status_code == 422


def test_nao_pode_criar_cliente_com_email_invalido(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Rei Ayanami",
        email="rei@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=10000.00,
        data_de_nascimento="2001-03-30",
    )
    dado.email = "rei@nerv"
    resp = client.post("/cliente", json=dado.model_dump(mode="json"))

    assert resp.status_code == 422


def test_nao_pode_criar_cliente_com_genero_invalido(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Kaworu Nagisa",
        email="kaworu@nerv.com",
        genero=Genero.FEMININO,
        renda_mensal=10000.00,
        data_de_nascimento="2000-09-13",
    )
    dado.genero = "X"
    resp = client.post("/cliente", json=dado.model_dump(mode="json"))

    assert resp.status_code == 422


def test_criar_com_cpf_ja_existente(client: TestClient):
    cpf = CPF()
    cpf.generate()
    dado = EntradaCriarCliente(
        cpf=cpf.generate(),
        nome="Gendo Ikari",
        email="gendo@nerv.com",
        genero=Genero.MASCULINO,
        renda_mensal=10000.00,
        data_de_nascimento="1967-04-29",
    )
    resp = client.post("/cliente", json=dado.model_dump(mode="json"))
    assert resp.status_code == 201

    resp = client.post("/cliente", json=dado.model_dump(mode="json"))
    assert resp.status_code == 500

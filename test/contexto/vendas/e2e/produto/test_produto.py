from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from contexto.vendas.dominio.modelos.produto import EntradaCriarProduto


def test_criar_produto_pela_api(client: TestClient):
    dado = EntradaCriarProduto(
        nome="Produto Inicial",
        susep="123456",
        idade_de_saida=60,
        idade_de_entrada=18,
        carencia_inicial_de_resgate=30,
        carencia_entre_resgates=180,
        valor_minimo_aporte_extra=100.00,
        valor_minimo_aporte_inicial=1000.00,
        expiracao_da_venda=datetime.now() + timedelta(days=365),
    )
    resp = client.post("/produto", json=dado.model_dump(mode="json"))

    assert resp.status_code == 201

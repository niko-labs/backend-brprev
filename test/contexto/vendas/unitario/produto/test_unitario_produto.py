from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from contexto.vendas.dominio.modelos.produto import EntradaCriarProduto
from contexto.vendas.erros.produto import (
    ErroProdutoComIdadeDeEntradaMaiorQueAIdadeDoCliente,
)


def test_erro_idade_de_entrada_maior_que_idade_de_saida():
    with pytest.raises(ValidationError):
        EntradaCriarProduto(
            nome="Erro: Idade de entrada maior que idade de saída",
            susep="123456",
            idade_de_saida=18,
            idade_de_entrada=60,
            carencia_inicial_de_resgate=30,
            carencia_entre_resgates=180,
            valor_minimo_aporte_extra=100.00,
            valor_minimo_aporte_inicial=1000.00,
            expiracao_da_venda=datetime.now() + timedelta(days=365),
        )


def test_erro_carencia_entre_resgates_negativa():
    with pytest.raises(ValidationError):
        EntradaCriarProduto(
            nome="Erro: Carência entre resgates negativa",
            susep="123456",
            idade_de_saida=60,
            idade_de_entrada=18,
            carencia_inicial_de_resgate=30,
            carencia_entre_resgates=-180,
            valor_minimo_aporte_extra=100.00,
            valor_minimo_aporte_inicial=1000.00,
            expiracao_da_venda=datetime.now() + timedelta(days=365),
        )


def test_erro_carencia_inicial_de_resgate_negativa():
    with pytest.raises(ValidationError):
        EntradaCriarProduto(
            nome="Erro: Carência inicial de resgate negativa",
            susep="123456",
            idade_de_saida=60,
            idade_de_entrada=18,
            carencia_inicial_de_resgate=-30,
            carencia_entre_resgates=180,
            valor_minimo_aporte_extra=100.00,
            valor_minimo_aporte_inicial=1000.00,
            expiracao_da_venda=datetime.now() + timedelta(days=365),
        )


def test_erro_valor_minimo_aporte_inicial_negativo():
    with pytest.raises(ValidationError):
        EntradaCriarProduto(
            nome="Erro: Valor mínimo de aporte inicial negativo",
            susep="123456",
            idade_de_saida=60,
            idade_de_entrada=18,
            carencia_inicial_de_resgate=30,
            carencia_entre_resgates=180,
            valor_minimo_aporte_extra=100.00,
            valor_minimo_aporte_inicial=-1000.00,
            expiracao_da_venda=datetime.now() + timedelta(days=365),
        )


def test_erro_valor_minimo_aporte_extra_negativo():
    with pytest.raises(ValidationError):
        EntradaCriarProduto(
            nome="Erro: Valor mínimo de aporte extra negativo",
            susep="123456",
            idade_de_saida=60,
            idade_de_entrada=18,
            carencia_inicial_de_resgate=30,
            carencia_entre_resgates=180,
            valor_minimo_aporte_extra=-100.00,
            valor_minimo_aporte_inicial=1000.00,
            expiracao_da_venda=datetime.now() + timedelta(days=365),
        )


def test_nao_generar_erro_com_valores_corretos():
    EntradaCriarProduto(
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

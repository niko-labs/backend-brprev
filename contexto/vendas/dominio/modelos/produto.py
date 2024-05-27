from datetime import datetime
from uuid import UUID

from pydantic import model_validator

from libs.fastapi.camelcase import Modelo


class EntradaCriarProduto(Modelo):
    nome: str
    susep: str
    expiracao_da_venda: datetime

    valor_minimo_aporte_inicial: float
    valor_minimo_aporte_extra: float

    idade_de_entrada: int
    idade_de_saida: int

    carencia_entre_resgates: int
    carencia_inicial_de_resgate: int

    @model_validator(mode="after")
    def validacoes(cls, dados):
        if dados.idade_de_entrada > dados.idade_de_saida:
            raise ValueError("A idade de entrada deve ser menor que a idade de saída")

        if dados.carencia_entre_resgates < 0:
            raise ValueError("A carência entre resgates deve ser maior ou igual a zero")

        if dados.carencia_inicial_de_resgate < 0:
            raise ValueError(
                "A carência inicial de resgate deve ser maior ou igual a zero"
            )
        if dados.valor_minimo_aporte_inicial < 0:
            raise ValueError(
                "O valor mínimo de aporte inicial deve ser maior ou igual a zero"
            )
        if dados.valor_minimo_aporte_extra < 0:
            raise ValueError(
                "O valor mínimo de aporte extra deve ser maior ou igual a zero"
            )
        if dados.expiracao_da_venda <= datetime.now(tz=dados.expiracao_da_venda.tzinfo):
            raise ValueError(
                "A data de expiração da venda deve ser maior que a data atual"
            )
        return dados


class SaidaProduto(Modelo):
    id: UUID
    nome: str
    susep: str
    expiracao_da_venda: datetime

    valor_minimo_aporte_inicial: float
    valor_minimo_aporte_extra: float

    idade_de_entrada: int
    idade_de_saida: int

    carencia_entre_resgates: int
    carencia_inicial_de_resgate: int


if __name__ == "__main__":
    from datetime import timedelta

    # erro idade de entrada maior que idade de saída
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

    # erro carencia entre resgates negativa
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

    # erro carencia inicial de resgate negativa
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

    # erro valor mínimo de aporte inicial negativo
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

    # erro valor mínimo de aporte extra negativo
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

    # sucesso
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

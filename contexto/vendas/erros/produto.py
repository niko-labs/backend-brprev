from dataclasses import dataclass

from libs.fastapi.exception import ExceptionBase


@dataclass
class ErroAoCriarProduto(ExceptionBase):
    detail = "Erro durante a criação do produto."
    status_code = 500


@dataclass
class ErroProdutoExpirado(ExceptionBase):
    detail = "Produto expirado."
    status_code = 400


@dataclass
class ErroProdutoNaoEncontrado(ExceptionBase):
    detail = "Produto não encontrado."
    status_code = 404


@dataclass
class ErroProdutoNaoTeveValorDoAporteMinimoAtingido(ExceptionBase):
    detail = "O valor do aporte não atingiu o valor mínimo."
    status_code = 400


@dataclass
class ErroProdutoComIdadeDeEntradaMaiorQueAIdadeDoCliente(ExceptionBase):
    detail = "A idade do cliente é menor que a idade de entrada do produto. A idade minima para compra do produto."
    status_code = 400


@dataclass
class ErroProdutoComIdadeDeSaidaMaiorQueAIdadeDoCliente(ExceptionBase):
    detail = "A idade do cliente é maior que a idade de saída do produto. A idade maxima para comecar a usufruir do produto."
    status_code = 400

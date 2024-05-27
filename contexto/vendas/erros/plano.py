from dataclasses import dataclass

from libs.fastapi.exception import ExceptionBase


@dataclass
class ErroAoCriarPlano(ExceptionBase):
    detail = "Erro durante a criação do plano."
    status_code = 500


@dataclass
class ErroAoResgatarPlano(ExceptionBase):
    detail = "Erro durante o resgate do plano."
    status_code = 500


@dataclass
class ErroPlanoNaoEncontrado(ExceptionBase):
    detail = "Plano não encontrado."
    status_code = 404


@dataclass
class ErroPlanoJaFoiFinalizado(ExceptionBase):
    detail = "Plano não sofrer mais alterações, pois já foi finalizado."
    status_code = 400


@dataclass
class ErroPlanoSendoResgatadoAntesDoPeridoDeCarencia(ExceptionBase):
    detail = "Plano está sendo resgatado antes do período de carência."
    status_code = 400


@dataclass
class ErroPlanoSendoResgatadoAntesDoPeridoDeCarenciaEntreResgates(ExceptionBase):
    detail = "Plano está sendo resgatado antes do período de carência entre resgates."
    status_code = 400


@dataclass
class ErroValorDoResgateMaiorQueAporte(ExceptionBase):
    detail = "Valor do resgate é maior que o valor do aporte."
    status_code = 400


@dataclass
class ErroPlanoNaoPodeSerFinalizadoJaQueAindaPossuiAporte(ExceptionBase):
    detail = "Plano não pode ser finalizado, pois ainda possui aporte."
    status_code = 400
